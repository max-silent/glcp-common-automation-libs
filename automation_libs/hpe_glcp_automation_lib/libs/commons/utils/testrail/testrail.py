import base64
import configparser
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from enum import Enum

import click
import requests

from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import Settings

LOG = logging.getLogger(__name__)
TESTRAIL_BASE_URL = "https://testrail.glcp.hpedev.net/"
DEFAULT_PROJECT = "GLCP"
PYTEST_RESULTS = {}


class TestRailResult(Enum):
    PASSED = 1
    BLOCKED = 2
    UNTESTED = 3
    RETEST = 4
    FAILED = 5


class PyTestRail(object):
    """
    Client for the TestRail API with a straightforward integration with Pytest. This
    library uses contest.py for initializing and tracking test results, then uses the
    method testrail_upload_pytest_results() to upload the test results into TestRail.
    """

    def __init__(self, username=None, password=None, base_url=None):
        self.username = username or os.getenv("TR_USERNAME")
        self.password = password or os.getenv("TR_PASSWORD")

        if self.username is None or self.password is None:
            # Attempt to get creds from S3 bucket or local cred file.
            tr_creds = Settings.download_tr_creds()
            self.username = tr_creds["API"]["user"]
            self.password = tr_creds["API"]["password"]

        if self.username is None or self.password is None:
            raise TestRailError("TestRail API requires TR_USERNAME and TR_PASSWORD")
        if base_url is None:
            base_url = TESTRAIL_BASE_URL
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.__url = base_url + "index.php?/api/v2/"

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)

    def __send_request(self, method, uri, data) -> dict:
        url = self.__url + uri

        auth = str(
            base64.b64encode(bytes("%s:%s" % (self.username, self.password), "utf-8")),
            "ascii",
        ).strip()
        headers = {"Authorization": "Basic " + auth}

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = {"attachment": (open(data, "rb"))}
                response = requests.post(url, headers=headers, files=files)
                files["attachment"].close()
            else:
                headers["Content-Type"] = "application/json"
                payload = bytes(json.dumps(data), "utf-8")
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except Exception as e:  # response.content not formatted as JSON
                LOG.error(e)
                error = str(response.content)
            raise TestRailError(
                "TestRail API returned HTTP %s (%s)" % (response.status_code, error)
            )
        else:
            if uri[:15] == "get_attachment/":  # Expecting file, not JSON
                try:
                    open(data, "wb").write(response.content)
                    return data
                except Exception as e:
                    LOG.error(e)
                    return {"error": "Error saving attachment."}
            else:
                try:
                    return response.json()
                except Exception as e:  # Nothing to return
                    LOG.error(e)
                    return {}

    def get_active_projects(self):
        return self.send_get("get_projects&is_completed=0")

    def get_project_id(self, project_name):
        projects = self.get_active_projects()
        for project in projects["projects"]:
            if project["name"] == project_name:
                return project["id"]
        return 0

    def get_milestone(self, milestone_id):
        return self.send_get(f"get_milestone/{milestone_id}")

    def get_milestones(self, project_id):
        return self.send_get(f"get_milestones/{project_id}")

    def get_milestone_name(self, milestone_id):
        """Given milestone ID, return milestone name."""
        return self.get_milestone(milestone_id)["name"]

    def get_current_milestone(self, project_id=None):
        """
        Get the current milestone for a project ID (if not defined then use
        DEFAULT_PROJECT which is GLCP).
        """
        if project_id is None:
            project_id = self.get_project_id(DEFAULT_PROJECT)
        milestone_id = self.get_parent_milestone_id(project_id)
        return self.get_milestone(milestone_id)

    def get_parent_milestone_id(self, project_id, milestone_name=None):
        milestones = self.get_milestones(project_id)
        if milestone_name is not None:
            for milestone in milestones["milestones"]:
                if milestone["name"] == milestone_name:
                    return milestone["id"]
            return 0
        else:
            # Look up the current milestone in default project ("GLCP") by comparing
            # the current time with the start/end times in the project milestones,
            # but skipping completed milestones and milestones with undefined
            # start/end times.

            current_time = time.time()

            default_project_id = self.get_project_id(DEFAULT_PROJECT)
            if default_project_id != project_id:
                raise TestRailError(
                    f"TestRail API requires milestone unless project is {DEFAULT_PROJECT}"
                )
            match_list = []
            for milestone in milestones["milestones"]:
                # milestone_name_id = f"{milestone['name']} (ID: {milestone['id']})"
                if milestone["is_completed"] is True:
                    # LOG.info(f"Skipping {milestone_name_id} - milestone completed")
                    continue
                elif milestone["started_on"] is None:
                    # LOG.info(f"Skipping {milestone_name_id} - start date undefined")
                    continue
                elif milestone["started_on"] > current_time:
                    # LOG.info(f"Skipping {milestone_name_id} - start date in future")
                    continue
                elif milestone["due_on"] is None:
                    # LOG.info(f"Skipping {milestone_name_id} - due date undefined")
                    continue
                elif milestone["due_on"] + 24 * 60 * 60 < current_time:
                    # Milestone dates in TestRail are not exact and there may be gaps
                    # between milestones. So add a time buffer (24 hours) to the
                    # milestone end date.

                    # LOG.info(f"Skipping {milestone_name_id} - due date in past")
                    continue
                else:
                    match_list.append(milestone)
            if len(match_list) == 0:
                raise TestRailError(
                    f"TestRail API not able to find the current milestone in project"
                    f" {DEFAULT_PROJECT}"
                )
            elif len(match_list) > 1:
                LOG.info(
                    f"WARNING: Found multiple current milestones"
                    f" {[x['name'] for x in match_list]}"
                    f" in project {DEFAULT_PROJECT}. Use the first match."
                )
                return match_list[0]["id"]
            else:
                # Found the current milestone.
                return match_list[0]["id"]

    def get_child_milestone_id(self, parent_id, milestone_name):
        milestones = self.get_milestone(parent_id)["milestones"]
        for milestone in milestones:
            if milestone["name"] == milestone_name:
                return milestone["id"]
        return 0

    def add_milestone(self, project_id, milestone_name, parent_id=None):
        payload = {"name": milestone_name}
        if parent_id:
            payload["parent_id"] = parent_id
        result = self.send_post(f"add_milestone/{project_id}", payload)
        return result["id"]

    def get_suite(self, suite_id):
        return self.send_get(f"get_suite/{suite_id}")

    def get_suites(self, project_id):
        return self.send_get(f"get_suites/{project_id}")

    def get_suite_id(self, project_id, suite_name):
        suites = self.get_suites(project_id)
        for suite in suites:
            if suite["name"] == suite_name:
                return suite["id"]
        return 0

    def add_suite(self, project_id, suite_name, description=None):
        payload = {"name": suite_name}
        if description:
            payload["description"] = description
        result = self.send_post(f"add_suite/{project_id}", payload)
        return result["id"]

    def get_section(self, section_id):
        return self.send_get(f"get_section/{section_id}")

    def get_sections(self, project_id, suite_id):
        return self.send_get(f"get_sections/{project_id}&suite_id={suite_id}")

    def get_section_id(self, project_id, suite_id, section_name):
        sections = self.get_sections(project_id, suite_id)
        for section in sections["sections"]:
            if section["name"] == section_name:
                return section["id"]
        return 0

    def add_section(self, project_id, suite_id, section_name, description=None):
        payload = {"name": section_name, "suite_id": suite_id}
        if description:
            payload["description"] = description
        result = self.send_post(f"add_section/{project_id}", payload)
        return result["id"]

    def get_case(self, case_id):
        return self.send_get(f"get_case/{case_id}")

    def get_cases(self, project_id, suite_id, limit=250, offset=0):
        return self.send_get(
            f"get_cases/{project_id}&suite_id={suite_id}&limit={limit}&offset={offset}"
        )

    def get_cases_data(self, proj_id, suite_id):
        """
        The api returns maximum 250 items per page.
        We want fetch everything, so we'll make consecutive calls.
        """

        cases_data = {}
        page_size = 250

        # Limit page count to 10.
        for offset in range(0, page_size * 10, page_size):
            try:
                cases = self.get_cases(proj_id, suite_id, limit=page_size, offset=offset)

                for case in cases["cases"]:
                    key = case["id"]
                    cases_data[key] = dict(case)
                if len(cases["cases"]) < page_size:
                    break
            except Exception as e:
                LOG.warning(f"Error while processing cases at offset {offset}: '{e}'")

        return cases_data

    def get_plan(self, plan_id):
        return self.send_get(f"get_plan/{plan_id}")

    def get_plans(self, project_id, milestone_id=None):
        if milestone_id:
            return self.send_get(f"get_plans/{project_id}&milestone_id={milestone_id}")
        return self.send_get(f"get_plans/{project_id}")

    def get_plan_id(self, project_id, milestone_id, plan_name):
        retry = 2
        plans = self.get_plans(project_id)
        while retry != 0:
            for plan in plans["plans"]:
                if plan["name"] == plan_name and plan["milestone_id"] == milestone_id:
                    return plan["id"]
            plans = self.get_plans(project_id, milestone_id)
            retry -= 1
        return 0

    def add_plan(self, project_id, milestone_id, plan_name, description=None):
        payload = {"name": plan_name, "milestone_id": milestone_id}
        if description:
            payload["description"] = description
        result = self.send_post(f"add_plan/{project_id}", payload)
        return result["id"]

    def add_plan_entry(
        self,
        plan_id,
        test_run_name,
        suite_id,
        case_ids=None,
        config_ids=None,
        description=None,
    ):
        payload = {"name": test_run_name, "suite_id": suite_id, "include_all": False}
        if isinstance(case_ids, list):
            payload["case_ids"] = case_ids
        if isinstance(config_ids, list):
            payload["config_ids"] = config_ids
        if description:
            payload["description"] = description
        result = self.send_post(f"add_plan_entry/{plan_id}", payload)
        return result["id"]

    def get_run(self, run_id):
        return self.send_get(f"get_run/{run_id}")

    def get_runs(self, plan_id):
        return self.get_plan(plan_id)["entries"]

    def get_run_ids(self, plan_id, run_name):
        entries = self.get_runs(plan_id)
        run_ids = []
        for entry in entries:
            if entry["name"] == run_name:
                for run in entry["runs"]:
                    run_ids.append(run["id"])
                return run_ids
        run_ids.append(0)
        return run_ids

    def get_test(self, test_id):
        return self.send_get(f"get_test/{test_id}")

    def get_tests(self, run_id, limit=250, offset=0):
        return self.send_get(f"get_tests/{run_id}&limit={limit}&offset={offset}")

    def get_tests_data(self, run_id):
        """
        The api returns maximum 250 items per page.
        We want fetch everything, so we'll make consecutive calls.
        """
        if run_id == 0:
            LOG.warning(f"Invalid test run ID: {run_id}")
            return

        tests_data = {}
        page_size = 250

        # Limit page count to 10.
        for offset in range(0, page_size * 10, page_size):
            try:
                tests = self.get_tests(run_id, limit=page_size, offset=offset)

                for test in tests["tests"]:
                    key = test["case_id"]
                    tests_data[key] = dict(test)
                if len(tests["tests"]) < page_size:
                    break
            except Exception as e:
                LOG.warning(f"Error while processing tests at offset {offset}: '{e}'")

        return tests_data

    def add_result(self, test_id, status_id, comment=None):
        # status_id
        #   1: Passed
        #   2: Blocked
        #   3: Untested (not allowed when adding a new result)
        #   4: Retest
        #   5: Failed

        # By default, new tests have the status of Untested. The add_result API doesn't
        # allow you to set status to Untested - it will fails with error
        # 'Field :status_id uses an invalid status (Untested)'. The workaround is to
        # not post result when status is Untested.

        if status_id == TestRailResult.UNTESTED.value:
            result = {}
            # Don't post result
        else:
            payload = {"status_id": status_id}
            if comment:
                payload["comment"] = comment
            result = self.send_post(f"add_result/{test_id}", payload)
        return result

    def testrail_upload_pytest_results(self, results, testrail_configs):
        child_milestone = testrail_configs["child_milestone"] or "UndefTestType"
        if re.match(r"false", os.getenv("TR_RESULT_POPULATE", "true"), re.IGNORECASE):
            LOG.info("Env TR_RESULT_POPULATE is false. Don't upload results to TestRail.")
            return
        elif child_milestone == "UndefTestType":
            LOG.info(
                "Sub-milestone is 'UndefTestType'. Don't upload results to TestRail."
            )
            return

        # If tc_ids list is populated,
        #   then show executed tests vs expected tests
        #   else show executed tests
        if testrail_configs["tc_ids"]:
            tc_ids = testrail_configs["tc_ids"]
        else:
            tc_ids = list(results.keys())

        if not tc_ids:
            LOG.info(
                "TestRail markers are not defined. Don't upload results to TestRail."
            )
            return

        LOG.info("Uploading results to TestRail...")
        if "project" not in testrail_configs or not testrail_configs["project"]:
            project_name = DEFAULT_PROJECT
        else:
            project_name = testrail_configs["project"]
        project_id = self.get_project_id(project_name)
        LOG.info(f"  Project: {project_name}, id: {project_id}")

        # Get milestone id, or add milestone if it doesn't exist
        if "milestone" not in testrail_configs or not testrail_configs["milestone"]:
            milestone_name = None
        else:
            milestone_name = testrail_configs["milestone"]
        milestone_id = self.get_parent_milestone_id(project_id, milestone_name)
        if milestone_name is None:
            milestone_name = self.get_milestone_name(milestone_id)
        if milestone_id == 0:
            milestone_id = self.add_milestone(project_id, milestone_name)
        LOG.info(f"  Milestone: {milestone_name}, id: {milestone_id}")

        # Get sub milestone id, or add sub milestone if it doesn't exist
        child_milestone_id = self.get_child_milestone_id(milestone_id, child_milestone)
        if child_milestone_id == 0:
            child_milestone_id = self.add_milestone(
                project_id, child_milestone, milestone_id
            )
        LOG.info(f"  Sub Milestone: {child_milestone}, id: {child_milestone_id}")
        if child_milestone_id != 0:
            milestone_id = child_milestone_id

        # Get suite id, add suite if it doesn't exist
        if not testrail_configs["test_suite"]:
            raise TestRailError("test_suite is not defined or is empty string.")
        suite_id = self.get_suite_id(project_id, testrail_configs["test_suite"])
        if suite_id == 0:
            suite_id = self.add_suite(
                project_id, testrail_configs["test_suite"], "Added by Pytest automation"
            )
        LOG.info(f"  Suite: {testrail_configs['test_suite']}, id: {suite_id}")

        # # Get suite section id, add section if it doesn't exist
        # # 2023-07-19 [Vui]: Not sure if we need this. The assumption is that the
        # #   suite and sections are already defined, so we can simply populate results.
        #
        # section_id = self.get_section_id(
        #     project_id, suite_id, testrail_configs["test_suite_section"]
        # )
        # if section_id == 0:
        #     section_id = self.add_section(
        #         project_id, suite_id, testrail_configs["test_suite_section"]
        #     )
        # LOG.info(
        #     f"  Suite Section: {testrail_configs['test_suite_section']}, id: {section_id}"
        # )

        # Get test plan id, add plan if it doesn't exist
        plan_id = self.get_plan_id(
            project_id, milestone_id, testrail_configs["test_plan"]
        )
        if plan_id == 0:
            plan_id = self.add_plan(
                project_id, milestone_id, testrail_configs["test_plan"]
            )
        LOG.info(f"  Test Plan: {testrail_configs['test_plan']}, id: {plan_id}")

        # Check for invalid tests case IDs
        all_tc_ids = [case for case in self.get_cases_data(project_id, suite_id).keys()]
        invalid_tc_ids = list(set(tc_ids) - set(all_tc_ids))
        valid_tc_ids = list(set(tc_ids) - set(invalid_tc_ids))

        # Get test run id, add test run and test cases if they don't exist
        run_id = self.get_run_ids(plan_id, testrail_configs["test_run"])[0]
        if run_id == 0:
            # Dump selected environment variables into test run descriptions
            descr = "Environment variables:\n\n"
            # descr += f"    env_keys={':'.join(list(dict(os.environ).keys()))}\n\n"
            env_vars = (
                "PYTHONPATH|PWD|HOME|USER|CollectionType|"
                + "BUILD_NUMBER|BUILD_ID|JOB_NAME|WORKSPACE|BUILD_URL"
            )
            for k, v in os.environ.items():
                if re.match(rf"^({env_vars})$", k):
                    descr += f"    {k}={v}\n"
            try:
                self.add_plan_entry(
                    plan_id,
                    testrail_configs["test_run"],
                    suite_id,
                    case_ids=valid_tc_ids,
                    description=descr,
                )
                run_id = self.get_run_ids(plan_id, testrail_configs["test_run"])[0]
                LOG.info(f"  Test Run: {testrail_configs['test_run']}, id: {run_id}")
            except Exception as e:
                LOG.warning(
                    f"Failed to create test run '{testrail_configs['test_run']}',"
                    f" valid case IDs: {valid_tc_ids}: {e}"
                )
                return

        # Get tests info for results update
        tests_data = self.get_tests_data(run_id)
        for tc_id in tc_ids:
            if tc_id in results.keys():
                status = results[tc_id]["status"]
                comment = results[tc_id]["comment"]
                try:
                    self.add_result(tests_data[tc_id]["id"], status, comment)
                    LOG.info(
                        f"TestRail result posted for test case ID {tc_id}"
                        f" ({TestRailResult(status).name})"
                    )
                except Exception as e:
                    LOG.warning(
                        f"Not able to update TestRail result - invalid case ID {tc_id}"
                        f" due to error '{type(e)}': {e}"
                    )

        if invalid_tc_ids:
            LOG.warning(
                f"Not able to update TestRail result for the following invalid case IDs: {invalid_tc_ids}"
            )

        tr_results_link = f"{self.base_url}index.php?/runs/view/{run_id}"
        LOG.info(f"TestRail results: {tr_results_link}")
        os.environ["tr_link"] = tr_results_link

    @staticmethod
    def prepare_results(results):
        for test in results:
            result = results[test][0]
            test_id = results[test][1]
            comment = str(results[test][2])
            if comment:
                comment = (
                    "# Pytest result: #\n    " + comment.replace("\n", "\n    ") + "\n"
                )
            else:
                comment = "Pytest automation result"
            if result.passed is True:
                status = TestRailResult.PASSED.value
            elif result.skipped is True:
                status = TestRailResult.UNTESTED.value
            else:
                # Assume that test failed.
                status = TestRailResult.FAILED.value
            PYTEST_RESULTS[test_id] = {"status": status, "comment": comment}
        return PYTEST_RESULTS


class TestRailError(Exception):
    pass


class TestRail:
    def __init__(
        self,
        url,
        email,
        password,
        project_id=None,
        tr_config="/tmp",
    ):
        """
        Initializes the TestRail object with the TestRail API URL, email, password,
        project ID, headers, description, and TestRail configuration path.

        Args:
            url (str): The TestRail API URL.
            email (str): The email address associated with the TestRail account.
            password (str): The password associated with the TestRail account.
            project_id (int): The ID of the project in TestRail.
            tr_config (str): The TestRail configuration path.
        """
        self.password = password
        self.url = url
        self.email = email
        self.project_id = project_id
        self.headers = {"Content-Type": "application/json"}
        self.description = "This Run is created from Automated code."
        self.tr_config = tr_config

    def create_plan(self, plan_file):
        """
        Creates a Test Plan in TestRail.

        Args:
            plan_file (str): The absolute path of the JSON file containing the plan detail.

        Returns:
            id (int) of the plan if exist else dictionary with newly created plan data,
              or None if any errors appear.
        """
        output = {"TestRail": []}
        now = datetime.utcnow()
        time = now.strftime("%B-%d-%Y-%H:%M:%S")
        try:
            add_plan_url = f"{self.url}/index.php?/api/v2/add_plan/{self.project_id}"
            with open(plan_file) as json_file:
                plan = json.load(json_file)
            plan_id = self.get_plan_id(plan_name=plan["name"])
            if plan_id:
                return plan_id

            for entry in plan["entries"]:
                entry["name"] = entry["name"] + " - " + time
            milestone_id = plan.get("milestone_id")
            response = requests.post(
                add_plan_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(plan),
            )

            if response.status_code == 200:
                LOG.info(response.json())
                plan_id = response.json()["id"]
                for entry in response.json()["entries"]:
                    file = f"testrail-{entry['suite_id']}-{time}.cfg"
                    file_path = "{}".format(os.path.join(self.tr_config, file))
                    self.create_testrail_config_file(
                        suite_id=entry["suite_id"],
                        run_id=entry["runs"][0]["id"],
                        run_name=entry["runs"][0]["name"],
                        file_path=file_path,
                        plan_id=plan_id,
                        milestone_id=milestone_id,
                    )

                    output_data = {
                        "suite_id": int(entry["suite_id"]),
                        "run_id": entry["runs"][0]["id"],
                        "configuration_file": file_path,
                        "plan_id": plan_id,
                    }
                    if milestone_id:
                        output_data["milestone_id"] = milestone_id
                    output["TestRail"].append(output_data)
                LOG.info(f"Plan Id: {plan_id} got created.")
                return output
            else:
                LOG.error(
                    "Failed to create Test Plan in TestRail with error:"
                    + f" {response.status_code}"
                )
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def update_plan(self, plan_id, plan_file):
        """Update an existing Test Plan in TestRail with new test runs.

        Args:
            plan_id (int): The ID of the existing plan to update.
            plan_file (str): The absolute file path to the JSON file containing the plan details.

        Returns:
            dict: A dictionary containing information about the updated Test Plan.

        Raises:
            Exception: If an error occurs while updating the Test Plan.
        """
        output = {"TestRail": []}
        now = datetime.utcnow()
        time = now.strftime("%B-%d-%Y-%H:%M:%S")
        try:
            update_plan_url = f"{self.url}/index.php?/api/v2/add_plan_entry/{plan_id}"
            with open(plan_file) as json_file:
                plan = json.load(json_file)

            milestone_id = plan.get("milestone_id")

            for entry in plan["entries"]:
                entry["name"] = entry["name"] + " - " + time
                response = requests.post(
                    update_plan_url,
                    headers=self.headers,
                    auth=(self.email, self.password),
                    data=json.dumps(entry),
                )
                if response.status_code == 200:
                    plan_updated = response.json()
                    file = f"testrail-{plan_updated['suite_id']}-{time}.cfg"
                    file_path = "{}".format(os.path.join(self.tr_config, file))
                    self.create_testrail_config_file(
                        suite_id=plan_updated["suite_id"],
                        run_id=plan_updated["runs"][0]["id"],
                        run_name=plan_updated["runs"][0]["name"],
                        file_path=file_path,
                        plan_id=plan_id,
                        milestone_id=milestone_id,
                    )

                    output_data = {
                        "suite_id": int(plan_updated["suite_id"]),
                        "run_id": plan_updated["runs"][0]["id"],
                        "configuration_file": file_path,
                        "plan_id": plan_id,
                    }
                    if milestone_id:
                        output_data["milestone_id"] = milestone_id

                    output["TestRail"].append(output_data)

                else:
                    LOG.error(
                        "Failed to update plan with new runs for suite id {}.".format(
                            entry["suite_id"]
                        )
                    )
                    output["TestRail"][0].append(
                        {
                            "suite_id": int(entry["suite_id"]),
                            "error": "Failed to update plan with new runs for suite id {}.",
                        }
                    )
            LOG.info(f"Plan ID {plan_id} got updated.")
            return output
        except Exception as e:
            LOG.error(e)
            return None

    def create_run(self, suite_id, run_name=None, milestone_id=None, case_ids=None):
        """
        Create a new TestRail test run and returns the run ID along with its
        configuration file path.

        Args:
            suite_id (int): The ID of the Test Suite.
            run_name (str, optional): The name of the test run. If None, a default name with the current timestamp will
            be used.
            milestone_id (int, optional): The ID of the milestone to link the test run to.
            case_ids (List[str], optional): The list of case IDs to include in the test run. If None, all cases in the
            suite will be included.
        Returns:
            A dictionary containing information about the created test run, including the Test Suite ID, Run ID, and
            the configuration file path. Returns None if the test run creation fails.
        Raises:
            None
        """
        output = {"TestRail": []}
        now = datetime.utcnow()
        time = now.strftime("%B-%d-%Y-%H:%M:%S")
        try:
            add_run_url = f"{self.url}/index.php?/api/v2/add_run/{self.project_id}"
            if run_name is None:
                run_name = "Automated Run - " + time
            else:
                run_name = "{}-{}".format(run_name, time)

            data = {"suite_id": int(suite_id), "name": run_name}
            if case_ids is None:
                data["include_all"] = True
            else:
                data["include_all"] = False
                data["case_ids"] = [
                    int(case.replace("C", "")) if "C" in case else int(case)
                    for case in case_ids
                ]

            if milestone_id is not None:
                data["milestone_id"] = int(milestone_id)

            response = requests.post(
                add_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data),
            )
            if response.status_code == 200:
                run_id = response.json()["id"]
                file = f"testrail-{suite_id}-{time}.cfg"
                file_path = "{}".format(os.path.join(self.tr_config, file))
                self.create_testrail_config_file(
                    suite_id=suite_id,
                    run_id=run_id,
                    run_name=run_name,
                    plan_id=None,
                    milestone_id=None,
                    file_path=file_path,
                )
                LOG.info(f"Run Id: {run_id} got created.")
                output_data = {
                    "suite_id": int(suite_id),
                    "run_id": int(run_id),
                    "configuration_file": file_path,
                }
                if milestone_id:
                    output_data["milestone_id"] = milestone_id
                output["TestRail"].append(output_data)
                return output
            else:
                LOG.error(
                    f"Failed to created Run in TestRail: Error {response.status_code}"
                )
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def get_tests_for_run(self, run_id):
        """Return an existing test_id details for a particular test run.
        Includes:
        ID: Test_id in a test run
        Title: Title for the for particular test_id
        status_id: Status of the test_id from 1....5
        -------------------------------------------
        run_id (int) - The ID of the test run (required)
        """
        test_data = {}
        try:
            get_tests_url = f"{self.url}/index.php?/api/v2/get_tests/{run_id}"
            response = requests.get(
                get_tests_url, headers=self.headers, auth=(self.email, self.password)
            )

            if response.status_code == 200:
                for data in response.json():
                    tmp = {}
                    tmp["title"] = data["title"]
                    tmp["status_id"] = data["status_id"]
                    test_data[data["id"]] = tmp
                return test_data

            else:
                LOG.error(
                    "Failed to get test run ids for {} in TestRail with error code {}".format(
                        run_id, response.status_code
                    )
                )
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def update_result(self, run_id, result_file):
        """Update test results for a TestRail test run.
         "The update in the TestRun is based on the Case ID from the Test Suite,
         as mentioned in the documentation https://support.testrail.com/hc/en-us/articles/7077819312404-Results#addresultsforcases"

        Args:
            run_id (int): ID of the TestRail test run.
            result_file (str): Absolute path of the JSON file containing test results.
        Returns:
            bool: True if the test results were successfully updated, False otherwise.
        """
        try:
            update_result_run_url = (
                f"{self.url}/index.php?/api/v2/add_results_for_cases/{run_id}"
            )

            with open(result_file) as json_file:
                data = json.load(json_file)

            response = requests.post(
                update_result_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data),
            )
            if response.status_code == 200:
                LOG.info(f"Result in Run Id {run_id} got updated.")
                return True
            else:
                LOG.error(
                    "Failed to update result in Run ID {} in TestRail.".format(run_id)
                )
                LOG.error(f"TestRail Response: {response.status_code}")
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def update_result_via_testid(self, run_id, result_file):
        """Update test results for a TestRail test run.
         "The update in the TestRun is based on the TEST ID from the Test Run created from a particular Test Suite,
         as mentioned in the documentation https://support.testrail.com/hc/en-us/articles/7077819312404-Results#addresults"

        Args:
            run_id (int): ID of the TestRail test run.
            result_file (str): Absolute path of the JSON file containing test results.
        Returns:
            bool: True if the test results were successfully updated, False otherwise.
        """
        try:
            update_result_run_url = f"{self.url}/index.php?/api/v2/add_results/{run_id}"

            with open(result_file) as json_file:
                data = json.load(json_file)

            response = requests.post(
                update_result_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data),
            )
            if response.status_code == 200:
                LOG.info(f"Result in Run Id {run_id} got updated.")
                return True
            else:
                LOG.error(
                    "Failed to update result in Run ID {} in TestRail.".format(run_id)
                )
                LOG.error(f"TestRail Response: {response.status_code}")
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def create_testrail_config_file(
        self, suite_id, run_id, run_name, file_path, plan_id, milestone_id
    ):
        """Create a configuration file for TestRail.

        The configuration file will contain the following information:
        - API URL, email, and password
        - Test run details such as project ID, suite ID, run ID, and run name
        - Plan and milestone IDs (if provided)

        Args:
            suite_id: ID of the Test Suite.
            run_id: ID of the Test Run.
            run_name: Name of the Test Run.
            file_path: Absolute path of the configuration file to be created.
            plan_id (Optional): Plan ID.
            milestone_id (Optional): Milestone ID.

        Returns:
            None
        """
        config = configparser.ConfigParser()
        config.add_section("API")
        config.set("API", "url", self.url)
        config.set("API", "email", self.email)
        config.set("API", "password", self.password)
        config.add_section("TESTRUN")
        config.set("TESTRUN", "project_id", str(self.project_id))
        config.set("TESTRUN", "suite_id", str(suite_id))
        config.set("TESTRUN", "run_id", str(run_id))
        config.set("TESTRUN", "run_name", run_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if plan_id is not None:
            config.set("TESTRUN", "#plan_id", str(plan_id))
        if milestone_id is not None:
            config.set("TESTRUN", "#milestone_id", str(milestone_id))
        with open(file_path, "w") as configfile:
            config.write(configfile)

    def get_milestone_id(self, milestone_name):
        """Get milestone ID for the given milestone name.

        Args:
            milestone_name (str): Name of the milestone.

        Returns:
            milestone_id (int or None): ID of the milestone if found, otherwise None.
        """
        try:
            response = requests.get(
                f"{self.url}/index.php?/api/v2/get_milestones/{self.project_id}",
                headers=self.headers,
                auth=(self.email, self.password),
            )
            if response.status_code == 200:
                milestone_id = None
                for milestone in response.json()["milestones"]:
                    if milestone["name"] == milestone_name:
                        milestone_id = milestone["id"]
                return milestone_id
            else:
                LOG.error(f"Failed to get milestone id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def get_plan_id(self, plan_name, milestone_id=None):
        """Get the Test Plan ID for the specified plan name.

        Args:
            plan_name (str): The name of the Test Plan.

        Returns:
            int or None: The Test Plan ID, or None if the request was unsuccessful.
        """
        retry = 2
        try:
            response = requests.get(
                f"{self.url}/index.php?/api/v2/get_plans/{self.project_id}",
                headers=self.headers,
                auth=(self.email, self.password),
            )
            while retry != 0:
                if response.status_code == 200:
                    plan_id = None
                    for plan in response.json()["plans"]:
                        if plan["name"] == plan_name:
                            plan_id = plan["id"]
                    return plan_id
                if milestone_id:
                    response = requests.get(
                        f"{self.url}/index.php?/api/v2/get_plans/{self.project_id}/&milestone_id={milestone_id}",
                        headers=self.headers,
                        auth=(self.email, self.password),
                    )
                retry -= 1
            else:
                LOG.error(f"Failed to get plan id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def get_suite_id(self, suite_name):
        """Get the ID of the Test Suite with the specified name.

        Args:
            suite_name (str): The name of the Test Suite.

        Returns:
            int or None: The ID of the Test Suite if it exists, or None otherwise.

        """
        try:
            response = requests.get(
                f"{self.url}/index.php?/api/v2/get_suites/{self.project_id}",
                headers=self.headers,
                auth=(self.email, self.password),
            )
            if response.status_code == 200:
                suite_id = None
                for suite in response.json():
                    if suite["name"] == suite_name:
                        suite_id = suite["id"]
                return suite_id
            else:
                LOG.error(f"Failed to get suite_id id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def create_milestone(
        self, name, start_on, due_on, description="", parent_id=None, refs=None
    ):
        """Create Milestone in a Project.

        Args:
            name: Name of the Milestone
            start_on: Start date in format "%d-%m-%Y %H:%M:%S"
            due_on: Due date in format "%d-%m-%Y %H:%M:%S"
            description: Description of the milestone.
            parent_id: Id of the parent milestone.
            refs: A comma-separated list of references/requirements
        Returns:
            int or None: The ID of the Milestone OR None..
        """
        try:
            format = "%d-%m-%Y %H:%M:%S"

            LOG.info(f"Checking whether Milestone: {name} exists or not.")
            milestone = self.get_milestone_id(milestone_name=name)
            if milestone is not None:
                return milestone
            data = {"name": name, "description": description}
            if parent_id is not None:
                data["parent_id"] = int(parent_id)
            if refs is not None:
                data["refs"] = refs
            data["due_on"] = int(datetime.strptime(due_on, format).timestamp())
            data["start_on"] = int(datetime.strptime(start_on, format).timestamp())

            response = requests.post(
                f"{self.url}/index.php?/api/v2/add_milestone/{self.project_id}",
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data),
            )
            if response.status_code == 200:
                return response.json()["id"]
            else:
                LOG.error(f"Failed to get suite_id id: {response.status_code}")
                return None
        except ValueError as e:
            LOG.info("Please pass date in '%d-%m-%Y %H:%M:%S' format.")
            LOG.exception(f"Error: {e}")
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def get_run_id(self, run_name):
        """Get the ID of the Test Run.

        Args:
            run_name (str): The name of the Test Run.

        Returns:
            int or None: The ID of the Test Run if it exists, or None otherwise.

        """
        try:
            response = requests.get(
                f"{self.url}/index.php?/api/v2/get_runs/{self.project_id}",
                headers=self.headers,
                auth=(self.email, self.password),
            )
            if response.status_code == 200:
                run_id = None
                for run in response.json()["runs"]:
                    if run["name"] == run_name:
                        run_id = run["id"]
                return run_id
            else:
                LOG.warning(f"Failed to get suite_id id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")


@click.group()
def main():
    """
    Command for creating TestRun and TestPlan in TestRail.
    """


@main.command()
@click.option(
    "--email", required=True, help="Email address of a TestRail User.", type=str
)
@click.option("--url", required=True, help="URL of the TestRail.", type=str)
@click.option("--project_id", required=True, help="TestRail Project ID.", type=str)
@click.option("--suite_id", required=True, help="TestRail Suite ID.", type=str)
@click.option(
    "--milestone_id",
    required=False,
    default=None,
    help="TestRail Milestone ID.",
    type=str,
)
@click.option("--case_ids", default=None, help="(,) separated case ids.", type=str)
@click.option(
    "--run_name",
    default="Automated",
    help="Name of the Run (Date will be auto added in name)",
    type=str,
)
@click.option(
    "--tr_config",
    required=True,
    help="Path where you want to save tr_config file.",
    type=str,
)
@click.option(
    "--password_file",
    required=True,
    help="Full path of file where TestRail API key exist.",
    type=click.Path(exists=True),
)
def create_run(
    email,
    url,
    project_id,
    suite_id,
    run_name,
    case_ids,
    tr_config,
    password_file,
    milestone_id,
):
    """
    Command for creating a Test Run for a Test Suite.
    """

    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    if case_ids is not None:
        case_ids = case_ids.split(",")

    tr = TestRail(
        url=url,
        email=email,
        project_id=project_id,
        password=password,
        tr_config=tr_config,
    )
    status = tr.create_run(
        suite_id=suite_id,
        run_name=run_name,
        case_ids=case_ids,
        milestone_id=milestone_id,
    )
    if status is not None:
        click.echo(status)
        sys.exit(0)
    else:
        click.echo("Failed to create a Test Run.")
        sys.exit(-1)


@main.command()
@click.option(
    "--email", required=True, help="Email address of a TestRail User.", type=str
)
@click.option("--url", required=True, help="URL of the TestRail.", type=str)
@click.option("--project_id", required=True, help="TestRail Project ID.", type=str)
@click.option(
    "--plan_file", required=True, help="Full path of the plan json file.", type=str
)
@click.option(
    "--tr_config",
    required=True,
    help="Path where you want to save tr_config file.",
    type=str,
)
@click.option(
    "--password_file",
    required=True,
    help="Full path of file where TestRail API key exist.",
    type=click.Path(exists=True),
)
def create_plan(email, url, project_id, plan_file, tr_config, password_file):
    """
    Command for creatig a Test Plan.
    """
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        project_id=project_id,
        password=password,
        tr_config=tr_config,
    )
    status = tr.create_plan(plan_file)
    if status is not None:
        click.echo(status)
        sys.exit(0)
    else:
        click.echo("Failed to create a Test Plan.")
        sys.exit(-1)


@main.command()
@click.option(
    "--email", required=True, help="Email address of a TestRail User.", type=str
)
@click.option("--url", required=True, help="URL of the TestRail.", type=str)
@click.option("--plan_id", required=True, help="TestRail Plan ID.", type=str)
@click.option(
    "--plan_file", required=True, help="Full path of the plan json file.", type=str
)
@click.option(
    "--tr_config",
    required=True,
    help="Path where you want to save tr_config file.",
    type=str,
)
@click.option(
    "--password_file",
    required=True,
    help="Full path of file where TestRail API key exist.",
    type=click.Path(exists=True),
)
def update_plan(email, url, plan_id, plan_file, tr_config, password_file):
    """
    Command for creating new test runs in already created plan.
    """

    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(url=url, email=email, password=password, tr_config=tr_config)
    status = tr.update_plan(plan_id, plan_file)
    if status is not None:
        click.echo(status)
        sys.exit(0)
    else:
        click.echo("Failed to create a Test Run.")
        sys.exit(-1)


@main.command()
@click.option(
    "--email", required=True, help="Email address of a TestRail User.", type=str
)
@click.option("--url", required=True, help="URL of the TestRail.", type=str)
@click.option("--run_id", required=True, help="TestRail Run ID.", type=str)
@click.option(
    "--result_file", required=True, help="Full path of the result json file.", type=str
)
@click.option(
    "--password_file",
    required=True,
    help="Full path of file where TestRail API key exist.",
    type=click.Path(exists=True),
)
def update_result(email, url, run_id, result_file, password_file):
    """
    This command is used to update one or more new test results, comments or assigns
    one or more tests (using the case IDs).
    Ideal for test automation to bulk-add multiple test results  in one step.
    """
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(url=url, email=email, password=password)
    status = tr.update_result(run_id, result_file)
    if status is not None:
        click.echo(f"Test Result update to Test Run ID: {run_id}")
        sys.exit(0)
    else:
        click.echo("Failed to update result in Test Run.")
        sys.exit(-1)


if __name__ == "__main__":
    main()
