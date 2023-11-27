"""
This file holds library methods for enroll while signing in
"""
import logging

import pyotp
from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authn.ui.locators import EnrollSelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class Enroll(BasePage):
    """
    Class that holds the methods to access Enroll Page
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Enroll page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/signin/enroll"
        self.okta_device_id = None
        self.gauth_device_id = None

    def setup_okta(self):
        """
        Setting Up OKTA manually without push notification
        :param: None
        :return: Enroll page object instance
        """
        log.info("Setting Up OKTA")
        self.page.click(EnrollSelectors.OKTA_SETUP_BTN)
        self.page.click(EnrollSelectors.ANDROID_RADIO_BTN)
        self.page.click(EnrollSelectors.NEXT_BTN)
        self.page.click(EnrollSelectors.CANT_SCAN)
        self.page.click(EnrollSelectors.ACTIVATION_TYPE_DROPDOWN)
        self.page.locator(EnrollSelectors.ACTIVATION_TYPE_OPTION).nth(1).click()
        self.page.wait_for_load_state("networkidle")
        self.okta_device_id = self.page.locator(
            EnrollSelectors.SHARED_SECRET_FIELD
        ).input_value()
        log.info(f"Device secret id : {self.okta_device_id}")
        self.pw_utils.save_screenshot(self.test_name)
        otp = self.get_otp(self.okta_device_id)
        self.page.click(EnrollSelectors.OKTA_PUSH_NEXT_BTN)
        self.page.locator(EnrollSelectors.PASSCODE_INPUT_FIELD).fill(otp)
        self.page.click(EnrollSelectors.VERIFY_BTN)
        return self

    def setup_google_auth(self):
        """
        Setting Up Google authentication manually without push notification
        :param: None
        :return: Enroll page object instance
        """
        log.info("Setting Up Google Authenticator")
        self.page.click(EnrollSelectors.GOOGLE_AUTH_SETUP_BTN)
        self.page.click(EnrollSelectors.ANDROID_RADIO_BTN)
        self.page.click(EnrollSelectors.NEXT_BTN)
        self.page.click(EnrollSelectors.CANT_SCAN)
        self.gauth_device_id = self.page.locator(
            EnrollSelectors.SHARED_SECRET_FIELD
        ).input_value()
        log.info(f"Device secret id : {self.gauth_device_id}")
        self.pw_utils.save_screenshot(self.test_name)
        otp = self.get_otp(self.gauth_device_id)
        self.page.click(EnrollSelectors.NEXT_BTN)
        self.page.locator(EnrollSelectors.PASSCODE_INPUT_FIELD).fill(otp)
        self.page.click(EnrollSelectors.VERIFY_BTN)
        return self

    def get_otp(self, device_id):
        """
        Generating OTP for the given device_id
        :param: device_id
        :return: OTP
        """
        totp = pyotp.TOTP(device_id)
        otp = f"{totp.now()}"
        return otp
