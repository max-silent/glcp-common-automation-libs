"""
Devices side Menu page element.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.navigation.locators import (
    DevSideMenuSelectors,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class DevicesSideMenu:
    """
    Devices Side Menu page element class.
    """

    def __init__(self, page: Page):
        """Initialize instance of Devices Side Menu page element.

        :param page: page
        """
        log.info("Initialize Devices Side Menu page object")
        self.page = page
        self.pw_utils = PwrightUtils(page)

    def navigate_to_inventory(self):
        """Click at 'Inventory' menu item at devices side-menu."""
        log.info(f"Playwright: navigate to 'Inventory' page via devices side-menu link.")
        self.pw_utils.click_selector(DevSideMenuSelectors.DEVICES_TAB_BUTTON)

    def navigate_to_tags(self):
        """Click at 'Tags' menu item at devices side-menu."""
        log.info(f"Playwright: navigate to 'Tags' page via devices side-menu link.")
        self.pw_utils.click_selector(DevSideMenuSelectors.TAGS_TAB_BUTTON)

    def navigate_to_dev_subscriptions(self):
        """Click at 'Device Subscriptions' menu item at devices side-menu."""
        log.info(
            f"Playwright: navigate to 'Device Subscriptions' page via devices side-menu link."
        )
        self.pw_utils.click_selector(DevSideMenuSelectors.SUBSCRIPTIONS_TAB_BUTTON)

    def navigate_to_auto_subscribe(self):
        """Click at 'Auto-Subscribe' menu item at devices side-menu."""
        log.info(
            f"Playwright: navigate to 'Auto-Subscribe' page via devices side-menu link."
        )
        self.pw_utils.click_selector(DevSideMenuSelectors.AUTO_SUBSCRIBE_TAB_BUTTON)
