"""
This file holds library methods for User Profile
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import (
    CreateUserData,
    PasswordData,
)
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import UserProfileSelectors
from hpe_glcp_automation_lib.libs.authn.ui.enroll_page import Enroll
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class UserProfile(BasePage):
    """
    Class that holds the methods to access user profile page
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize User Profile page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/profile/UserProfile"

    def wait_for_loaded_state(self):
        """
        Wait till page is loaded and loading spinner is not present.
        :return: current instance of UserProfile page object.
        """
        log.info("Playwright: wait for UserProfile page is loaded.")
        self.page.wait_for_url(self.url)
        self.page.locator(UserProfileSelectors.LOADER_SPINNER).wait_for(state="hidden")
        return self

    def update_password(self, passwd_data: PasswordData = PasswordData):
        """
        Update user password
        param user_data: password edit for existing customer
        e.g. current_password, new_password, etc.
        """
        log.info("Playwright: Changing the password")
        self.pw_utils.click_selector(UserProfileSelectors.PASSWORD_EDIT_BTN)
        self.page.fill(
            UserProfileSelectors.CURRENT_PASSWORD, passwd_data.current_password
        )
        self.page.fill(UserProfileSelectors.NEW_PASSWORD, passwd_data.new_password)
        self.page.fill(
            UserProfileSelectors.CONFIRM_NEW_PASSWORD, passwd_data.new_password
        )
        self.pw_utils.save_screenshot(self.test_name)
        self.page.click(UserProfileSelectors.CHANGE_PASSWORD_BTN)
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def update_personal_information(self, user_data: CreateUserData = CreateUserData):
        """
         Updates the personal information

        :param user_data: e.g. email, password, address, phone etc.
        """
        log.info("Updating the user personal information")
        self.pw_utils.click_selector(UserProfileSelectors.PERSONAL_EDIT_INFO_BTN)
        self.page.fill(UserProfileSelectors.FIRST_NAME, user_data.first_name)
        self.page.fill(UserProfileSelectors.LAST_NAME, user_data.last_name)
        self.page.fill(UserProfileSelectors.ORGANISATION_NAME, user_data.business_name)
        self.page.fill(UserProfileSelectors.STREET_ADDRESS, user_data.street_address)
        self.page.fill(UserProfileSelectors.STREET_ADDRESS2, user_data.street_address2)
        self.page.fill(UserProfileSelectors.INPUT_CITY, user_data.city_name)
        self.page.fill(UserProfileSelectors.STATE_PROVINCE, user_data.state_or_province)
        self.page.fill(UserProfileSelectors.POSTAL_CODE, user_data.postal_code)
        self.pw_utils.select_drop_down_element(
            UserProfileSelectors.COUNTRY_BTN,
            user_data.country,
            UserProfileSelectors.COUNTRY_ELEMENT_ROLE,
        )
        self.pw_utils.select_drop_down_element(
            UserProfileSelectors.SELECT_LANG,
            user_data.language,
            UserProfileSelectors.SELECT_LANG_ROLE,
        )
        self.page.locator(UserProfileSelectors.PRIMARY_PHONE).fill(user_data.phone_number)
        self.page.locator(UserProfileSelectors.MOBILE_PHONE).fill(user_data.phone_number)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.click(UserProfileSelectors.SAVE_INFO_BTN)
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def toggle_mfa(self):
        """
        Enable/Disable Multi-factor Authentication at user level
        :return: Userprofile page Object instance
        """
        log.info("Toggling MFA")
        self.pw_utils.click_selector(UserProfileSelectors.MFA_TOGGLE_BTN)
        return self

    def open_okta_setup(self):
        """
        Opens up the Okta setup page
        """
        log.info("Select Okta Setup")
        self.pw_utils.click_selector(UserProfileSelectors.OKTA_VERIFY_SETUP_BTN)
        self.page.wait_for_load_state("domcontentloaded")
        return Enroll(self.page, self.cluster)

    def open_google_auth_setup(self):
        """
        Opens up the Google Auth setup page
        """
        log.info("Select Google Auth Setup")
        self.pw_utils.click_selector(UserProfileSelectors.GOOGLE_AUTH_VERIFY_SETUP_BTN)
        self.page.wait_for_load_state("domcontentloaded")
        return Enroll(self.page, self.cluster)

    def remove_google_auth_setup(self):
        """
        Remove Google Authenticator setup
        """
        log.info("Select Google Auth Remove button")
        self.pw_utils.click_selector(UserProfileSelectors.GOOGLE_AUTH_REMOVE_BTN)
        self.page.wait_for_load_state("networkidle")
        self.pw_utils.wait_for_selector(UserProfileSelectors.GOOGLE_AUTH_VERIFY_SETUP_BTN)
        return self

    def remove_okta_setup(self):
        """
        Remove Okta setup.
        Due to bug: https://hpe.atlassian.net/browse/GLCP-45923, please use this function twice to remove okta setup
        """
        log.info("Select Okta Remove button")
        self.pw_utils.click_selector(UserProfileSelectors.OKTA_REMOVE_BTN)
        self.page.wait_for_load_state("networkidle")
        self.pw_utils.wait_for_selector(UserProfileSelectors.OKTA_VERIFY_SETUP_BTN)
        return self

    def should_have_mfa(self, checked=True):
        """
        Check that MFA field with status checked or unchecked
        :return: Userprofile page Object instance
        """
        log.info(f"Playwright: Check that MFA Checked status is {checked}")
        if checked:
            expect(self.page.locator(UserProfileSelectors.MFA_TOGGLE_BTN)).to_be_checked()
        else:
            expect(
                self.page.locator(UserProfileSelectors.MFA_TOGGLE_BTN)
            ).not_to_be_checked()
        return self
