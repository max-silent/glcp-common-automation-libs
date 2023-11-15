"""
Apply Subscription page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.sm.ui.locators import ApplySubscriptionSelectors

log = logging.getLogger(__name__)


class ApplySubscription(BasePage):
    """
    Apply Subscription page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Apply Subscription page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Apply Subscription page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/devices/inventory/apply-subscription"

    def apply_subscription_for_model(
        self, model, subscr_tier="Advance", subscr_key_id=None, subscr_key_index=1
    ):
        """Apply Subscription to selected device(s) using wizard of apply-subscription page.

        :param model: model of device(s) to be licensed.
        :param subscr_tier: subscription tier with licenses (partially matched text).
        :param subscr_key_id: id of subscription within specified tier to be applied.
        :param subscr_key_index: order of subscription within specified tier to be applied
            (will be processed only if subscr_key_id=None).
        :return: licence key number of applied subscription.
        """
        log.info("Playwright: Apply subscription via apply-subscription page's wizard.")
        self.page.locator(
            ApplySubscriptionSelectors.APPLY_SUBSCRIPTION_BTN_TEMPLATE.format(model)
        ).click()
        self.pw_utils.select_drop_down_element(
            ApplySubscriptionSelectors.LICENSE_TIER_DROPDOWN,
            subscr_tier,
            element_role="option",
        )
        if subscr_key_id:
            log.warning(
                "Playwright: ignoring 'subscr_key_index' argument since 'subscr_key_id' was passed to method."
            )
            license_key = subscr_key_id
            self.page.locator(
                ApplySubscriptionSelectors.SUBSCRIPTION_CHECKBOX_ID_TEMPLATE.format(
                    license_key
                )
            ).click()
        else:
            license_key = self.page.locator(
                ApplySubscriptionSelectors.SUBSCRIPTION_KEY_TEMPLATE.format(
                    subscr_key_index
                )
            ).text_content()
            self.page.locator(
                ApplySubscriptionSelectors.SUBSCRIPTION_CHECKBOX_TEMPLATE.format(
                    subscr_key_index
                )
            ).click()
        self.page.locator(ApplySubscriptionSelectors.APPLY_SUBSCRIPTION_BTN).click()
        self.page.locator(ApplySubscriptionSelectors.APPLY_SUBSCRIPTION_BTN).wait_for(
            state="hidden"
        )
        self.page.locator(ApplySubscriptionSelectors.FINISH_BUTTON).click()
        self.page.locator(ApplySubscriptionSelectors.CLOSE_BUTTON).click()
        return license_key

    def get_available_subscriptions(self, model, subscr_tier="Advance"):
        """Get list of available subscription's keys, displayed at apply-subscription wizard for specified tier.

        :param model: model of device(s) to be selected in apply-subscription wizard.
        :param subscr_tier: subscription tier with licenses (partially matched text).
        :return: list of displayed subscription keys.
        """
        log.info(
            "Playwright: get list of subscription's keys available via apply-subscription page's wizard."
        )
        self.page.locator(
            ApplySubscriptionSelectors.APPLY_SUBSCRIPTION_BTN_TEMPLATE.format(model)
        ).click()
        self.pw_utils.select_drop_down_element(
            ApplySubscriptionSelectors.LICENSE_TIER_DROPDOWN,
            subscr_tier,
            element_role="option",
        )
        self.pw_utils.wait_for_selector(
            ApplySubscriptionSelectors.SUBSCRIPTION_KEYS, timeout_ignore=True
        )
        subscr_keys = []
        for item in self.page.locator(ApplySubscriptionSelectors.SUBSCRIPTION_KEYS).all():
            subscr_keys.append(item.text_content())
        self.page.locator(
            ApplySubscriptionSelectors.APPLY_SUBSCRIPTION_CANCEL_BTN
        ).click()
        self.page.locator(
            ApplySubscriptionSelectors.APPLY_SUBSCRIPTION_CANCEL_BTN
        ).wait_for(state="hidden")
        log.info(f"Subscriptions found: {subscr_keys}.")
        return subscr_keys
