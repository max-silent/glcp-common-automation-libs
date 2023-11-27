"""
Base Page for page object model
"""
import logging
import os

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.locators import BasePageSelectors
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class BasePage:
    """
    Base Page for page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        self.test_name = (
            os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
        )
        self.pw_utils = PwrightUtils(page)
        self.page = page
        self.cluster = cluster
        self.url = None

    def open(self):
        """
        Navigating to page url
        :return: instance of current page object
        """
        if not self.url:
            raise Exception("URL was not specified.")
        self.page.goto(self.url)
        self.pw_utils.wait_for_url(f"{self.url}", timeout_ignore=True, timeout=20000)
        current_url = self.page.url
        if not current_url == self.url:
            log.error("Unexpected URL")
            self.pw_utils.save_screenshot(self.test_name)
            raise Exception(
                f"Wrong page opened instead of expected '{self.url.split('/')[-1]}': '{current_url}'"
            )
        return self

    def wait_for_loaded_state(self):
        """
        Wait till page is loaded and loading spinner is not present
        :return: instance of current page object
        """
        self.page.wait_for_url(self.url)
        self.page.locator(BasePageSelectors.APP_LOADER).wait_for(state="hidden")
        self.pw_utils.wait_for_selector(
            BasePageSelectors.LOADER_SPINNER,
            state="visible",
            timeout_ignore=True,
            timeout=5000,
        )
        self.page.locator(BasePageSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def close_notification_banner(self):
        """
        Click at notification banner's close button.
        :return: instance of current page object.
        """
        log.info(
            "Playwright: click at notification banner's close button and wait for completion."
        )
        with self.page.expect_request_finished(
            predicate=lambda request: "notifications-svc/ui/v1alpha1/notifications"
            in str(request.url)
            and request.method == "PATCH"
        ):
            self.page.locator(BasePageSelectors.BANNER_NOTIF_CLOSE_BTN).click()
        return self

    def should_contain_notification_banner_text(self, text, timeout=180000):
        """
        Check that expected text is contained at notification banner.
        :param text: expected text to be contained.
        :param timeout: timeout for expected text to appear.
        :return: instance of current page object.
        """
        log.info(f"Playwright: check notification banner contains text: '{text}'.")
        expect(self.page.locator(BasePageSelectors.BANNER_NOTIFICATION)).to_contain_text(
            text, timeout=timeout
        )
        return self

    def should_have_page_title(self, text):
        """
        Check that current page's title match to expected text.
        :param text: expected title text.
        :return: instance of current page object
        """
        log.info(f"Playwright: Verifying page title with text {text}")
        self.page.wait_for_load_state()
        expect(self.page).to_have_title(text)
        return self
