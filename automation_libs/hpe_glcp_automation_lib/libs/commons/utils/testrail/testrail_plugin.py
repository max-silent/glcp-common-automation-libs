import ast
import logging
from datetime import datetime
from pathlib import Path

import pytest

from hpe_glcp_automation_lib.libs.commons.utils.slack.slack_utils import SlackNotification
from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail import PyTestRail

RESULTS_FILENAME = "test_execution_results.txt"
log = logging.getLogger(__name__)


class PyTestRailPlugin(object):
    """
    This Pytest plugin for TestRail is designed to capture test results and report
    them to TestRail. In your conftest.py, add the following:

    :example:
    from hpe_glcp_automation_lib.libs.commons.utils.testrail_plugin import PyTestRailPlugin
    def pytest_configure(config):
        config.pluginmanager.register(PyTestRailPlugin(testrail_configs))

    :note: For more info about the testrail_configs dictionary and the Pytest-TestRail
    workflow, refer to
    https://hpe.atlassian.net/wiki/spaces/GST/pages/2083754495/TestRail+User+Guide
    """

    def __init__(
        self,
        testrail_configs,
        username=None,
        password=None,
        base_url=None,
        notify_slack=False,
    ):
        self.configs = testrail_configs
        self.username = username
        self.password = password
        self.base_url = base_url
        self.notify_slack = notify_slack

    def pytest_sessionstart(self, session):
        session.results = dict()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        result = outcome.get_result()
        comment = result.longrepr  # dump stack trace on failure

        if result.when in ["call", "setup"]:
            markers = item.iter_markers(name="testrail")
            tids = []

            for mark in markers:
                if result.when == "setup":
                    if result.outcome != "skipped":
                        continue
                val = mark.kwargs["id"]
                if isinstance(val, list):
                    for x in val:
                        tids.append(x)
                else:
                    tids.append(val)

            for tid in tids:
                if (
                    tid in item.session.results
                    and item.session.results[tid][0].outcome == "failed"
                ):
                    pass
                else:
                    item.session.results[tid] = (result, tid, comment)

            # Dumping results in case of chained cli execution
            previous_results = self.read_results_file()
            with open(RESULTS_FILENAME, "w") as test_results_file:
                previous_results.update(PyTestRail.prepare_results(item.session.results))
                test_results_file.write(
                    str(previous_results)
                )  # String conversion done because json package
                # does not allow using integer as a key

    def pytest_sessionfinish(self, session, exitstatus):
        tr = PyTestRail(self.username, self.password, self.base_url)
        results = self.read_results_file() or PyTestRail.prepare_results(session.results)
        tr.testrail_upload_pytest_results(results, self.configs)
        if self.notify_slack:
            slack = SlackNotification()
            slack.send_notification(
                name=self.configs["test_run"],
                date=(datetime.now()).strftime("%B %d, %Y %H:%M:%S"),
                data=results,
            )

    @staticmethod
    def read_results_file():
        if Path(RESULTS_FILENAME).resolve().exists():
            try:
                file_content = Path(RESULTS_FILENAME).resolve().read_text()
                return ast.literal_eval(file_content)
            except SyntaxError:
                log.error(
                    f"Unable to parse {RESULTS_FILENAME} file, using empty dictionary. File content: \n{file_content}"
                )
                return dict()
        log.debug(f"File {RESULTS_FILENAME} does not exist, using empty dictionary.")
        return dict()
