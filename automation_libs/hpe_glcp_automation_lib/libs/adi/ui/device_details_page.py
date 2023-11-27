import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import DeviceDetailsSelectors
from hpe_glcp_automation_lib.libs.audit_logs.ui.audit_logs_page import AuditLogs
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class DeviceDetails(HeaderedPage):
    """
    Selected device's details page object model
    """

    def __init__(self, page: Page, cluster: str, serial: str):
        """
        Initialize with page, cluster and device serial
        :param page: Page.
        :param cluster: cluster under test url.
        :param serial: serial number of opened device's details.
        """
        log.info(f"Playwright: Initialize device details page for '{serial}'.")
        super().__init__(page, cluster)
        self.url = f"{cluster}/devices/inventory/{serial}"

    def go_back_to_devices(self):
        log.info("Playwright: navigating back to devices list.")
        self.page.locator(DeviceDetailsSelectors.DEVICES_BTN).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def get_application_instance(self):
        """Get Application Instance at device details page.
        :return: Application Instance value
        """
        log.info(f"Playwright: get application instance value at device details page")
        return self.page.locator(DeviceDetailsSelectors.APP_INSTANCE_VALUE).text_content()

    def remove_assignment(self):
        """Remove Application Assignment form the device.
        :return: current instance of Device Details page object.
        """
        log.info("Playwright: click 'Remove Assignment' button.")
        self._open_actions()
        self.page.locator(DeviceDetailsSelectors.REMOVE_ASSIGNMENT).click()
        self.page.locator(DeviceDetailsSelectors.REMOVE_APP_ASSIGNMENT).click()
        self.wait_for_loaded_state()
        return self

    def archive_device(self):
        """Archive a device.
        :return: current instance of Device Details page object.
        """
        log.info("Playwright: Archive a device.")
        self._open_actions()
        self.page.locator(DeviceDetailsSelectors.ARCHIVE_BTN).click()
        self.page.locator(DeviceDetailsSelectors.ARCHIVE_CONFIRM_BTN).click()
        self.wait_for_loaded_state()
        return self

    def unarchive_device(self):
        """Un-archive a device.
        :return: current instance of Device Details page object.
        """
        log.info("Playwright: Un-archive a device.")
        self._open_actions()
        self.page.locator(DeviceDetailsSelectors.UNARCHIVE_BTN).click()
        self.page.locator(DeviceDetailsSelectors.ARCHIVE_CONFIRM_BTN).click()
        self.wait_for_loaded_state()
        return self

    def click_popup_cancel_button(self):
        """Close a dialog by clicking 'Cancel' popup button.
        :return: current instance of Device Details page object.
        """
        log.info("Playwright: Close a dialog by clicking 'Cancel' button.")
        self.page.locator(DeviceDetailsSelectors.CANCEL_BTN).click()
        return self

    def view_audit_logs_after_action(self):
        """Click 'View Audit Logs' on after-action popup.
        :return: Audit Log page object.
        """
        log.info("Playwright: Close a dialog.")
        self.page.locator(DeviceDetailsSelectors.VIEW_AUDIT_LOG_BTN).click()
        return AuditLogs(self.page, self.cluster)

    def should_be_available_for_assignment(self):
        """Check if device is available for assignment.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check if device is available for assign at device details page"
        )
        self._open_actions()
        expect(
            self.page.locator(DeviceDetailsSelectors.ASSIGN_APPLICATION_BTN)
        ).to_have_text("Assign to Application")
        return self

    def should_be_available_for_archiving(self):
        """Check if device is available for archiving.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check if device is available for archive at device details page"
        )
        self._open_actions()
        expect(self.page.locator(DeviceDetailsSelectors.ARCHIVE_BTN)).to_be_visible()
        return self

    def should_be_available_for_unarchiving(self):
        """Check if device is available for un-archiving.

        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check if device is available for un-archive at device details page"
        )
        self._open_actions()
        expect(self.page.locator(DeviceDetailsSelectors.UNARCHIVE_BTN)).to_be_visible()
        return self

    def should_have_mac_address(self, mac_addr):
        """Check displayed MAC-address at device details page.

        :param mac_addr: expected value of MAC-address.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check that device has correct MAC-address '{mac_addr}' at device details page."
        )
        expect(self.page.locator(DeviceDetailsSelectors.MAC_ADDRESS_VALUE)).to_have_text(
            mac_addr
        )
        return self

    def should_have_serial(self, serial):
        """Check displayed serial number at device details page.

        :param serial: expected value of serial number.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check that device has correct serial number '{serial}' at device details page."
        )
        expect(
            self.page.locator(DeviceDetailsSelectors.SERIAL_NUMBER_VALUE)
        ).to_have_text(serial)
        return self

    def should_have_part_no(self, part_no):
        """Check displayed part number at device details page.

        :param part_no: expected value of part number.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check that device has correct part number '{part_no}' at device details page."
        )
        expect(self.page.locator(DeviceDetailsSelectors.PART_NUMBER_VALUE)).to_have_text(
            part_no
        )
        return self

    def should_have_subscription_key(self, lic_key):
        """Check displayed subscription key at device details page.

        :param lic_key: expected value of subscription key.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check that device has correct license key '{lic_key}' at device details page."
        )
        expect(
            self.page.locator(DeviceDetailsSelectors.SUBSCRIPTION_KEY_VALUE)
        ).to_have_text(lic_key)
        return self

    def should_not_have_subscription_key(self, lic_key):
        """Check displayed subscription key at device details page.

        :param lic_key: value of subscription key to become detached from device.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check that device does not have license key '{lic_key}' at device details page."
        )
        expect(
            self.page.locator(DeviceDetailsSelectors.SUBSCRIPTION_KEY_VALUE)
        ).not_to_have_text(lic_key)
        return self

    def should_have_tag(self, tag_name, tag_value=None):
        """Check displayed assigned tag at device details page.

        :param tag_name: expected tag.
        :param tag_value: expected value of specified tag.
        :return: current instance of Device Details page object.
        """
        log.info(
            f"Playwright: check that device has expected tag '{tag_name}' with value '{tag_value}'."
        )
        expected_text_value = f"{tag_name} : {tag_value}" if tag_value else tag_name
        expect(
            self.page.locator(
                DeviceDetailsSelectors.TAG_TEMPLATE.format(expected_text_value)
            )
        ).to_be_visible()
        return self

    def _open_actions(self):
        """Open actions dialog.
        :return: current instance of Device Details page object.
        """
        if self.page.locator(DeviceDetailsSelectors.ACTIONS_POPUP).is_hidden():
            log.info("Playwright: click 'Actions' button.")
            self.page.locator(DeviceDetailsSelectors.ACTIONS_DROPDOWN).click()
        return self
