"""
Support Online Help page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.support_assistant.ui.locators import BillingSelectors

log = logging.getLogger(__name__)


class BillingAndSubscription(BasePage):
    def __init__(self, page: Page):
        """
        Online Support Help page object model class
        """
        log.info("Initialize Online Support Center page object.")
        self._base_url = "https://h41390.www4.hpe.com"
        super().__init__(page, self._base_url)
        self.url = f"{self._base_url}/support/index.html?form=osqbm"

    def should_have_heading_text(self, text):
        """
        verify heading loads for the support page
        :param text: expected text of title.
        :return: current instance of BillingAndSubscription page object.
        """
        log.info(f"Check for '{text}' text in the page title.")
        expect(
            self.page.locator(BillingSelectors.PAGE_HEADING_TEMPLATE.format(text))
        ).to_be_visible(timeout=60000)
        return self
