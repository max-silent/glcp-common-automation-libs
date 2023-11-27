"""
Activate Device Details page object model.
"""
import logging
from datetime import datetime

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateDeviceDetailsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class ActivateDeviceDetails(HeaderedPage):
    """
    Activate Device Details page object model class.
    """

    def __init__(self, page: Page, cluster: str, serial_number: str):
        """
        Initialize Activate Device Details page object.
        :param page: page.
        :param cluster: cluster url.
        :param serial_number: device serial number.
        """
        log.info("Initialize Activate Device Details page object")
        super().__init__(page, cluster)
        self.page = page
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/activate/devices/{serial_number.upper()}"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.page.wait_for_selector(
            ActivateDeviceDetailsSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.locator(ActivateDeviceDetailsSelectors.LOADER_SPINNER).wait_for(
            state="hidden"
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def edit_device_details(self, device_name, device_full_name, device_desc):
        """Edit the existing device details - device name, device full name & device description
        :param: device_name: New device name to apply
        :param: device_full_name: New full device name to apply
        :param: device_desc: New device description to apply
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: Edit device details")
        self.pw_utils.click_selector(
            ActivateDeviceDetailsSelectors.EDIT_DEVICE_DETAILS_BTN
        )
        self.pw_utils.enter_text_into_element(
            ActivateDeviceDetailsSelectors.DEVICE_NAME_INPUT, device_name
        )
        self.pw_utils.enter_text_into_element(
            ActivateDeviceDetailsSelectors.DEVICE_FULL_NAME_INPUT, device_full_name
        )
        self.page.get_by_test_id(ActivateDeviceDetailsSelectors.DEVICE_DESC_INPUT).fill(
            device_desc
        )
        self.pw_utils.click_selector(ActivateDeviceDetailsSelectors.SAVE_CHANGES_BTN)
        return self

    def go_back_to_activate_device_page(self):
        """Navigate to Activate Devices page (back)."""
        self.page.locator(ActivateDeviceDetailsSelectors.BACK_TO_DEVICES_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_valid_date_for_status(
        self, expected_status, timedelta=300, column_name="Status"
    ):
        """Check that last executed event (according status name) is not too old
        (by default - not more than 5 minutes old).

        :param expected_status: expected status, action made with the device, which date need to be checked.
        :param timedelta: expected time difference between current time and table event time, seconds. Default 300.
        :param column_name: Table column name, wor which we will check the expected status. Default to 'Status'.
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: verify date for corresponding device event status")
        expected_date = datetime.now()
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(
            column_name, expected_status
        )
        date_locator = self.page.locator(
            ActivateDeviceDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                matching_rows_indices[0]
            )
        ).nth(0)
        table_row_date = date_locator.all_inner_texts()[0].split("\n")[0]
        table_date = datetime.strptime(table_row_date, "%m/%d/%Y %I:%M %p")
        assert abs((table_date - expected_date).total_seconds()) < timedelta, (
            f"Failed: last {expected_status} event is too old (more than {timedelta} seconds difference from table "
            f"datetime, current time delta: {abs((table_date - expected_date).total_seconds())} seconds)"
        )
        return self

    def should_have_details_update_success_notification(self, text):
        """Validate the device details update success notification
        :param: text message to be validated
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: Validate the device details update success notification")
        self.page.wait_for_load_state("domcontentloaded")
        expect(
            self.page.locator(
                ActivateDeviceDetailsSelectors.DEVICE_UPDATED_SUCCESS_NOTIFICATION
            )
        ).to_have_text(text)
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of Activate Device Details page object.
        """
        log.info(
            f"Playwright: check that row with text '{value}' in column '{column_name}' is present in table."
        )
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(
            column_name, value
        )
        if not matching_rows_indices:
            raise ValueError(
                f"Not found rows with '{value}' value at '{column_name}' column."
            )
        expect(
            self.page.locator(
                ActivateDeviceDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text
        to be in that column.
        :return: current instance of Activate Device Details page object.
        """
        log.info(
            f"Playwright: check that row with expected text values in related columns is present in table."
        )
        matching_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(
            column_to_text_dict
        )
        if not matching_rows_indices:
            raise ValueError(
                f"Not found rows with expected text values at related columns: '{column_to_text_dict}'."
            )
        expect(
            self.page.locator(
                ActivateDeviceDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(
            self.page.locator(ActivateDeviceDetailsSelectors.TABLE_ROWS)
        ).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self
