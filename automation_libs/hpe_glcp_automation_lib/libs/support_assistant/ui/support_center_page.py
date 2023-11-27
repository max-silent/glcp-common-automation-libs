"""
Support Online Help page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.support_assistant.ui.locators import (
    SupportCenterSelectors,
)

log = logging.getLogger(__name__)


class SupportCenter(BasePage):
    def __init__(self, page: Page):
        """
        Online Support Help page object model class
        """
        log.info("Initialize Online Support Center page object.")
        self._base_url = "https://support.hpe.com"
        super().__init__(page, self._base_url)
        self.url = f"{self._base_url}/hpesc/public/docDisplay?docId=a00120892en_us"

    def wait_for_loaded_state(self):
        """Wait till page is loaded and loading spinner is not present.
        :return: current instance of SupportCenter page object.
        """
        self.page.wait_for_url(self.url)
        self.pw_utils.wait_for_selector(
            SupportCenterSelectors.PAGE_LOADER,
            state="visible",
            timeout_ignore=True,
            timeout=10000,
        )
        self.page.locator(SupportCenterSelectors.PAGE_LOADER).wait_for(state="hidden")
        self.page.locator(SupportCenterSelectors.LINKS_LOADER).wait_for(state="hidden")
        return self

    def should_have_title(self):
        """Verify expected title is present at page.
        :return: current instance of SupportCenter page object.
        """
        log.info("Playwright: check displayed user guide title at Documentation page.")
        expect(self.page.locator(SupportCenterSelectors.USER_GUIDE_TITLE)).to_be_visible()
        return self

    def should_have_documentation_navigation_links(self):
        """Verify Documentation's page navigation links are present at page.
        :return: current instance of SupportCenter page object.
        """
        log.info("Playwright: check displayed navigation links at Documentation page.")
        expect(
            self.page.locator(SupportCenterSelectors.WELCOME_HPE_GLE_ETC_PLATFORM)
        ).to_be_visible()
        expect(
            self.page.locator(SupportCenterSelectors.DASHBOARD_DOCUMENT)
        ).to_be_visible()
        expect(
            self.page.locator(SupportCenterSelectors.APPLICATIONS_DOCUMENT)
        ).to_be_visible()
        expect(self.page.locator(SupportCenterSelectors.DEVICES_DOCUMENT)).to_be_visible()
        expect(self.page.locator(SupportCenterSelectors.MANAGE_DOCUMENT)).to_be_visible()
        expect(
            self.page.locator(SupportCenterSelectors.DOCUMENTATION_FEEDBACK)
        ).to_be_visible()
        return self
