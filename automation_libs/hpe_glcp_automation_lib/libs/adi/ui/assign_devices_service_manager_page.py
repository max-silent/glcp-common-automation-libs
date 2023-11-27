"""
Assign Devices to Service Manager page object model
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.adi.ui.locators import AssignDeviceToServiceManager
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class AssignDevicesToServiceManager(HeaderedPage):
    """
    Assign Devices to Service Manager page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Assign Devices to Service Manager page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Assign Devices to Service Manager page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/devices/inventory/assign-to-application"

    def assign_device_to_service_manager_instance(self, service_manager, region_name):
        """
        Assigns the device to service_manager and closes the Assign to Service Manager pop-up
        :params: service_manager: service manager to be selected from dropdown
        :params: region_name: region manager to be selected from dropdown
        :returns: self reference
        """
        self.pw_utils.select_drop_down_element(
            drop_menu_selector=AssignDeviceToServiceManager.SERVICE_MANAGER_DROPDOWN,
            element=service_manager,
            element_role="option",
            exact_match=True,
        )

        self.pw_utils.select_drop_down_element(
            drop_menu_selector=AssignDeviceToServiceManager.REGION_DROPDOWN,
            element=region_name,
            element_role="option",
            exact_match=True,
        )
        self.page.locator(AssignDeviceToServiceManager.FINISH_BTN).click()
        self.page.locator(AssignDeviceToServiceManager.CLOSE_BTN).click()
        return self
