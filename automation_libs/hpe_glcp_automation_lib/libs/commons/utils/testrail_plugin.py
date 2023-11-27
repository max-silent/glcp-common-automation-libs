import pytest

from hpe_glcp_automation_lib.libs.commons.utils.testrail import PyTestRail


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

    def __init__(self, testrail_configs, username=None, password=None, base_url=None):
        self.configs = testrail_configs
        self.username = username
        self.password = password
        self.base_url = base_url

    def pytest_sessionstart(self, session):
        session.results = dict()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        result = outcome.get_result()
        comment = result.longrepr  # dump stack trace on failure
        tid = 0

        if result.when == "call":
            markers = item.iter_markers(name="testrail")
            for mark in markers:
                tid = mark.kwargs["id"]
            item.session.results[item] = (result, tid, comment)

    def pytest_sessionfinish(self, session, exitstatus):
        tr = PyTestRail(self.username, self.password, self.base_url)
        # tr = PyTestRail()
        tr.testrail_upload_pytest_results(session, self.configs)
