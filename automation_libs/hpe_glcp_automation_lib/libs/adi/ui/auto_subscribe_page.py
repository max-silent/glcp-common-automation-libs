"""
Auto Subscribe page element
"""

import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import AutoSubscribeSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_devices_navigable_page import (
    SideMenuNavigablePage,
)

log = logging.getLogger(__name__)


class AutoSubscribe(HeaderedPage, SideMenuNavigablePage):
    """
    Auto Subscribe page object model.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize instance of page Auto Subscribe
        :param page: page
        :param cluster: cluster url.
        """

        log.info("Initialize Auto Subscribe page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/devices/auto-subscribe"
        self.valid_device_types = ["Switch", "Gateway", "Compute", "Sensor", "AP"]

    def delete_auto_subscribe(self, name: str):
        """
        Delete an auto subscription for a Device.
        :params name: Device type name. Accepted values: AP, Switch, Gateway, Compute, Sensor
        :returns: AutoSubscribe page object
        """
        log.info(f"Playwright: Deleting auto-subscription for '{name}'.")
        self._validate_device_type(name)
        self.page.locator(
            AutoSubscribeSelectors.DELETE_BTN_TEMPLATE.format(name.upper())
        ).click()
        self.page.locator(AutoSubscribeSelectors.CONFIRM_DELETE).click()
        return self

    def add_auto_subscription(self, name, tier):
        """
        Add auto subscription for a Device.
        :param name: Device type name. Accepted values: AP, Switch, Gateway, Compute, Sensor
        :param tier: Device tier Name
        :returns: self reference
        """
        log.info(f"Playwright: Adding auto subscription for {name}.")
        self._validate_device_type(name)
        subs_name = "Access Points" if name == "AP" else name
        self.page.click(AutoSubscribeSelectors.ADD_AUTOSUBSCRIBE_BTN)
        self.page.click(AutoSubscribeSelectors.SELECT_DEVICE_TYPE)
        self.page.click(
            AutoSubscribeSelectors.SUBSCRIPTION_TIER_MENU_ITEM_TEMPLATE.format(subs_name)
        )
        self.page.click(AutoSubscribeSelectors.SUBSCRIPTION_TIER_TYPE)
        self.page.click(
            AutoSubscribeSelectors.SUBSCRIPTION_TIER_MENU_ITEM_TEMPLATE.format(tier)
        )
        self.page.click(AutoSubscribeSelectors.CONFIGURE_DEVICE_BTN)
        self.page.locator(AutoSubscribeSelectors.CONFIGURE_DEVICE_BTN).wait_for(
            state="hidden"
        )
        return self

    def is_auto_subscribe_configured(self):
        """
        To check that account already has auto subscription(s).
        :return: bool
        """
        log.info("Checking if Auto Subscribe is configured or not.")
        return self.page.locator(
            AutoSubscribeSelectors.AUTO_SUBSCRIPTIONS_LIST
        ).is_visible()

    def edit_auto_subscribe(self, name, tier):
        """
        Edit an auto subscription for a Device.
        :param name: Device type name. Accepted values: AP, Switch, Gateway, Compute, Sensor
        :param tier: Device tier Name
        :returns: self reference
        """
        log.info(f"Playwright: Editing auto-subscription {name}.")
        self._validate_device_type(name)
        self.page.locator(
            AutoSubscribeSelectors.EDIT_BTN_TEMPLATE.format(name.upper())
        ).click()

        self.pw_utils.select_drop_down_element(
            drop_menu_selector=AutoSubscribeSelectors.SUBSCRIPTION_TIER_TYPE,
            element=tier,
            element_role="option",
            exact_match=False,
        )
        return self

    def click_edit_save(self):
        """
        Click Save button under edit auto-subscribe
        return: self reference
        """
        log.info(f"Playwright: Click Save button under auto-subscribe edit.")
        self.page.locator(AutoSubscribeSelectors.SAVE_BTN).click()
        return self

    def click_edit_save_ok(self):
        """
        Click OK button on the Update Auto-Subscribe notification pop-up
        return: self reference
        """
        log.info(
            f"Playwright: Click OK button on the 'Update Auto-Subscribe' notification pop-up."
        )
        self.page.locator(AutoSubscribeSelectors.UPDATE_OK_BTN).click()
        return self

    def click_edit_save_cancel(self):
        """
        Click Cancel button on the Update Auto-Subscribe notification pop-up
        return: self reference
        """
        log.info(
            f"Playwright: Click Cancel button on the 'Update Auto-Subscribe' notification pop-up."
        )
        self.page.locator(AutoSubscribeSelectors.UPDATE_CANCEL_BTN).click()
        return self

    def close_update_success_notification(self):
        """
        Close the 'Updated Auto Subscribe Successfully' notification pop-up
        return: self reference
        """
        log.info(
            f"Playwright: Close the 'Updated Auto Subscribe Successfully' notification pop-up."
        )
        self.page.locator(AutoSubscribeSelectors.SUCCESS_NOTIF_CLOSE_BTN).click()
        return self

    def should_particular_auto_subscription_be_configured(self, name):
        """
        Check auto subscription is configured for a Device type.
        :params name: Device type name. Accepted values: AP, Switch, Gateway, Compute, Sensor
        :returns: self reference
        """
        log.info(f"Playwright: check auto subscription configured for {name}.")
        self._validate_device_type(name)
        expect(
            self.page.locator(
                AutoSubscribeSelectors.AUTO_SUBS_LIST_TEMPLATE.format(name.upper())
            )
        ).to_be_visible()
        return self

    def should_not_particular_auto_subscription_be_configured(self, name):
        """
        Check auto subscription is not configured for a Device type.
        :params name: Device type name. Accepted values: AP, Switch, Gateway, Compute, Sensor
        :returns: self reference
        """
        log.info(f"Playwright: check auto subscription not configured for {name}.")
        self._validate_device_type(name)
        expect(
            self.page.locator(
                AutoSubscribeSelectors.AUTO_SUBS_LIST_TEMPLATE.format(name.upper())
            )
        ).to_be_hidden()
        return self

    def should_contain_card_tier_text(self, name, exp_tier):
        """
        Check the tier name for a Device type.
        :params name: Device type name. Accepted values: AP, Switch, Gateway, Compute, Sensor
        :params exp_tier : The expected tier Name
        :returns: self reference
        """
        log.info(
            f"Playwright: check auto subscription for '{name}' has text '{exp_tier}'."
        )
        expect(
            self.page.locator(
                AutoSubscribeSelectors.AUTO_SUBS_LIST_TEMPLATE.format(name.upper())
            )
        ).to_contain_text(exp_tier)
        return self

    def should_have_add_auto_subscribe_option(self):
        """
        Check the page has add auto-subscriber button
        :returns: self reference
        """
        log.info(f"Playwright: check the page has add auto-subscriber button.")
        expect(
            self.page.locator(AutoSubscribeSelectors.ADD_AUTOSUBSCRIBE_BTN)
        ).to_be_visible()
        return self

    def _validate_device_type(self, dev_type):
        if dev_type not in self.valid_device_types:
            raise ValueError(
                f"Unsupported device type. Supported types: {self.valid_device_types}"
            )
