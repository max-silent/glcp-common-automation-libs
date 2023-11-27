"""
This file holds functions for Account type page
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.check_eligibility_page import (
    CheckEligibility,
)
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import AccountTypeSelectors
from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class AccountType(HeaderedPage):
    """
    Class for converting standard account to MSP account and vice versa
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Account Type page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/account-type-overview"

    def open_check_eligibility(self):
        """
        Opens the Check Eligibility page
        :return: Instance of Check Eligibility page
        """
        self.page.locator(AccountTypeSelectors.CHECK_ELIGIBILITY_BUTTON).click()
        return CheckEligibility(self.page, self.cluster)

    def convert_account_type(self, to_msp=False):
        """
        Converts Standard to MSP and vice-versa
        :param to_msp: True when the conversion is to MSP
        :return: Login page instance
        """
        log.info("Converting account type")

        if to_msp:
            self.page.wait_for_selector(AccountTypeSelectors.ELIGIBILITY_HEADER)

            # Check if eligible button is available
            if self.page.locator(
                AccountTypeSelectors.CHECK_ELIGIBILITY_BUTTON
            ).is_visible():
                # step - 01: Check eligibility
                check_eligible = self.open_check_eligibility().wait_for_loaded_state()
                check_eligible.perform()

        # Convert account type
        self.page.locator(AccountTypeSelectors.CONVERT_ACCT_BUTTON).click()

        # Confirm conversion
        self.page.locator(AccountTypeSelectors.CONFIRM_CONVERT_BUTTON).click()

        return Login(self.page, self.cluster)

    def go_back_to_manage_workspace(self):
        """
        Navigate back to manage account page
        """
        log.info(f"Playwright: Navigating to manage account page")
        self.page.click(AccountTypeSelectors.BACK_TO_MANAGE_BUTTON)
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of  Account Type page object.
        """
        log.info(
            f"Playwright: check that title has matched text '{text}' in Account Type page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(AccountTypeSelectors.MANAGE_WORKSPACE_TITLE)
        ).to_have_text(text)
        return self

    def should_have_remove_unsupported_service_button_error_msg(self):
        """
        Verify account_type.step_remove_unsupported_service_button_text on account-type-overview page.
        :return: current instance of Account Type page object.
        """
        log.info(
            "Playwright: check that account_type.step_remove_unsupported_service_button message is visible at "
            "Account Type page."
        )
        expect(
            self.page.locator(AccountTypeSelectors.STEP_REMOVE_UNSUPPORTED_SERVICE_BUTTON)
        ).to_be_visible()
        return self

    def should_have_review_customer_workspaces_button(self):
        """
        Check that Review Workspace button is present at the page.
        :return: current instance of Account Type page object.
        """
        log.info("Playwright: Verifying Review Workspace button on Account type page.")
        expect(
            self.page.locator(AccountTypeSelectors.REVIEW_CUST_WORKSPACES)
        ).to_be_visible()
        return self
