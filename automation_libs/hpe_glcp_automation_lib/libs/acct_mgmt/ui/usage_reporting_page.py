"""
usage reporting page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import UsageReportingSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class UsageReporting(HeaderedPage):
    """
    usage reporting page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize usage reporting page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/consumption-reporting"

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of usage reporting page object.
        """
        log.info("Playwright: check that title has matched text in usage reporting page.")
        expect(self.page.locator(UsageReportingSelectors.PAGE_TITLE)).to_be_visible()
        return self
