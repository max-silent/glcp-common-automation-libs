"""
Devices Inventory page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.add_devices_page import AddDevices
from hpe_glcp_automation_lib.libs.adi.ui.device_details_page import DeviceDetails
from hpe_glcp_automation_lib.libs.adi.ui.locators import DevicesInventorySelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.sm.ui.apply_subscription_page import ApplySubscription

log = logging.getLogger(__name__)


class DevicesInventory(HeaderedPage):
    """
    Devices Inventory page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Devices Inventory page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Devices Inventory page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/devices/inventory"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(
            DevicesInventorySelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.locator(DevicesInventorySelectors.LOADER_SPINNER).wait_for(
            state="hidden"
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text, ensure_not_empty=True):
        """
        Enter text to search field.
        :param search_text: search_text.
        :param ensure_not_empty: defines either it's required to wait for non-empty table or not.
        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at devices inventory.")
        self.pw_utils.enter_text_into_element(
            DevicesInventorySelectors.SEARCH_FIELD, search_text
        )
        if ensure_not_empty:
            self.wait_for_loaded_table()
        else:
            self.wait_for_loaded_state()
        return self

    def click_add_devices(self):
        """Open add devices page.

        :return: instance of AddDevices page object.
        """
        log.info("Playwright: click 'Add Devices' button.")
        (self.page.locator(DevicesInventorySelectors.ADD_DEVICE_BUTTON)).click()
        return AddDevices(self.page, self.cluster)

    def add_filter_by_applications(self, applications: list):
        """Add devices table filtering by Applications list.

        :param applications: list of applications labels to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: adding devices table filtering by Applications list: '{applications}'."
        )
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_checkbox_items("Application", applications)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def add_filter_by_device_types(self, device_types: list):
        """Add devices table filtering by Devices Types list.

        :param device_types: list of devices types labels to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: adding devices table filtering by Devices Types list: '{device_types}'."
        )
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_checkbox_items("Device Type", device_types)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def add_filter_by_subscription_tiers(self, tiers: list):
        """Add devices table filtering by Subscription Tiers list.

        :param tiers: list of subscription tiers labels to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: adding devices table filtering by Subscription Tiers list: '{tiers}'."
        )
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_checkbox_items("Subscription Tier", tiers)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def add_filter_by_archived_visibility(self, visibility: str):
        """Add devices table filtering by Archived Devices Visibility option.

        :param visibility: visibility label of radiobutton to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            "Playwright: adding devices table filtering by Archived Devices Visibility option."
        )
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_radiobutton_items("Archived Devices Visibility", visibility)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def clear_filter(self):
        """Clear Devices Inventory filter.

        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: clear value in search field of audit logs.")
        self.page.locator(DevicesInventorySelectors.CLEAR_FILTERS_BUTTON).click()
        return self

    def select_rows_with_text_in_column(self, column_name, value, required_match=True):
        """Enable checkboxes of the rows with matched text in specified column of table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :param required_match: is at least one match in displayed rows required or not.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: check checkboxes of rows with text '{value}' in column '{column_name}'."
        )
        self.table_utils.select_rows_with_value_in_column(
            column_name, value, required_match
        )
        return self

    def assign_tag_to_devices(self, tag_name, tag_value):
        """Assign tag to selected devices.

        :param tag_name: tag name.
        :param tag_value: tag value.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: assign tag '{tag_name}' with text '{tag_value}' to selected devices."
        )
        self._choose_bulk_actions_item("Manage Tags")
        self.page.locator(DevicesInventorySelectors.TAG_NAME_INPUT).click()
        self.page.locator(DevicesInventorySelectors.TAG_INPUT_FIELD).type(
            tag_name, delay=100
        )
        self.page.locator(
            DevicesInventorySelectors.TAG_BUTTON_TEMPLATE.format(tag_name)
        ).click()
        self.page.locator(DevicesInventorySelectors.TAG_VALUE_INPUT).click()
        self.page.locator(DevicesInventorySelectors.TAG_INPUT_FIELD).type(
            tag_value, delay=100
        )
        self.page.locator(
            DevicesInventorySelectors.TAG_BUTTON_TEMPLATE.format(tag_value)
        ).click()
        self.page.locator(DevicesInventorySelectors.ASSIGN_BTN).click()
        self.page.locator(DevicesInventorySelectors.SUBMIT_BTN).click()
        self.page.locator(DevicesInventorySelectors.SUBMIT_BTN).wait_for(state="hidden")
        self.pw_utils.wait_for_selector(
            DevicesInventorySelectors.TABLE_ROWS_CHECK_ICONS, state="hidden", timeout=5000
        )
        return self

    def assign_devices_to_tenant(self, tenant_name):
        """Assign selected devices to specified tenant.

        :param tenant_name: tenant name.
        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: assign selected devices to tenant '{tenant_name}'.")
        self._choose_bulk_actions_item("Assign Devices")
        self.page.locator(
            DevicesInventorySelectors.ACCOUNT_TILE_TEMPLATE.format(tenant_name)
        ).click()
        self.page.locator(DevicesInventorySelectors.NEXT_BUTTON).click()
        self.pw_utils.select_drop_down_element_by_index(
            dropdown_selector=DevicesInventorySelectors.APPLICATION_DROPDOWN,
            list_items_selector=DevicesInventorySelectors.APP_DROPDOWN_LIST_ITEM,
            item_index=1,
        )
        self.pw_utils.select_drop_down_element_by_index(
            dropdown_selector=DevicesInventorySelectors.APP_REGION_DROPDOWN,
            list_items_selector=DevicesInventorySelectors.APP_DROPDOWN_LIST_ITEM,
            item_index=1,
        )
        self.page.locator(DevicesInventorySelectors.FINISH_BUTTON).click()
        self.page.locator(DevicesInventorySelectors.CLOSE_BTN).click()
        return self

    def apply_subscription(self, model, subscr_tier="Advance", subscr_key=None):
        """Apply subscription to selected devices with specified part number.

        :param model: model of selected device(s) to be licensed.
        :param subscr_tier: subscription tier (partially matched text).
        :param subscr_key: subscription key id.
        :return: applied subscription key number.
        """
        log.info(
            f"Playwright: assign subscription to selected devices of model '{model}'."
        )
        self._choose_bulk_actions_item("Apply Subscription")
        license_key = ApplySubscription(
            self.page, self.cluster
        ).apply_subscription_for_model(model, subscr_tier, subscr_key)
        log.info(f"Playwright: applied subscription key is '{license_key}'.")
        return license_key

    def detach_subscription(self):
        """Detach subscription from selected devices.

        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: detach subscription from selected devices.")
        self._choose_bulk_actions_item("Detach Subscription")
        self.page.locator(DevicesInventorySelectors.DETACH_BTN).click()
        self.page.locator(DevicesInventorySelectors.CLOSE_BTN).click()
        self.pw_utils.wait_for_selector(
            DevicesInventorySelectors.TABLE_ROWS_CHECK_ICONS,
            state="hidden",
            timeout=5000,
            strict=False,
        )
        return self

    def open_device_details_page(self, column_name, value):
        """Click at row, containing expected text in specified column.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: instance of Device Details page object.
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
                DevicesInventorySelectors.TABLE_ROW_COLUMN_TEMPLATE.format(
                    row_index=matching_rows_indices[0], column_index=sn_column_index
                )
            )
            serial_number = self.page.locator(sn_column_selector).text_content()
        self.page.locator(
            DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0])
        ).click()
        return DeviceDetails(self.page, self.cluster, serial_number)

    def archive_devices(self):
        """Archive selected devices.

        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: Archive selected devices.")
        self._choose_bulk_actions_item("Archive")
        self.page.locator(DevicesInventorySelectors.ARCHIVE_CONFIRM_BTN).click()
        self.page.locator(DevicesInventorySelectors.CLOSE_BTN).click()
        self.pw_utils.wait_for_selector(
            DevicesInventorySelectors.TABLE_ROWS_CHECK_ICONS,
            state="hidden",
            timeout=5000,
            strict=False,
        )
        return self

    def unarchive_devices(self):
        """Unarchive selected devices.

        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: Unarchive selected devices.")
        self._choose_bulk_actions_item("Unarchive")
        self.page.locator(DevicesInventorySelectors.ARCHIVE_CONFIRM_BTN).click()
        self.page.locator(DevicesInventorySelectors.CLOSE_BTN).click()
        self.pw_utils.wait_for_selector(
            DevicesInventorySelectors.TABLE_ROWS_CHECK_ICONS,
            state="hidden",
            timeout=5000,
            strict=False,
        )
        return self

    def unassign_devices(self):
        """Unassign selected devices.

        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: Unassign selected devices.")
        self._choose_bulk_actions_item("Remove Assignment")
        self.page.locator(DevicesInventorySelectors.UNASSIGN_CONFIRM_BTN).click()
        self.page.locator(DevicesInventorySelectors.CLOSE_BTN).click()
        self.pw_utils.wait_for_selector(
            DevicesInventorySelectors.TABLE_ROWS_CHECK_ICONS,
            state="hidden",
            timeout=5000,
            strict=False,
        )
        return self

    def should_action_be_unavailable(self, text):
        """Check that action with specified text is not present at the list of bulk-actions button.

        :param text: action text to search for.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: Check that action '{text}' is not displayed at bulk actions list."
        )
        self.page.locator(DevicesInventorySelectors.ACTIONS_BUTTON).click()
        self.page.wait_for_selector(DevicesInventorySelectors.ACTIONS_LIST)
        expect(
            self.page.locator(DevicesInventorySelectors.ACTIONS_TEMPLATE.format(text))
        ).to_be_hidden()
        self.page.locator(DevicesInventorySelectors.ACTIONS_BUTTON).click()
        return self

    def should_subscr_apply_be_unavailable(self, model, subscr_tier, subscr_key):
        """Check that specified subscription is not present in apply-subscription wizard for specified tier.

        :param model: model of device(s) to be selected in apply-subscription wizard.
        :param subscr_tier: subscription tier to be observed.
        :param subscr_key: subscription to be verified as unavailable.
        :return: current instance of Devices Inventory page object.
        """
        self._choose_bulk_actions_item("Apply Subscription")
        available_subscriptions = ApplySubscription(
            self.page, self.cluster
        ).get_available_subscriptions(model, subscr_tier)
        assert (
            subscr_key not in available_subscriptions
        ), f"Subscription '{subscr_key}' is present in list of available subscriptions of {subscr_tier} tier."
        return self

    def should_have_search_field(self):
        """Check that search field with correct placeholder is present on the page.

        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: check search field is present at devices inventory.")
        search_field_locator = self.page.locator(DevicesInventorySelectors.SEARCH_FIELD)
        self.pw_utils.save_screenshot(self.test_name)
        expect(search_field_locator).to_be_visible()
        expect(search_field_locator).to_have_attribute(
            "placeholder", "Search by Serial, Model, or MAC Address"
        )
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of Devices Inventory page object.
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
                DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text
            to be in that column.
        :return: current instance of Devices Inventory page object.
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
                DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(
                    matching_rows_indices[0]
                )
            )
        ).to_be_visible()
        return self

    def should_all_rows_have_text_in_column(self, column_name, allowed_values):
        """Check that current table page has only rows with values at 'column_name' column,
        which are present in specified 'allowed_values' list.

        :param column_name: column name where matching text should be looked at.
        :param allowed_values: list of allowed expected values in specified column.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: check all rows at current table page have only allowed values in '{column_name}' column."
        )
        matching_rows_indices = set()
        for value in allowed_values:
            matching_indices = self.table_utils.get_rows_indices_by_text_in_column(
                column_name, value
            )
            matching_rows_indices.update(set(matching_indices))
        if not matching_rows_indices:
            raise ValueError(
                f"Not found rows with any of '{allowed_values}' values at '{column_name}' column."
            )
        expect(
            self.page.locator(
                DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(
                    list(matching_rows_indices)[0]
                )
            )
        ).to_be_visible()
        rows_count = self.page.locator(DevicesInventorySelectors.TABLE_ROWS).count()
        expected_matching_rows_indices = set(range(1, rows_count + 1))
        assert expected_matching_rows_indices == matching_rows_indices, (
            f"Some table rows have unexpected value(s) at '{column_name}' column. "
            f"Mismatched rows indexes: '{sorted(expected_matching_rows_indices ^ matching_rows_indices)}'."
        )
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(self.page.locator(DevicesInventorySelectors.TABLE_ROWS)).to_have_count(
            count
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def should_have_add_device_btn(self):
        """
        Verify Add Device button
        return: self Reference
        """
        self.page.wait_for_load_state()
        expect(
            self.page.locator(DevicesInventorySelectors.ADD_DEVICE_BUTTON)
        ).to_be_visible()
        return self

    def should_have_text_in_title(self, text="Inventory"):
        """
        Verify device inventory title
        param:(str) optional
        return:(object) self reference
        """
        self.wait_for_loaded_state()
        expect(
            self.page.locator(DevicesInventorySelectors.DEVICE_INVENTORY_TITLE)
        ).to_have_text(text)
        return self

    def _select_checkbox_items(self, field_label, item_labels):
        """Select all checkboxes with text, listed in 'item_labels' list and located at field labeled as 'field_label'.

        :param field_label: text label of the field, whose checkbox-items have to be checked.
        :param item_labels: list of checkbox-items (list of text labels), to be selected.
        """
        selector_qualifiers = {"field_label": field_label}
        for item in item_labels:
            selector_qualifiers.update({"item_label": item})
            item_locator = self.page.locator(
                DevicesInventorySelectors.FILTER_ITEM_TEMPLATE.format(
                    **selector_qualifiers
                )
            )
            if item_locator.locator("svg[viewBox]").is_hidden():
                item_locator.click()
            else:
                log.warning(
                    f"Filter checkbox '{item}' at '{field_label}' field was set already."
                )

    def _select_radiobutton_items(self, field_label, item):
        """Select all checkboxes with text, listed in 'item_labels' list and located at field labeled as 'field_label'.

        :param field_label: text label of the field, whose checkbox-items have to be checked.
        :param item: text label of radiobutton item to be selected.
        """
        selector_qualifiers = {"field_label": field_label}
        selector_qualifiers.update({"item_label": item})
        selector = DevicesInventorySelectors.FILTER_ITEM_TEMPLATE.format(
            **selector_qualifiers
        )
        item_locator = self.page.locator(selector)
        if item_locator.locator("svg[viewBox]").is_hidden():
            item_locator.click()
        else:
            log.warning(
                f"Filter radiobutton '{item}' at '{field_label}' field was set already."
            )

    def _choose_bulk_actions_item(self, item_text):
        """Click bulk-actions button and select item with specified text.

        :param item_text: text of item to be clicked.
        :return: current instance of Devices Inventory page object.
        """
        self.page.locator(DevicesInventorySelectors.ACTIONS_BUTTON).click()
        self.page.locator(
            DevicesInventorySelectors.ACTIONS_TEMPLATE.format(item_text)
        ).click()
        return self

    def should_not_have_add_device_btn(self):
        """
        check the absence of add device button
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: Checking the absence of add device button")
        expect(
            self.page.locator(DevicesInventorySelectors.ADD_DEVICE_BUTTON)
        ).not_to_be_visible()
        return self
