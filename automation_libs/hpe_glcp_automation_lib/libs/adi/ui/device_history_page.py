"""
Device History page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.adi.ui.activate_device_details_page import (
    ActivateDeviceDetails,
)

log = logging.getLogger(__name__)


class DeviceHistory(ActivateDeviceDetails):
    """
    Device History page object model class.
    """

    def __init__(self, page: Page, cluster: str, serial_number: str):
        """
        Initialize Device History page object.
        :param page: page.
        :param cluster: cluster url.
        :param serial_number: device serial number.
        """
        log.info("Initialize Device History page object")
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'DeviceHistory()' by 'ActivateDeviceDetails()'."
        )
        super().__init__(page, cluster, serial_number)
