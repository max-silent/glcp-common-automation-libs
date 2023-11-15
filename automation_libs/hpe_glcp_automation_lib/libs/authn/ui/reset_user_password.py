"""
This file holds functions for Reset User Password page
"""

import logging
import time

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authn.ui.locators import ResetUserPasswordSelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.utils.gmail.gmail_imap2 import GmailOps_okta

log = logging.getLogger(__name__)


class ResetUserPwd(BasePage):
    """
    Reset User Password Page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Reset User Pwd page object")
        super().__init__(page, cluster)

    def send_reset_password_link(self, username):
        """
        Sends reset password link to the username

        :param username: User's email
        """
        self.page.goto(self.cluster)
        self.page.locator(ResetUserPasswordSelectors.NEED_HELP).click()
        self.page.locator(ResetUserPasswordSelectors.FORGOT_PASSWORD).click()
        self.page.locator(ResetUserPasswordSelectors.ACCOUNT_RECOVERY_USERNAME).fill(
            username
        )
        self.page.locator(ResetUserPasswordSelectors.REST_VIA_EMAIL).click()
        self.pw_utils.save_screenshot(self.test_name)
        log.info(f"Playwright: Reset link has been emailed to {username}")

    def reset_password(self, gmail_username, gmail_password, new_passwd):
        """
        Reset glcp user password (Only gmail account)

        :param gmail_username: User's gmail id
        :param gmail_password: User's gmail api password
        :param new_passwd: new password
        """
        log.info(f"Playwright: Reset {gmail_username} password")
        gmail_session = GmailOps_okta()
        self.send_reset_password_link(gmail_username)
        time.sleep(30)
        reset_link = gmail_session.get_okta_password_reset_link(
            gmail_username,
            gmail_username,
            gmail_password,
        )
        if reset_link == None:
            raise Exception("Playwright: No Reset link found!")
        self.page.goto(reset_link)
        self.page.locator(ResetUserPasswordSelectors.NEW_PASSWD_PATH).fill(new_passwd)
        self.page.locator(ResetUserPasswordSelectors.REPEAT_PASSWD_PATH).fill(new_passwd)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(ResetUserPasswordSelectors.RESET_PASSWD_BUTTON).click()
        return self
