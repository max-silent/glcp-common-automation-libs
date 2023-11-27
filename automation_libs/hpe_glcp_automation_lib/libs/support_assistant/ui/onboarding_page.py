"""
Support Online Help page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.support_assistant.ui.locators import OnBoardingSelectors

log = logging.getLogger(__name__)


class OnBoardingPage(BasePage):
    def __init__(self, page: Page):
        """
        OnBoarding User Workspace page object model class
        """
        log.info("Initialize OnBoarding User Workspace page object.")
        self._base_url = "https://h41390.www4.hpe.com/support/index.html?form=glsupport"
        super().__init__(page, self._base_url)
        self.url = f"{self._base_url}/support/index.html?form=osqbm"

    def should_have_heading_text(self):
        """
        verify heading loads for the OnBoardingPage page
        :return: current instance of OnBoardingPage page object.
        """
        log.info(f"Check for title visible on page")
        expect(self.page.locator(OnBoardingSelectors.PAGE_HEADING_TITLE)).to_be_visible()
        return self
