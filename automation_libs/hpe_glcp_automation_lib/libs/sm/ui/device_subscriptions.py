"""
Device Subscriptions page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.subscription_details import SubscriptionDetails
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_devices_navigable_page import (
    SideMenuNavigablePage,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.sm.ui.locators import DevSubscriptionsSelectors

log = logging.getLogger(__name__)


class DeviceSubscriptions(HeaderedPage, SideMenuNavigablePage):
    """
    Device Subscriptions page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """Initialize with page and cluster.

        :param page: Page.
        :param cluster: cluster under test url.
        """
        log.info("Initialize Device Subscriptions page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/devices/subscriptions"

    def wait_for_loaded_table(self):
        """Wait for table rows are not empty on the page.

        :return: current instance of Device Subscriptions page object.
        """
        log.info(f"Playwright: wait for loaded table in Device Subscriptions.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(DevSubscriptionsSelectors.TABLE_ROWS, strict=False)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def add_device_subscription(self, sub_key):
        """Add device subscription by subscription key.
        :param sub_key: subscription key.
        :return: current instance of Device Subscriptions page object.
        """
        log.info(f"Playwright: Add device subscription by subscription key.")
        self.page.locator(DevSubscriptionsSelectors.ADD_SUBS_BUTTON).click()
        self.page.locator(DevSubscriptionsSelectors.SUBS_KEY_FIELD).fill(sub_key)
        self.page.locator(DevSubscriptionsSelectors.SUBMIT_SUBS_BTN).click()
        return self

    def search_for_text(self, search_text):
        """Enter text to search field.

        :param search_text: search_text.
        :return: current instance of Device Subscriptions page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' in Device Subscriptions")
        self.pw_utils.enter_text_into_element(
            DevSubscriptionsSelectors.SEARCH_FIELD, search_text
        )
        self.wait_for_loaded_table()
        return self

    def set_device_type_filtering_item(self, device_type, selected=True):
        """Set device type filtering of Devices Subscriptions to specified state.
        :param device_type: device type.
        :param selected: include (True) or exclude (False) specified device type from filtering.
        :return: current instance of Device Subscriptions page object.
        """
        log.info(f"Playwright: set Advanced Search filter to specified values.")
        self.page.locator(DevSubscriptionsSelectors.DEV_TYPES_DROPDOWN).click()
        list_item = DevSubscriptionsSelectors.DEV_TYPES_ITEM_TEMPLATE.format(device_type)
        expected_state = "true" if selected else "false"
        if self.page.locator(list_item).get_attribute("aria-selected") == expected_state:
            self.page.locator(
                DevSubscriptionsSelectors.DEV_TYPES_DROPDOWN
            ).click()  # collapse dropdown.
        else:
            self.page.locator(
                list_item
            ).click()  # click on list item to change its state.
        return self

    def click_clear_filters(self):
        """
        Clicks the clear filter button if visible.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: clicking clear filters button")
        self.page.locator(DevSubscriptionsSelectors.CLEAR_FILTER_BTN).click()
        return self

    def open_filter_popup(self):
        """
        Clicks the filter button.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: Clicking filter menu button")
        self.page.locator(DevSubscriptionsSelectors.FILTER_BUTTON).click()
        return self

    def click_apply_filters(self):
        """
        Clicks the close filter menu button and applies selected settings.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: Closing filter menu and applying selection")
        self.page.locator(DevSubscriptionsSelectors.APPLY_FILTER_BTN).click()
        return self

    def close_filter_popup(self):
        """
        Clicks the close filter menu button and discards selected settings.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: Closing filter menu and discarding selection")
        self.page.locator(DevSubscriptionsSelectors.CANCEL_FILTER_BTN).click()
        return self

    def add_subscription_tier_filtering_item(self, tier: str):
        """
        Adds the given filter for subscription tier.
        :params tier: The subscription tier filter that is to be selected.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info(f"Playwright selecting subscription tier filer {tier}")
        self.open_filter_popup()
        self._select_checkbox_item("Subscription Tier", tier)
        self.click_apply_filters()
        return self

    def add_expiration_date_filtering_item(self, expiration):
        """
        Adds the given filter for expiration date.
        :params expiration: The expiration date filter that is to be selected.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info(f"Playwright selecting expiration date filer of {expiration} days")
        self.open_filter_popup()
        self._select_radiobutton_item("Expiration Date", expiration)
        self.click_apply_filters()
        return self

    def add_visibility_filtering_item(self, visibility):
        """
        Adds the given filter for subscription visibility.
        :params visibility: The expiration date filter that is to be selected.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info(f"Playwright selecting subscription visibility filer of {visibility}")
        self.open_filter_popup()
        self._select_radiobutton_item("Subscription Visibility", visibility)
        self.click_apply_filters()
        return self

    def click_actions_export(self):
        """
        Clicks on the "Export" button in the Action dropdown.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: clicking Actions Export button")
        self.page.locator(DevSubscriptionsSelectors.ACTION_BTN).click()
        self.page.locator(DevSubscriptionsSelectors.EXPORT_BTN).click()
        return self

    def close_export_dialog(self):
        """
        Closes the export dialog.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: closing the export dialog")
        self.page.locator(DevSubscriptionsSelectors.EXPORT_DIALOG_CANCEL).click()
        return self

    def open_subscription_information(self, subscription_key):
        """
        Searches for the given subscription key and opens the subscription information dialog.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info(
            f"Playwright: opening Subscription information of Subscription: {subscription_key}"
        )
        self.search_for_text(subscription_key)
        self.page.locator(
            DevSubscriptionsSelectors.SUBSCRIPTION_KEY_TEMPLATE.format(subscription_key)
        ).click()
        return SubscriptionDetails(
            page=self.page, cluster=self.cluster, key=subscription_key
        )

    def click_on_found_here(self):
        """Click on 'found here' service subscription link"""
        log.info("Playwright: click on 'found here' button.")
        self.page.locator(DevSubscriptionsSelectors.SERVICE_SUBSCRIPTIONS_LNK).click()
        # Note: instance of ServiceSubscriptions page object cannot be returned due to the circular import

    def should_have_search_field(self):
        """Check that search field with correct placeholder is present on the page.

        :return: current instance of Device Subscriptions page object.
        """
        log.info(f"Playwright: check search field is present at device subscriptions.")
        search_field_locator = self.page.locator(DevSubscriptionsSelectors.SEARCH_FIELD)
        self.pw_utils.save_screenshot(self.test_name)
        expect(search_field_locator).to_be_visible()
        expect(search_field_locator).to_have_attribute(
            "placeholder", "Search Subscription Keys"
        )
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of Device Subscriptions page object.
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
                DevSubscriptionsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs,
        where 'key' is column name and 'value' is text to match value in that column.
        :return: current instance of Device Subscriptions page object.
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
                DevSubscriptionsSelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of Device Subscriptions page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(self.page.locator(DevSubscriptionsSelectors.TABLE_ROWS)).to_have_count(
            count
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def should_have_device_subscription_header(self):
        """
        Checks that the device subscription header is visible.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: check for device subscription header")
        expect(
            self.page.locator(DevSubscriptionsSelectors.DEV_SUBSCRIPTIONS_HEADER)
        ).to_be_visible()
        return self

    def should_have_export_dialog(self):
        """
        Checks for presence of export dialog header.
        :return: current instance of Device Subscriptions page Object.
        """
        log.info("Playwright: checking for export dialog header")
        expect(
            self.page.locator(DevSubscriptionsSelectors.EXPORT_DIALOG_HEADER)
        ).to_be_visible()
        return self

    def should_have_subtitle(self):
        """Check that displayed subtitle is present.
        :return: current instance of Device Subscriptions page object.
        """
        log.info("Playwright: verify subtitle on the Device Subscriptions page")
        expect(
            self.page.locator(DevSubscriptionsSelectors.PAGE_SUBTITLE_TXT)
        ).to_be_visible()
        return self

    def _select_radiobutton_item(self, field_label, item_label):
        """
        Selects the checkbox with text, listed in 'item_labels' list and located at field labeled as 'field_label'.
        :param field_label: text label of the field, whose checkbox-items have to be checked.
        :param item_label: checkbox-item, to be selected.
        :return: current instance of Device Subscriptions page Object.
        """
        selector_qualifiers = {"field_label": field_label}
        selector_qualifiers.update({"item_label": item_label})
        item_locator = self.page.locator(
            DevSubscriptionsSelectors.FILTER_ITEM_TEMPLATE.format(**selector_qualifiers)
        )
        if item_locator.locator("svg[viewBox]").is_hidden():
            item_locator.click()
        else:
            log.warning(
                f"Filter radiobutton '{item_label}' at '{field_label}' field was set already."
            )
        return self

    def _select_checkbox_item(self, field_label, item_labels):
        """
        Selects the checkboxes with text, listed in 'item_labels' list and located at field labeled as 'field_label'.
        :param field_label: text label of the field, whose checkbox-items have to be checked.
        :param item_label: checkbox-items, to be selected.
        :return: current instance of Device Subscriptions page Object.
        """
        selector_qualifiers = {"field_label": field_label}
        for item in item_labels:
            selector_qualifiers.update({"item_label": item})
            item_locator = self.page.locator(
                DevSubscriptionsSelectors.FILTER_ITEM_TEMPLATE.format(
                    **selector_qualifiers
                )
            )
            if item_locator.locator("svg[viewBox]").is_hidden():
                item_locator.click()
            else:
                log.warning(
                    f"Filter checkbox '{item_labels}' at '{field_label}' field was set already."
                )
        return self
