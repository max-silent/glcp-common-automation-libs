"""
Navigation bar page element
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.service_centric_ui.locators import (
    NavBarSelectors,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class NavigationBar:
    """
    Navigation bar page element class
    """

    def __init__(self, page: Page):
        """
        Initialize instance of page navigation
        :param page: page
        """
        self.pw_utils = PwrightUtils(page)
        self.page = page

    def navigate_to_home(self):
        """
        Navigate to dashboard home page.
        """
        log.info("Navigate to dashboard home page.")
        self.pw_utils.click_selector(NavBarSelectors.MENU_BTN_HOME)

    def navigate_to_services(self):
        """
        Navigate to services page.
        """
        log.info("Navigate to services page.")
        self.pw_utils.click_selector(NavBarSelectors.MENU_BTN_SERVICES)

    def navigate_to_devices(self):
        """
        Navigate to devices page.
        """
        log.info("Navigate to devices page.")
        self.pw_utils.click_selector(NavBarSelectors.MENU_BTN_DEVICES)

    def navigate_to_customers(self):
        """
        Navigate to customers page in case of MSP
        """
        log.info("Navigate to customers page")
        self.pw_utils.click_selector(NavBarSelectors.MENU_BTN_CUSTOMERS)
