"""
Service Subscriptions page object model.
"""

import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_services_navigable_page import (
    SideMenuNavigablePage,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.sm.ui.locators import ServiceSubscriptionsSelectors

log = logging.getLogger(__name__)


class ServiceSubscriptions(HeaderedPage, SideMenuNavigablePage):
    """
    Service Subscriptions page object model.
    """

    def __init__(self, page: Page, cluster: str):
        """Initialize with page and cluster.

        :param page: Page.
        :param cluster: cluster under test url.
        """
        log.info("Initialize Service Subscriptions page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/services/service-subscriptions"

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

    def add_service_subscription_key(
        self, subscription_key, timeout=2000, expect_failure=False
    ):
        """Add service subscription key
        :param subscription_key: Subscription service key to be added.
        :param timeout: timeout to wait for possible error-message.
        :param expect_failure: if 'True' it will expect failed add key attempt and  error message presence. Default to 'False'
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
            if not expect_failure:
                raise Exception(error_msg)
        return self

    def click_service_subscription(self, subscription_key):
        """
        Clicks a service subscription (by the given subscription_key) from the list, to open subscription details popup
        :return: current instance of Service Subscriptions page object.
        """
        log.info("Playwright clicking Service by Subscription Key")
        self.page.locator(
            ServiceSubscriptionsSelectors.SUBSCR_KEY_FIELD_TEMPLATE.format(
                subscription_key
            )
        ).click()
        return self

    def click_goto_application_from_subscription_details(self):
        """
        Opens a service from an opened service details dialog
        # Note: navigates current page to Service Details page
        """
        log.info("Playwright opening application from subscriptions details box")
        self.page.locator(ServiceSubscriptionsSelectors.GO_TO_APP_BTN).click()

    def click_on_found_here(self):
        """
        Clicks on the "found here" link.
        This click lands on a Device subcriptions page \
        The reason why this is not returned is to avoid a circular import
        """
        log.info("Playwright: click on 'found here' link.")
        # Note: DeviceSubscriptions instance cannot be returned due to the circular import
        self.page.locator(ServiceSubscriptionsSelectors.FOUND_HERE_LINK).click()

    def close_add_subscription_popup(self):
        """
        Closes the add subscription popup
        returns: Service Subscription page object
        """
        log.info("Playwright: closing add subscription popup")
        self.page.locator(ServiceSubscriptionsSelectors.SERVICE_CANCEL_BTN).click()
        return self

    def should_have_heading_title(self):
        """Check that expected heading title is present at the page.
        :return: current instance of Service Subscriptions page object.
        """
        log.info(
            f"Playwright: check that Services heading title is present in Service Subscriptions page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(ServiceSubscriptionsSelectors.SERVICE_SUBSCRIPTIONS_HEADING)
        ).to_be_visible()
        return self

    def should_have_service_subscription_title(self, text="Service Subscriptions"):
        """Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of Service Subscriptions page object.
        """
        log.info(
            f"Playwright: check that title has Service Subscriptions text in Service Subscriptions page."
        )
        expect(
            self.page.locator(ServiceSubscriptionsSelectors.SERVICE_SUBSCRIPTIONS_TITLE)
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

    def should_have_column_type(self, column_name):
        """
        Check the presence of a column with a given name in the service subscriptions table
        :return: current instance of Service Subscriptions page object.
        """
        log.info(
            f'Playwright: checking the presence of "{column_name}" column in the service subscriptions table'
        )
        expect(
            self.page.locator(
                ServiceSubscriptionsSelectors.TABLE_COLUMN_TEMPLATE.format(column_name)
            )
        ).to_be_visible()
        return self

    def should_have_subscription_submit_error(self):
        """
        Verifies an error message presence in the add subscription popup
        :return: current instance of Service Subscriptions page object.
        """
        log.info("Playwright checking failure state of adding subscription key")
        expect(self.page.locator(ServiceSubscriptionsSelectors.ERROR_MSG)).to_be_visible()
        return self

    def should_subscription_details_dialog_be_visible(self):
        """
        Checks for the exisntence of an opened service details dialog
        :return: current instance of Service Subscriptions page object.
        """
        log.info("Playwright checking the presense of service subscription dialog box")
        expect(
            self.page.locator(ServiceSubscriptionsSelectors.SERVICE_DETAIL_DIALOG)
        ).to_be_visible()
        return self
