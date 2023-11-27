"""
Audit logs page object model
"""
import logging
from typing import Optional

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.audit_logs.ui.locators import AuditLogsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class AuditLogs(HeaderedPage):
    """
    Audit logs page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize AuditLogs page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/auditlogs"
        self.downloaded_filename = None

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page
        :return: current instance of audit log page object
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.locator(AuditLogsSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_selector(
            AuditLogsSelectors.AUDIT_LOGS_TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(
        self,
        search_text,
        changed_rows_timeout: Optional[int] = None,
        timeout_ignore=False,
        ensure_not_empty=True,
    ):
        """
        Enter text to search field
        :param search_text: search_text
        :param changed_rows_timeout: timeout (seconds) to check for changed rows counter value.
        :param timeout_ignore: defines either it's allowed to continue without changed number of records count or not.
        :param ensure_not_empty: defines either it's required to wait for non-empty table or not.
        :return: current instance of audit log page object
        """
        log.info(f"Playwright: search for text: '{search_text}' in audit logs")
        self.pw_utils.store_text_content(AuditLogsSelectors.TABLE_ROWS_COUNT)
        self.pw_utils.enter_text_into_element(
            AuditLogsSelectors.SEARCH_FIELD, search_text
        )
        if changed_rows_timeout:
            self.pw_utils.wait_for_changed_text_content(
                AuditLogsSelectors.TABLE_ROWS_COUNT, changed_rows_timeout, timeout_ignore
            )
        if ensure_not_empty:
            self.wait_for_loaded_table()
        else:
            self.wait_for_loaded_state()
        return self

    def open_row_details(self, column_name, value):
        """Click at row, containing expected text in specified column.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of audit log page object.
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
            AuditLogsSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0])
        ).click()
        return self

    def clear_search_field(self, changed_rows_timeout: Optional[int] = None):
        """Clear search field. If 'changed_rows_timeout' specified - make sure that rows counter value
            has changed within specified timeout.

        :param changed_rows_timeout: timeout (seconds) to check for changed rows counter value.
        :return: current instance of audit log page object.
        """
        log.info(f"Playwright: clear value in search field of audit logs.")
        self.pw_utils.store_text_content(AuditLogsSelectors.TABLE_ROWS_COUNT)
        self.page.locator(AuditLogsSelectors.SEARCH_FIELD).clear()
        if changed_rows_timeout:
            self.pw_utils.wait_for_changed_text_content(
                AuditLogsSelectors.TABLE_ROWS_COUNT, changed_rows_timeout
            )
        self.wait_for_loaded_table()
        return self

    def clear_filter(self):
        """Clear Audit Logs filter.

        :return: current instance of audit log page object.
        """
        log.info(f"Playwright: clear value in search field of Audit Logs.")
        self.page.locator(AuditLogsSelectors.CLEAR_FILTERS_BUTTON).click()
        return self

    def close_detail_dialog(self):
        self.page.locator(AuditLogsSelectors.DETAIL_CLOSE_BUTTON).click()
        return self

    def select_table_columns(self, *columns, reset_checked=True):
        """
        This will check/select the given columns for the audit log table to be populated.
        If no columns provided: by default Category, Description and Time are checked
        :param columns: columns to be selected.
        :param reset_checked: uncheck (True) all selectable columns or not (False).
        :return: current instance of audit log page object.
        """
        # By default, Category, Description, Time are checked and disabled.
        # Also max 6 columns to be checked for the table to populate, so columns length should max 3
        if len(columns) > 3:
            raise ValueError("Only 3 Columns expected to display in audit log table...")
        log.info(f"Playwright: set displayed columns in audit logs: '{columns}'.")
        self.page.locator(AuditLogsSelectors.EDIT_COLUMNS_BTN).click()
        self.page.locator(AuditLogsSelectors.EDIT_COLS_MODAL_DIALOG).wait_for()
        if reset_checked:
            for column in self.page.locator(AuditLogsSelectors.TABLE_COLUMNS).all():
                column.uncheck()
        for col in columns:
            self.page.locator(AuditLogsSelectors.SELECT_COLS_TEMPLATE.format(col)).check()
        self.page.locator(AuditLogsSelectors.SAVE_EDIT_COLS_BTN).click()
        return self

    def deselect_table_columns(self, *columns):
        """
        removes columns under the audit log table

        :param columns: column labels to be removed from the audit log table
        e.g. username, IP address
        :return: current instance of audit log page object
        """
        self.page.locator(AuditLogsSelectors.EDIT_COLUMNS_BTN).click()
        self.page.locator(AuditLogsSelectors.EDIT_COLS_MODAL_DIALOG).wait_for()
        for col in columns:
            self.page.locator(
                AuditLogsSelectors.SELECT_COLS_TEMPLATE.format(col)
            ).uncheck()
        self.page.locator(AuditLogsSelectors.SAVE_EDIT_COLS_BTN).click()
        return self

    def reset_default_table_columns(self):
        """
        Reset to default audit logs table columns
        :return: current instance of audit log page object
        """
        log.info("Playwright: reset displayed columns in audit logs.")
        self.page.locator(AuditLogsSelectors.EDIT_COLUMNS_BTN).click()
        self.page.locator(AuditLogsSelectors.EDIT_COLS_MODAL_DIALOG).wait_for()
        self.page.locator(AuditLogsSelectors.RESET_DEFAULT_COLS_BTN).click()
        self.page.locator(AuditLogsSelectors.SAVE_EDIT_COLS_BTN).click()
        return self

    def set_advanced_search(self, *args, **kwargs):
        """Set audit log Advanced Filter to specified values.

        :param args: dictionary with set of sections names as dict keys and their values as dict values.
            Example:
                {"Category": ["App Management", "Delete Device"],
                 "Search Description": "Some description",
                 "Search IP Address": "10.0.0.5",
                 "Search Target": "Some target",
                 "Select Time": "Custom Time Range",
                 "Custom Date": "07/03/2023-10/31/2023"
                }
        :param kwargs: key-value pairs of fields to be set (applicable only if args with dictionary is not provided).
            Note: key should be passed in snake-case format, e.g. for "Search Target" field - pass "search_target".
            Example:
                category=["Reboot"],
                search_description="Some description 2",
                search_ip_address="10.0.0.10",
                search_target="Some target 2",
                select_time="Custom Time Range",
                custom_date="07/03/2023-10/31/2023"
        return :self reference
        """
        log.info(f"Playwright: set Advanced Search filter to specified values.")
        filter_dict = {}
        if args:
            if len(args) > 1 or not isinstance(args[0], dict) or kwargs:
                raise ValueError(
                    "Only 1 dictionary or series of kwargs should be passed to the method."
                )
            filter_dict = args[0]
        elif kwargs:
            for field_name, value in kwargs.items():
                field = " ".join(
                    [word.capitalize() for word in field_name.split("_")]
                ).replace("Ip", "IP")
                filter_dict[field] = value

        self.page.locator(AuditLogsSelectors.ADVANCED_SEARCH).click()
        for category in filter_dict.pop("Category", []):
            list_item = self.page.locator(
                AuditLogsSelectors.ADV_SEARCH_CATEGORY_TEMPLATE.format(category)
            )
            if list_item.locator("svg[viewBox]").is_hidden():
                log.debug(f"Select '{category}' item at filter's  'Category' section.")
                list_item.click()
            else:
                log.warning(
                    f"Filter checkbox '{category}' at 'Category' section was set already."
                )
        time_range = filter_dict.pop("Select Time", None)
        if time_range:
            log.debug(f"Set filter's 'Select Time' to '{time_range}'.")
            self.pw_utils.select_drop_down_element(
                AuditLogsSelectors.ADV_SEARCH_FIELD_TEMPLATE.format("Select Time"),
                time_range,
                element_role="option",
            )
            if time_range == "Custom Time Range":
                if "Custom Date" not in filter_dict:
                    raise ValueError(
                        "Missed dictionary key 'Custom Date': it's mandatory when 'Select Time' is 'Custom Time Range'."
                    )
                custom_date = filter_dict.pop("Custom Date")
                log.debug(f"Set filter's 'Custom Time Range' to '{custom_date}'.")
                self.page.locator(AuditLogsSelectors.ADV_SEARCH_CUSTOM_DATE_FIELD).fill(
                    custom_date
                )
        log.debug(f"Set filter's fields values: '{filter_dict}'.")
        for field, value in filter_dict.items():
            self.page.locator(
                AuditLogsSelectors.ADV_SEARCH_FIELD_TEMPLATE.format(field)
            ).fill(value)
        self.page.locator(AuditLogsSelectors.ADV_SEARCH_SAVE_BUTTON).click()
        return self

    def export_audit_log(self, file_type=None):
        """
        exports audit log in desired file type
        default file type if no arguments are passed is csv

        :param file_type: file format to export logs
        :return: current instance of audit log page object
        """

        self.page.locator(AuditLogsSelectors.EXPORT_LOG_BUTTON).click()
        if file_type:
            self.page.locator(
                AuditLogsSelectors.FILE_TYPE_TO_BE_EXPORTED_TEMPLATE.format(file_type)
            ).click()
        self.page.locator(AuditLogsSelectors.CONTINUE_BUTTON).click()
        with self.page.expect_download() as download_info:
            self.page.locator(AuditLogsSelectors.SAVE_EDIT_COLS_BTN).click()
        self.downloaded_filename = download_info.value.suggested_filename
        log.info(f"Filename for downloaded audit logs: {self.downloaded_filename}")
        return self

    def should_have_no_log_data(self):
        """Check that no log data displayed

        :return: current instance of audit log page object.
        """
        log.info("Playwright: checking for no log data")
        expect(self.page.locator(AuditLogsSelectors.NO_AUDIT_LOG_DATA)).to_be_visible()
        return self

    def should_audit_log_item_have_details(self, details_text):
        """Click at table row in Audit Logs page and check details for description on opened panel.

        :param details_text: details_text.
        :return: current instance of audit log page object.
        """
        log.info(f"Playwright: check that description in item details is correct")
        expect(self.page.locator(AuditLogsSelectors.AUDIT_LOG_DESCRIPTION)).to_have_text(
            details_text
        )
        return self

    def should_log_entry_exists(self, category, description, user_name, account_name):
        """
        Check the in the log entry table row matches given columns values of category, description, user_name
        and account_name
        :param category: Audit log category
        :param description: Audit log description
        :param user_name: Name of the user
        :param account_name: Name of the account (workspace)
        :return: current instance of audit log page object
        """
        selector = AuditLogsSelectors.LOG_ENTRY_CHECK.format(
            category=category,
            description=description,
            user_name=user_name,
            account_name=account_name,
        )
        expect(self.page.locator(selector)).to_be_enabled()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text
            to be in that column.
        :return: current instance of audit log page object.
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
                AuditLogsSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0])
            )
        ).to_be_visible()
        return self

    def should_matched_rows_count_be(self, column_to_text_dict, count):
        """Check that table has correct count of rows with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text
            to be in that column.
        :param count: expected count of matched rows.
        :return: current instance of audit log page object.
        """
        log.info(
            f"Playwright: check that rows count with specified values in related columns matches to expected."
        )
        matching_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(
            column_to_text_dict
        )
        actual_count = len(matching_rows_indices)
        assert (
            actual_count == count
        ), f"Wrong count of matched rows. Expected: {count}. Actual: {actual_count}."
        return self

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of audit logs page object.
        """
        log.info("Playwright: check that title has matched text in audit logs page.")
        expect(self.page.locator(AuditLogsSelectors.PAGE_TITLE)).to_be_visible()
        return self

    def should_columns_have_visiblity(self, *columns, visible=True):
        """
        Check table columns visibility.

        :param columns: columns to be checked
        :param visible: Boolean value for whether the columns are expected to
        be visible or not
        True = expects columns to be visible
        False = expects columns to not be visible

        :return: current instance of audit logs page object.
        """
        log.info(
            f"Playwright: check that table columns are"
            f"{'' if visible else ' not'} displayed: '{columns}'."
        )
        if visible:
            for col in columns:
                expect(
                    self.page.locator(
                        AuditLogsSelectors.TABLE_COLUMNS_TEXT_TEMPLATE.format(col)
                    )
                ).to_be_visible()
        else:
            for col in columns:
                expect(
                    self.page.locator(
                        AuditLogsSelectors.TABLE_COLUMNS_TEXT_TEMPLATE.format(col)
                    )
                ).not_to_be_visible()
        return self
