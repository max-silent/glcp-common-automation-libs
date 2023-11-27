"""
Roles page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.cds.ui.locators import UsageReportingSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class Usage_Reporting(HeaderedPage):
    """
    Usage Reporting page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Usage reporting page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Usage Reporting page object")
        super().__init__(page, cluster)
        cluster = "https://mira.ccs.arubathena.com"
        self.url = f"{cluster}/manage-account/consumption-reporting"

    def open_cds_page(self):
        """
        Navigate to usage reporting  by url
        :return: current instance of page object
        """
        log.info("Open Usage Reporting page by navigating to url.")
        self.page.goto(self.url)
        self.pw_utils.wait_for_selector(
            UsageReportingSelectors.USAGEREPORTING, timeout_ignore=True, timeout=10000
        )
        if self.page.locator(UsageReportingSelectors.USAGEREPORTING).count() < 2:
            self.pw_utils.wait_for_url(
                f"{self.cluster}/home", timeout_ignore=True, timeout=20000
            )
        return self

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of Usage Reporting page object.
        """
        log.info(
            f"Playwright: check that title has text '{text}' in My Usage Reporting page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(UsageReportingSelectors.HEADING_PAGE_TITLE)
        ).to_have_text(text)
        return self

    def search_for_text(self, search_text):
        """
        Enter text to search field.
        :param search_text: search_text.
        :return: current instance of Usage Reporting page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' in Usage Reporting Page.")
        self.pw_utils.enter_text_into_element(
            UsageReportingSelectors.SEARCH_FIELD, search_text
        )
        self.wait_for_loaded_table()
        return self
