"""
Order History page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import OrderHistorySelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class OrderHistory(HeaderedPage):
    """
    Order History page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Order History page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/subscriptions/order-history"

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of Order History page object.
        """
        log.info("Playwright: check that title has matched text in Order History page.")
        expect(self.page.locator(OrderHistorySelectors.PAGE_TITLE)).to_be_visible()
        return self
