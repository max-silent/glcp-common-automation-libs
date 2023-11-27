"""
TAC  page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacSubscriptionsSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_menu_navigable_page import (
    TacMenuNavigablePage,
)
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacSubscriptionsPage(HeaderedPage, TacMenuNavigablePage):
    """
    TAC Subscriptions page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize TAC Subscriptions page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Subscriptions page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-ccs/subscriptions"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of TAC Subscriptions page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(
            TacSubscriptionsSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text):
        """Enter text to search field.

        :param search_text: search_text.
        :return: current instance of TAC Subscriptions page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at TAC Subscriptions.")
        self.pw_utils.enter_text_into_element(
            TacSubscriptionsSelectors.SEARCH_FIELD, search_text
        )
        self.wait_for_loaded_table()
        return self

    def transfer_subscription(self, subs_key, pcid):
        """Search and then transfer corresponding subscription to given pcid account.

        :param subs_key: subscription key to be moved.
        :param pcid: destination Platform Customer ID.
        :return: current instance of TAC Subscriptions page object.
        """
        self.search_for_text(subs_key)
        log.info(
            f"Playwright: transferring: '{subs_key}' Subscription to {pcid} account."
        )
        self.page.locator(TacSubscriptionsSelectors.TABLE_ITEM_ACTION_BTN).first.click()
        self.page.locator(TacSubscriptionsSelectors.TRANSFER_ITEM_ACTION).click()
        self.page.locator(TacSubscriptionsSelectors.PCID_INPUT_FIELD_POPUP).fill(pcid)
        self.page.locator(TacSubscriptionsSelectors.TRANSFER_BTN_POPUP).click()
        self.page.locator(TacSubscriptionsSelectors.TRANSFER_BTN_POPUP).wait_for(
            timeout=20000, state="hidden"
        )
        self.wait_for_loaded_state()
        return self

    def get_error_on_transfer_subscription(self, subs_key, pcid):
        """Search and then verify that corresponding subscription cannot be transferred to given pcid account.

        :param subs_key: subscription key to be moved.
        :param pcid: destination Platform Customer ID.
        :return: text of error message, got during transfer operation.
        """
        self.search_for_text(subs_key)
        log.info(
            f"Playwright: Verifying error while transferring subscription '{subs_key}' to {pcid} account."
        )
        self.page.locator(TacSubscriptionsSelectors.TABLE_ITEM_ACTION_BTN).first.click()
        self.page.locator(TacSubscriptionsSelectors.TRANSFER_ITEM_ACTION).click()
        self.page.locator(TacSubscriptionsSelectors.PCID_INPUT_FIELD_POPUP).fill(pcid)
        self.page.locator(TacSubscriptionsSelectors.TRANSFER_BTN_POPUP).click()
        error_message = self.page.locator(
            TacSubscriptionsSelectors.TRANSFER_ERROR_MSG
        ).inner_text()
        self.page.locator(TacSubscriptionsSelectors.CANCEL_BTN_POPUP).click()
        return error_message

    def generate_eval_subscription(self, pcid, subs_tier="Advanced AP"):
        """Generates EVAL subscription to given pcid account.

        :param pcid: destination Platform Customer ID.
        :param subs_tier: subscription tier to be applied to newly created subscription. Optional, has default value.
        :return: current instance of TAC Subscriptions page object.
        """
        log.info(f"Playwright: Generating subscription for {pcid} account.")
        self.page.locator(TacSubscriptionsSelectors.GENERATE_SUBSCRIPTION_BTN).click()
        self.page.locator(TacSubscriptionsSelectors.PCID_INPUT_FIELD).fill(pcid)
        self.page.locator(
            TacSubscriptionsSelectors.SUBSCRIPTION_TIER_TEMPLATE.format(subs_tier)
        ).check()
        self.page.locator(TacSubscriptionsSelectors.GENERATE_SUBS_BTN_POPUP).click()
        self.wait_for_loaded_state()
        return self

    def click_table_row(self, row_index):
        """Click on table row with specified index (starting from 1).

        :param row_index: row index to click at.
        :return: instance of TAC Customer Details page object.
        """
        log.info(f"Playwright: check that description in item details is correct")
        self.page.locator(
            TacSubscriptionsSelectors.TABLE_ROW_TEMPLATE.format(row_index)
        ).click()
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of TAC Subscriptions page object.
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
                TacSubscriptionsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value'
            is text to be in that column.
        :return: current instance of TAC Subscriptions page object.
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
                TacSubscriptionsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of TAC Subscriptions page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(TacSubscriptionsSelectors.TABLE_ROWS)).to_have_count(
            count
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self
