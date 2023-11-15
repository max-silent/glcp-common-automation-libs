import logging
import time

from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_base import (
    TestRailBase,
    TestRailError,
)
from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_defines import (
    TestRailResult,
)

LOG = logging.getLogger(__name__)


class TestRailUtils(TestRailBase):
    def __init__(self, username, password, base_url, default_project):
        self.username = username
        self.password = password
        self.default_project = default_project

        if self.username is None or self.password is None or default_project is None:
            raise TestRailError(
                "TestRail API requires username, password and default_project"
            )

        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url

        super().__init__(username, password, base_url)

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
        self.default_project).
        """
        if project_id is None:
            project_id = self.get_project_id(self.default_project)
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
            # Look up the current milestone in default project by comparing
            # the current time with the start/end times in the project milestones,
            # but skipping completed milestones and milestones with undefined
            # start/end times.

            current_time = time.time()

            default_project_id = self.get_project_id(self.default_project)
            if default_project_id != project_id:
                raise TestRailError(
                    f"TestRail API requires milestone unless project is {self.default_project}"
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
                    f" {self.default_project}"
                )
            elif len(match_list) > 1:
                LOG.info(
                    f"WARNING: Found multiple current milestones"
                    f" {[x['name'] for x in match_list]}"
                    f" in project {self.default_project}. Use the first match."
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
