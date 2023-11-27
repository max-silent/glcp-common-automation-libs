"""
Side Menu page element
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.navigation.locators import (
    ActivateSideMenuSelectors,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class ActivateSideMenu:
    """
    Activate Side Menu page element class
    """

    def __init__(self, page: Page):
        """
        Initialize instance of ADI Side Menu page element
        :param page: page
        """
        log.info("Initialize ADI Side Menu page object")
        self.page = page
        self.pw_utils = PwrightUtils(page)

    def navigate_to_devices(self):
        """Click at 'Devices' menu item at activate side-menu."""
        log.info(f"Playwright: navigate to 'Devices' page via activate side-menu link.")
        self.pw_utils.click_selector(ActivateSideMenuSelectors.DEVICES_TAB_BUTTON)

    def navigate_to_folders(self):
        """Click at 'Folders' menu item at activate side-menu."""
        log.info(f"Playwright: navigate to 'Folders' page via activate side-menu link.")
        self.pw_utils.click_selector(ActivateSideMenuSelectors.FOLDERS_TAB_BUTTON)

    def navigate_to_activate_documentation(self):
        """Click at 'Activate Documentation' menu item at activate side-menu."""
        log.info(
            f"Playwright: navigate to 'Activate Documentation' page via activate side-menu link."
        )
        self.pw_utils.click_selector(ActivateSideMenuSelectors.DOCUMENTATION_TAB_BUTTON)
