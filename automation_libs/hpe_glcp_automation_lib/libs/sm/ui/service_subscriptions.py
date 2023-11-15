"""
Service Subscriptions page object model
"""

import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.sm.ui.locators import ServiceSubscriptionsSelectors

log = logging.getLogger(__name__)


class DeviceSubscriptions(HeaderedPage):
    """
    Service Subscriptions page object model
    """

    def __init__(self, page: Page, cluster: str):
        """Initialize with page and cluster.

        :param page: Page.
        :param cluster: cluster under test url.
        """
        log.info("Initialize Service Subscriptions page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/subscriptions/service-subscriptions"

    def wait_for_loaded_table(self):
        """Wait for table rows are not empty on the page.

        :return: current instance of Service Subscriptions page object.
        """
        log.info(f"Playwright: wait for loaded table in Service Subscriptions.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(
            ServiceSubscriptionsSelectors.TABLE_ROWS, strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def check_subscription_exists(self, subscription_key):
        """Check if the subscriptions exists.
        :param subscription_key: Subscription service key to be checked if it exists.
        :return: boolean True if it exists otherwise False
        """
        log.info("Check if the subscription key already exists")
        self.page.locator(ServiceSubscriptionsSelectors.SERVICE_SUB_BTN).click()
        sub_key_exists = self.pw_utils.wait_for_selector(
            ServiceSubscriptionsSelectors.SUBSCR_KEY_ENTRY_TEMPLATE.format(
                subscription_key
            ),
            timeout_ignore=True,
            timeout=3000,
        )
        if sub_key_exists:
            log.info("Subscription key already exists!")
        return sub_key_exists

    def add_service_subscription_key(self, subscription_key, timeout=2000):
        """Add service subscription key
        :param subscription_key: Subscription service key to be added.
        :param timeout: timeout to wait for possible error-message.
        :return self: reference of the page or an exception for invalid key
        """

        log.info("Adding the subscription key now")
        add_subscr_button = self.page.locator(
            ServiceSubscriptionsSelectors.ADD_SUBSCR_BTN
        )
        add_subscr_button.click()

        subscr_key_input_field = self.page.locator(
            ServiceSubscriptionsSelectors.SUBSCR_KEY_INPUT_FIELD
        )
        subscr_key_input_field.fill(subscription_key)

        self.page.locator(ServiceSubscriptionsSelectors.SUBMIT_BTN).click()
        sub_err = self.pw_utils.wait_for_selector(
            ServiceSubscriptionsSelectors.ERROR_MSG, timeout_ignore=True, timeout=timeout
        )
        error_msg = self.page.locator(
            ServiceSubscriptionsSelectors.ERROR_MSG
        ).text_content()
        if sub_err:
            log.info(error_msg)
            raise Exception(error_msg)
        else:
            return self

    def should_have_service_subscription_title(self, text="Service Subscriptions"):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        """
        log.info(
            f"Playwright: check that title has Service Subscriptions text in Services page."
        )
        expect(
            self.page.locator(ServiceSubscriptionsSelectors.SERVICE_SUBSCRIPTION_TITLE)
        ).to_contain_text(text)
        return self

    def should_have_add_service_subscription_btn(self):
        """
        Check the presence of Add service subscription button
        :return: current instance of Service Subscriptions page object.
        """
        log.info("Playwright: checking the presence of Add service subscription button")
        expect(
            self.page.locator(ServiceSubscriptionsSelectors.ADD_SUBSCR_BTN)
        ).to_be_visible()
        return self

    def should_not_have_add_service_subscription_btn(self):
        """
        Check the presence of Add service subscription button
        :return: current instance of Service Subscriptions page object.
        """
        log.info("Playwright: checking the presence of Add service subscription button")
        expect(
            self.page.locator(ServiceSubscriptionsSelectors.ADD_SUBSCR_BTN)
        ).not_to_be_visible()
        return self
