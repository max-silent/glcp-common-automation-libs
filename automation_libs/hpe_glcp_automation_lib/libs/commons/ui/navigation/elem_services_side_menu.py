"""
Side Menu page element
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.locators import (
    ServicesSideMenuSelectors,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class ServicesSideMenu:
    """
    Services Side Menu page element class
    """

    def __init__(self, page: Page):
        """Initialize instance of Services Side Menu page element.
        :param page: page
        """
        log.info("Initialize Services Side Menu page object.")
        self.page = page
        self.pw_utils = PwrightUtils(page)

    def navigate_to_my_services(self):
        """Navigate to my-services page."""
        log.info(
            f"Playwright: navigate to 'My Services' page via services side-menu link."
        )
        self.pw_utils.click_selector(ServicesSideMenuSelectors.MY_SERVICES_TAB)

    def navigate_to_subscriptions(self):
        """Navigate to service-subscriptions page."""
        log.info(
            f"Playwright: navigate to 'Service Subscriptions' page via services side-menu link."
        )
        self.pw_utils.click_selector(ServicesSideMenuSelectors.SUBSCRIPTIONS_TAB)

    def navigate_to_catalog(self):
        """Navigate to service-catalog page."""
        log.info(
            f"Playwright: navigate to 'Service Catalog' page via services side-menu link."
        )
        self.pw_utils.click_selector(ServicesSideMenuSelectors.SERVICE_CATALOG)

    def should_have_side_menu_tab(self, text):
        """Check that side-menu item with expected text is present at the page.

        :param text: expected text to match with the text in side-menu tab.
        """
        log.info(f"Playwright: check that side-menu contains tab with '{text}' text.")
        expect(
            self.page.locator(
                ServicesSideMenuSelectors.SIDE_MENU_TAB_TEMPLATE.format(text)
            )
        ).to_be_visible()
