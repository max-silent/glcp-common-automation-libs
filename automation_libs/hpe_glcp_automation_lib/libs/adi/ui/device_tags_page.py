import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import DeviceTagSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_devices_navigable_page import (
    SideMenuNavigablePage,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class DeviceTags(HeaderedPage, SideMenuNavigablePage):
    """
    Device Tags page element class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize instance of Devices Tags page
        :param page: page.
        :param cluster: cluster url.
        """

        log.info("Initialize Devices Tags page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/devices/tags"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page
        :return: current instance of customers page object
        """
        self.page.wait_for_selector(
            DeviceTagSelectors.TAGS_TABLE_ROWS, state="visible", strict=False
        )
        self.page.locator(DeviceTagSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_tags(self, name):
        """
        Search for tags
        NOTE: Currently tag search does not work, due to bug: GLCP-124220.
        :param: name
        :returns : list of table rows indices
        """
        self.pw_utils.enter_text_into_element(DeviceTagSelectors.SEARCH_FIELD, name)
        self.wait_for_loaded_table()
        return self

    def click_resource_by_row_num(self, tag_name):
        """
        Click on the dropdown 'Resources' item for the specified row number.
        NOTE: may not work for some items, due to bug: GLCP-124224.
        :param tag_name: row number to select
        :returns: None
        """
        self.page.locator(
            DeviceTagSelectors.ACTIONS_MENU_TEMPLATE.format(tag_name)
        ).first.click()
        self.page.locator(DeviceTagSelectors.VIEW_RESOURCES_OPTION).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_all_tag_name(self, tag_name):
        """
        verify the table only have rows for tag_name passed .
        :param tag_name: tag_name to check for
        :returns: None
        """
        log.info(f"Verifying the tag table only have rows for tag name {tag_name}")
        for element in self.page.locator(DeviceTagSelectors.TAGS_TABLE_NAME_COLS).all():
            expect(element).to_contain_text(tag_name)
