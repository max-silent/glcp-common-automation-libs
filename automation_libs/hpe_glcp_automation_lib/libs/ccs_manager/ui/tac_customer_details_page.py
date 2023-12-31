"""
TAC Customer Details page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import (
    TacCustomerDetailsSelectors,
)
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_device_details_page import (
    TacDeviceDetailsPage,
)
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_folder_details_page import (
    TacFolderDetails,
)
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacCustomerDetailsPage(HeaderedPage):
    """
    TAC Customer Details page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize TAC Customer Details page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Customer Details page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-ccs/customers/customer-details"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of TAC Customer Details page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(
            TacCustomerDetailsSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def click_tab_link(self, tab_text):
        """Click at menu item with specified text.

        :param tab_text: text of tab item to click.
        :return: current instance of TAC Customer Details page object.
        """
        log.info(f"Playwright: navigate to tab with text '{tab_text}'.")
        self.page.locator(
            TacCustomerDetailsSelectors.TABS_TEMPLATE.format(tab_text)
        ).click()
        self.table_utils.cached_table_context = tab_text
        return self

    def create_new_folder(self, folder_name, parent_folder="default", description=""):
        """Create new folder with specified name and parent.
        :param folder_name: name of the folder to create.
        :param parent_folder: parent folder's name.
        :param description: text value for description field of new folder.
        :return: current instance of Activate Folders page object.
        """
        log.info(f"Playwright: Create new folder '{folder_name}'.")
        self.page.locator(TacCustomerDetailsSelectors.CREATE_FOLDER_BTN).click()
        self.page.locator(TacCustomerDetailsSelectors.FOLDER_NAME_INPUT).fill(folder_name)
        self.pw_utils.select_drop_down_element(
            TacCustomerDetailsSelectors.PARENT_NAME_DROPDOWN, parent_folder, "option"
        )
        self.page.locator(TacCustomerDetailsSelectors.DESCRIPTION_INPUT).fill(description)
        self.page.locator(TacCustomerDetailsSelectors.POPUP_CREATE_BTN).click()
        return self

    def create_new_alias(self, alias_name, alias_type="Customer Name"):
        """Create new alias with specified name and type.
        :param alias_name: name of the alias to create.
        :param alias_type: alias type (default to 'Customer Name').
        :return: current instance of TAC Customer Details page object.
        """
        log.info(f"Playwright: Create new alias '{alias_name}'.")
        self.page.locator(TacCustomerDetailsSelectors.CREATE_ALIAS_BTN).click()
        self.page.locator(TacCustomerDetailsSelectors.ALIAS_NAME_INPUT_FIELD).fill(
            alias_name
        )
        self.pw_utils.select_drop_down_element(
            TacCustomerDetailsSelectors.ALIAS_TYPE_DROPDOWN, alias_type, "option"
        )
        self.page.locator(TacCustomerDetailsSelectors.POPUP_ADD_BTN).click()
        return self

    def delete_alias(self, alias_name):
        """Delete alias with specified name.
        :param alias_name: name of the alias.
        :return: current instance of TAC Customer Details page object.
        """
        log.info(f"Playwright: Delete new alias '{alias_name}'.")
        row = self.page.locator(TacCustomerDetailsSelectors.TABLE_ROWS).filter(
            has_text=alias_name
        )
        row.locator(TacCustomerDetailsSelectors.ITEM_MENU_BUTTON).click()
        self.page.locator(TacCustomerDetailsSelectors.DELETE_ALIAS_MENU_ITEM).click()
        self.page.locator(TacCustomerDetailsSelectors.POPUP_DELETE_BTN).click()
        self.page.wait_for_selector(
            TacCustomerDetailsSelectors.POPUP_DELETE_BTN
        ).is_hidden()
        return self

    def search_for_text(self, search_text, ensure_not_empty=True):
        """Enter text to search field.

        :param search_text: search_text.
        :param ensure_not_empty: defines either it's required to wait for non-empty table or not.
        :return: current instance of TAC Customer Details page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at TAC Customers.")
        self.pw_utils.enter_text_into_element(
            TacCustomerDetailsSelectors.SEARCH_FIELD, search_text
        )
        if ensure_not_empty:
            self.wait_for_loaded_table()
        else:
            self.wait_for_loaded_state()
        return self

    def open_folder_details_page(self, column_name, value):
        """Click at row, containing expected text in specified column.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: instance of Folder Details page object.
        """
        log.info(f"Playwright: click row with text '{value}' in column '{column_name}'.")
        self.wait_for_loaded_table()
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(
            column_name, value
        )
        if not matching_rows_indices:
            raise ValueError(
                f"Not found rows with '{value}' value at '{column_name}' column."
            )
        self.page.locator(
            TacCustomerDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                matching_rows_indices[0]
            )
        ).click()
        return TacFolderDetails(self.page, self.cluster)

    def move_to_folder(self, folder_name: str):
        """Move selected devices to the folder with specified name, using 'Actions' -> 'Move To Folder'
            dialog of 'Devices' tab.

        :param folder_name: name of the target folder.
        :return: current instance of TAC Customer Details page object.
        """
        self.page.locator(TacCustomerDetailsSelectors.ACTIONS_BTN).click()
        self.page.locator(TacCustomerDetailsSelectors.MOVE_TO_FOLDER_BTN).click()
        self.pw_utils.select_drop_down_element(
            drop_menu_selector=TacCustomerDetailsSelectors.FOLDER_NAME_DROPDOWN,
            element=folder_name,
            element_role="option",
            exact_match=True,
        )

        self.page.locator(TacCustomerDetailsSelectors.MOVE_TO_FOLDER_ACTION_BTN).click()
        self.page.locator(TacCustomerDetailsSelectors.MOVE_CONFIRMATION_BTN).click()
        return self

    def select_rows_with_text_in_column(self, column_name, value, required_match=True):
        """Enable checkboxes of the rows with matched text in specified column of table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :param required_match: is at least one match in displayed rows required or not.
        :return: current instance of TAC Customer Details page object.
        """
        log.info(
            f"Playwright: check checkboxes of rows with text '{value}' in column '{column_name}'."
        )
        self.table_utils.select_rows_with_value_in_column(
            column_name, value, required_match
        )
        return self

    def open_device_details_page(self, column_name, value):
        """Click at row, containing expected text in specified column.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: instance of Folder Details page object.
        """
        log.info(f"Playwright: click row with text '{value}' in column '{column_name}'.")
        self.wait_for_loaded_table()
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(
            column_name, value
        )
        if not matching_rows_indices:
            raise ValueError(
                f"Not found rows with '{value}' value at '{column_name}' column."
            )
        if column_name == "Serial Number":
            serial_number = value
        else:
            sn_column_index = self.table_utils.get_column_index_by_name("Serial Number")
            sn_column_selector = (
                TacCustomerDetailsSelectors.TABLE_ROW_COLUMN_TEMPLATE.format(
                    row_index=matching_rows_indices[0], column_index=sn_column_index
                )
            )
            serial_number = self.page.locator(sn_column_selector).text_content()
        self.page.locator(
            TacCustomerDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                matching_rows_indices[0]
            )
        ).click()
        return TacDeviceDetailsPage(self.page, self.cluster, serial_number)

    def get_visible_devices_count_in_folder(self, folder_name):
        """Get number of specified folder's devices, displayed at 'Number of Devices' column of the table,
        represented at 'Folders' tab of customer-details page.

        :param folder_name: name of folder, whose devices count is going to be retrieved.
        :return: number (int) of devices at specified folder.
        """
        log.info(f"Playwright: get displayed count of devices at '{folder_name}' folder.")
        dev_count = int(
            self.table_utils.get_column_value_from_matched_row(
                {"Name": folder_name}, "Number of Devices"
            )
        )
        return dev_count

    def go_back_to_customers(self):
        """Navigate back to Customers page."""
        log.info(f"Playwright: Navigate back to Customers page.")
        self.page.locator(TacCustomerDetailsSelectors.BACK_TO_CUSTOMERS_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def modify_subscription(self, subscr_key, end_date=None, quantity=None):
        """Modify subscription with 'subscr_key' by specified values.

        :param subscr_key: subscription key of subscription to be modified.
        :param end_date: expiration date to be set (remains unchanged if not specified).
        :param quantity: quantity of seats to be set (remains unchanged if not specified).
        :return: current instance of TAC Customer Details page object.
        """
        log.info(f"Playwright: Modify subscription '{subscr_key}'.")
        row_index = self.table_utils.get_rows_indices_by_text_in_column(
            "Key", subscr_key
        )[0]
        self.page.locator(
            TacCustomerDetailsSelectors.TABLE_ROW_ACTIONS_TEMPLATE.format(row_index)
        ).click()
        self.page.locator(
            TacCustomerDetailsSelectors.TABLE_ROW_ACTIONS_ITEM_TEMPLATE.format("Modify")
        ).click()
        if end_date:
            log.info(f"Playwright: Setting subscription end date to '{end_date}'...")
            field = self.page.locator(TacCustomerDetailsSelectors.POPUP_END_DATE_FIELD)
            field.clear()
            field.fill(end_date)
        if quantity:
            log.info(
                f"Playwright: Setting subscription seats quantity to '{quantity}'..."
            )
            field = self.page.locator(TacCustomerDetailsSelectors.POPUP_QUANTITY_FIELD)
            field.clear()
            field.fill(quantity)
        self.page.locator(TacCustomerDetailsSelectors.POPUP_MODIFY_BTN).click()
        self.page.wait_for_selector(
            TacCustomerDetailsSelectors.POPUP_MODIFY_BTN, state="hidden"
        )
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of TAC Customer Details page object.
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
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(
                TacCustomerDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value'
            is text to be in that column.
        :return: current instance of TAC Customer Details page object.
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
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(
                TacCustomerDetailsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of TAC Customer Details page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(TacCustomerDetailsSelectors.TABLE_ROWS)).to_have_count(
            count
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    # TODO: Refactor for not taking unused arguments (or remove since it just wraps existing 'should_have_rows_count()')
    def should_not_have_folder_in_the_table(self, folder_name):
        """Check that folder is not in the table. Empty table expected.

        :param folder_name: folders' name.
        :return: current instance of TAC Customer Details page object.
        """
        log.info("Playwright: check that folder is not in the table.")
        self.should_have_rows_count(0)
        return self
