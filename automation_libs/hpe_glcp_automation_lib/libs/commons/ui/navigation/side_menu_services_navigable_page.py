import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.elem_services_side_menu import (
    ServicesSideMenu,
)

log = logging.getLogger(__name__)


class SideMenuNavigablePage(BasePage):
    """
    Services Side Menu Navigable page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Services Side Menu Navigable page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Services Side Menu Navigable page object.")
        super().__init__(page, cluster)
        self.page = page
        self.side_menu = ServicesSideMenu(page)
