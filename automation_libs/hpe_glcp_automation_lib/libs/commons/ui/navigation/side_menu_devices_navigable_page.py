import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.elem_devices_side_menu import (
    DevicesSideMenu,
)

log = logging.getLogger(__name__)


class SideMenuNavigablePage(BasePage):
    """
    Devices Side Menu Navigable page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Devices Side Menu Navigable page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Devices Side Menu Navigable page object.")
        super().__init__(page, cluster)
        self.page = page
        self.side_menu = DevicesSideMenu(page)
