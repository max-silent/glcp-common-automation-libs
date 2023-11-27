"""
Launched Service Page Model
"""
import logging
import os
from functools import wraps

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.services.ui.locators import LaunchedServiceSelectors

log = logging.getLogger(__name__)


def _screenshot_on_failure(func):
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        try:
            return func(obj, *args, **kwargs)
        except Exception:
            obj.pw_utils.save_screenshot(obj.test_name)
            raise

    return wrapper


class LaunchedService:
    """
    Class for page with launched service.
    """

    def __init__(self, page: Page):
        """
        Initialize Launched Service page.
        :param page: Page
        """
        log.info("Initialize LaunchedService page object.")
        self.test_name = (
            os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
        )
        self.pw_utils = PwrightUtils(page)
        self.page = page

    @_screenshot_on_failure
    def wait_for_url(self, url):
        """Wait for expected URL of current page.

        :param url: expected URL.
        :return: current instance of LaunchedService page object.
        """
        log.info(f"Playwright: Wait for expected URL: '{url}'.")
        self.page.wait_for_url(url)
        return self

    @_screenshot_on_failure
    def should_have_page_title(self, title):
        """Check that current page's title match to expected text.

        :param title: expected title text.
        :return: current instance of LaunchedService page object.
        """
        log.info(f"Playwright: Check browser page's title.")
        expect(self.page).to_have_title(title)
        return self

    @_screenshot_on_failure
    def should_have_element_with_text(self, text):
        """Check that current page contains any element with expected text.

        :param text: expected text of the element.
        :return: current instance of LaunchedService page object.
        """
        log.info(f"Playwright: Check that page contains element with expected text.")
        expect(
            self.page.locator(
                LaunchedServiceSelectors.TEXT_ELEMENT_TEMPLATE.format(text)
            ).first
        ).to_be_visible()
        return self

    @_screenshot_on_failure
    def should_have_button_with_text(self, text):
        """Check that there is a button with expected text at current page.

        :param text: expected text of the button.
        :return: current instance of LaunchedService page object.
        """
        log.info(f"Playwright: Check that page contains button with expected text.")
        expect(
            self.page.locator(
                LaunchedServiceSelectors.TEXT_BUTTON_TEMPLATE.format(text)
            ).first
        ).to_be_visible()
        return self
