"""
Audit logs page object model
"""
import logging
from typing import Optional

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.audit_logs.ui.locators import AuditLogsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


# TODO: Remove following legacy methods below, when they are replaced in tests by corresponding table methods:
#  'should_have_subscr_in_table', 'should_subscr_with_text_have_details', 'should_have_added_claim_in_table',
#  'should_added_claim_with_text_have_details'


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

    def close_detail_dialog(self):
        self.page.locator(AuditLogsSelectors.DETAIL_CLOSE_BUTTON).click()
        return self

    def select_table_columns(self, *columns):
        """
        This will check/select the given columns for the audit log table to be populated.
        If no columns provided: by default Category, Description and Time are checked
        :param columns: columns to be selected.
        :return: current instance of audit log page object.
        """
        # By default Category, Description, Time are checked and disabled.
        # Also max 6 columns to be checked for the table to populate, so columns length should max 3
        if len(columns) > 3:
            raise ValueError("Only 3 Columns expected to display in audit log table...")
        log.info(f"Playwright: set displayed columns in audit logs: '{columns}'.")
        self.pw_utils.click_selector(AuditLogsSelectors.EDIT_COLUMNS_BTN)
        self.page.locator(AuditLogsSelectors.EDIT_COLS_MODAL_DIALOG).wait_for()
        for column in self.page.locator(AuditLogsSelectors.TABLE_COLUMNS).all():
            column.uncheck()
        for col in columns:
            self.page.locator(AuditLogsSelectors.SELECT_COLS_TEMPLATE.format(col)).check()
        self.page.locator(AuditLogsSelectors.SAVE_EDIT_COLS_BTN).click()
        return self

    def reset_default_table_columns(self):
        """
        Reset to default audit logs table columns
        :return: current instance of audit log page object
        """
        log.info("Playwright: reset displayed columns in audit logs.")
        self.pw_utils.click_selector(AuditLogsSelectors.EDIT_COLUMNS_BTN)
        self.page.locator(AuditLogsSelectors.EDIT_COLS_MODAL_DIALOG).wait_for()
        self.page.locator(AuditLogsSelectors.RESET_DEFAULT_COLS_BTN).click()
        self.page.locator(AuditLogsSelectors.SAVE_EDIT_COLS_BTN).click()
        return self

    def should_have_no_log_data(self):
        """Check that no log data displayed

        :return: current instance of audit log page object.
        """
        log.info("Playwright: checking for no log data")
        expect(self.page.locator(AuditLogsSelectors.NO_AUDIT_LOG_DATA)).to_be_visible()
        return self

    def should_have_subscr_in_table(self, search_text):
        """Check table row content is expected for subscriptions assignment string.
        NOTE: LEGACY METHOD! WILL BE REMOVED! Please use 'should_have_row_with_values_in_columns()' instead.

        :param search_text: search_text
        :return: current instance of audit log page object
        """
        log.info(
            f"Playwright: check that 'DEVICE_SUBSCRIPTION_ASSIGNED' item "
            f"with text '{search_text}' is present in table"
        )
        subscription_item = AuditLogsSelectors.AUDIT_LOG_SM_ITEM_TEMPLATE.format(
            search_text
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(subscription_item).first).to_be_visible()
        return self

    def should_subscr_with_text_have_details(self, item_text, details_text):
        """Clicks on table row for subscription and check details for description on opened panel.
        NOTE: LEGACY METHOD! WILL BE REMOVED! Please use 'open_row_details()' and 'should_audit_log_item_have_details()'
        instead.

        :param item_text: item_text
        :param details_text: details_text
        :return: current instance of audit log page object
        """
        log.info(f"Playwright: check that description in item details is correct")
        subscription_item = AuditLogsSelectors.AUDIT_LOG_SM_ITEM_TEMPLATE.format(
            item_text
        )
        self.page.locator(subscription_item).first.click()
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(AuditLogsSelectors.AUDIT_LOG_DESCRIPTION)).to_have_text(
            details_text
        )
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
        Check the table row matches given columns values of category, description, user_name
        and account_name
        :param: catefory
        :param: description
        :param: user_name
        :param: account_name
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

    def should_have_added_claim_in_table(self, search_text):
        """Check table row content match with expected for device's add claim string.
        NOTE: LEGACY METHOD! WILL BE REMOVED! Please use 'should_have_row_with_values_in_columns()' instead.

        :param search_text: search_text
        :return: current instance of audit log page object
        """
        log.info(
            f"Playwright: check that added device claim with text '{search_text}' is present in table."
        )
        subscription_item = AuditLogsSelectors.AUDIT_LOG_ADDED_DEV_ITEM_TEMPLATE.format(
            search_text
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(subscription_item).first).to_be_visible()
        return self

    def should_added_claim_with_text_have_details(self, item_text, details_text):
        """Click on table row for device's add claim and check details for description on opened panel.
        NOTE: LEGACY METHOD! WILL BE REMOVED! Please use 'open_row_details()' and 'should_audit_log_item_have_details()'
        instead.

        :param item_text: item_text
        :param details_text: details_text
        :return: current instance of audit log page object
        """
        log.info("Playwright: check that description in item details is correct.")
        subscription_item = AuditLogsSelectors.AUDIT_LOG_ADDED_DEV_ITEM_TEMPLATE.format(
            item_text
        )
        self.page.locator(subscription_item).first.click()
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(AuditLogsSelectors.AUDIT_LOG_DESCRIPTION)).to_have_text(
            details_text
        )
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