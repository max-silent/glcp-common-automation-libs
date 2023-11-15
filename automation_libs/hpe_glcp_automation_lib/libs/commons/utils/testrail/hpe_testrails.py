import logging
import os
import re

from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import Settings
from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_defines import (
    TestRailError,
    TestRailResult,
)
from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_utils import (
    TestRailUtils,
)

LOG = logging.getLogger(__name__)

# Put here all defined entries
TESTRAIL_BASE_URL = "https://testrail.glcp.hpedev.net/"
DEFAULT_PROJECT = "GLCP"
PYTEST_RESULTS = {}


class HPETestRails(TestRailUtils):
    def __init__(self, username=None, password=None, base_url=None):
        self.username = username or os.getenv("TR_USERNAME")
        self.password = password or os.getenv("TR_PASSWORD")

        if self.username is None or self.password is None:
            # Attempt to get creds from S3 bucket or local cred file.
            tr_creds = Settings.download_tr_creds()
            self.username = tr_creds["API"]["user"]
            self.password = tr_creds["API"]["password"]

        if base_url is None:
            base_url = TESTRAIL_BASE_URL

        super().__init__(self.username, self.password, base_url, DEFAULT_PROJECT)

    def discover_hpe_child_milestone(self, testrail_configs):
        child_milestone = testrail_configs["child_milestone"] or "UndefTestType"
        if re.match(r"false", os.getenv("TR_RESULT_POPULATE", "true"), re.IGNORECASE):
            LOG.info("Env TR_RESULT_POPULATE is false. Don't upload results to TestRail.")
            return
        elif child_milestone == "UndefTestType":
            LOG.info(
                "Sub-milestone is 'UndefTestType'. Don't upload results to TestRail."
            )
            return
        return child_milestone

    def setup_hpe_project_id(self, testrail_configs):
        if "project" not in testrail_configs or not testrail_configs["project"]:
            project_name = self.default_project
        else:
            project_name = testrail_configs["project"]
        project_id = self.get_project_id(project_name)
        LOG.info(f"  Project: {project_name}, id: {project_id}")
        return project_id

    def setup_milestones(self, testrail_configs, child_milestone, project_id):
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
        return milestone_id

    def setup_suites(self, testrail_configs, project_id):
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
        return suite_id

    def setup_plan(self, testrail_configs, project_id, milestone_id):
        # Get test plan id, add plan if it doesn't exist
        plan_id = self.get_plan_id(
            project_id, milestone_id, testrail_configs["test_plan"]
        )
        if plan_id == 0:
            plan_id = self.add_plan(
                project_id, milestone_id, testrail_configs["test_plan"]
            )
        LOG.info(f"  Test Plan: {testrail_configs['test_plan']}, id: {plan_id}")
        return plan_id

    def setup_plan_runid(self, testrail_configs, plan_id, suite_id, valid_tc_ids):
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
        return run_id

    def testrail_upload_pytest_results(self, results, testrail_configs):
        child_milestone = self.discover_hpe_child_milestone(testrail_configs)
        if child_milestone is None:
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
        project_id = self.setup_hpe_project_id(testrail_configs)

        milestone_id = self.setup_milestones(
            testrail_configs, child_milestone, project_id
        )

        suite_id = self.setup_suites(testrail_configs, project_id)

        plan_id = self.setup_plan(testrail_configs, project_id, milestone_id)

        # Check for invalid tests case IDs
        all_tc_ids = [case for case in self.get_cases_data(project_id, suite_id).keys()]
        invalid_tc_ids = list(set(tc_ids) - set(all_tc_ids))
        valid_tc_ids = list(set(tc_ids) - set(invalid_tc_ids))

        run_id = self.setup_plan_runid(testrail_configs, plan_id, suite_id, valid_tc_ids)

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

    def testrail_create_plan_run_robot(self, testrail_configs):
        child_milestone = self.discover_hpe_child_milestone(testrail_configs)
        if child_milestone is None:
            return

        # If tc_ids list is populated,
        #   then show executed tests vs expected tests
        #   else show executed tests
        if testrail_configs["tc_ids"]:
            tc_ids = testrail_configs["tc_ids"]

        if not tc_ids:
            LOG.info(
                "TestRail markers are not defined. Don't upload results to TestRail."
            )
            return

        LOG.info("Uploading results to TestRail...")
        project_id = self.setup_hpe_project_id(testrail_configs)

        milestone_id = self.setup_milestones(
            testrail_configs, child_milestone, project_id
        )

        suite_id = self.setup_suites(testrail_configs, project_id)

        plan_id = self.setup_plan(testrail_configs, project_id, milestone_id)

        run_id = self.setup_plan_runid(testrail_configs, plan_id, suite_id, tc_ids)

        return plan_id, run_id
