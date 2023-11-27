import logging

import pyotp
from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.authn.ui.locators import LoginPageSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_home_page import TacHomePage
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage

log = logging.getLogger(__name__)


class Login(BasePage):
    """
    Login Page object methods

    """

    def __init__(self, page: Page, cluster: str):
        log.info("Initialize Login page object")
        super().__init__(page, cluster)

    def login_acct(self, username, password, account_name=None, remember_me=False):
        """Method used for logging in based on credentials

        :param username: str - User's email
        :param password: str - User's password
        :param account_name: str - User's account name, if user has several accounts (optional)
        :param remember_me: bool - True/False to check remeber_me checkbox (optional)
        :return: Choose Account (if user has several accounts) or Home Page (if only one account available) object
        """
        log.info(f"Login by '{username}'.")
        self._login_account(username, password, remember_me)
        self.pw_utils.wait_for_url(
            f"{self.cluster}/onboarding/choose-account", timeout_ignore=True
        )
        if account_name:
            return ChooseAccount(self.page, self.cluster)
        else:
            self.page.wait_for_load_state("domcontentloaded")
            return HomePage(self.page, self.cluster)

    def sso_login(self, username, okta_password, device_id, account_name=None):
        """Method used for SSO Login

        :param username: str - User's email
        :param okta_password: str - Okta password
        :param device_id: str - device id for google authenticator code
        :param account_name: str - User's account name, if user has several accounts (optional)
        :return: Choose Account (if user has several accounts) or Home Page (if only one account available) object
        """
        log.info(f"SSO Login by '{username}'.")
        self.page.click(LoginPageSelectors.SSO_SIGN_IN)
        self.page.fill(LoginPageSelectors.SSO_EMAIL_INPUT, username)
        self.page.click(LoginPageSelectors.NEXT_BUTTON)
        if self.pw_utils.wait_for_selector(
            LoginPageSelectors.OKTA_EMAIL_INPUT, timeout_ignore=True
        ):
            self.page.fill(LoginPageSelectors.OKTA_EMAIL_INPUT, username)
            if self.page.locator(LoginPageSelectors.OKTA_PASSCODE_INPUT).is_visible():
                self.page.fill(LoginPageSelectors.OKTA_PASSCODE_INPUT, okta_password)
                self.page.click(LoginPageSelectors.OKTA_SIGN_IN_BTN)
            else:
                self.page.locator(LoginPageSelectors.OKTA_NEXT_BTN).click()
                self.page.locator(LoginPageSelectors.OKTA_PASSWORD_SELECT).click()
                self.page.fill(LoginPageSelectors.OKTA_PASSCODE_INPUT, okta_password)
                self.page.click(LoginPageSelectors.VERIFY_BUTTON)
            self.page.wait_for_selector(LoginPageSelectors.OKTA_FORM_TITLE)
            otp = pyotp.TOTP(device_id).now()
            self.page.fill(LoginPageSelectors.OKTA_PASSCODE_INPUT, otp)
            self.page.click(LoginPageSelectors.VERIFY_BUTTON)
        if account_name:
            return ChooseAccount(self.page, self.cluster)
        else:
            return HomePage(self.page, self.cluster)

    def login_acct_tac(self, username, password, account_name=None, remember_me=False):
        """Method used for logging in by TAC-user based on credentials.

        :param username: str - User's email.
        :param password: str - User's password.
        :param account_name: str - User's account name, if user has several accounts (optional).
        :param remember_me: bool - True/False to check remeber_me checkbox (optional)
        :return: ChooseAccount (if user has several accounts) or TacHomePage (if only one account available) object.
        """
        log.info(f"TAC: Login by '{username}'.")
        self._login_account(username, password, remember_me)
        if account_name:
            return ChooseAccount(self.page, self.cluster)
        else:
            return TacHomePage(self.page, self.cluster)

    def open(self):
        """Opens the Login page and verifies it is opened

        :return: the instance of itself
        """
        self.page.goto(self.cluster)
        self.page.wait_for_selector(LoginPageSelectors.EMAIL_ID_PATH)
        return self

    def send_reset_password_email(self, username):
        """Method used to reset the password.

        :param username: str - User's email.
        return: instance of Login POM.
        """
        self.page.click(LoginPageSelectors.NEED_HELP_SIGING_IN)
        self.page.click(LoginPageSelectors.FRGT_PASSWD)
        self.page.fill(LoginPageSelectors.ACC_RCVRY_USERNAME, username)
        self.page.click(LoginPageSelectors.RESET_VIA_EMAIL_BTN)
        self.page.click(LoginPageSelectors.BACK_TO_SIGN_BTN)
        return self

    def _login_account(self, username, password, remember_me=False):
        """Log in by user with provided credentials.

        :param username: str - User's email.
        :param password: str - User's password.
        :param remember_me: bool - True/False to check remeber_me checkbox (optional)
        """
        self.page.fill(LoginPageSelectors.EMAIL_ID_PATH, username)
        if remember_me:
            self.page.locator(LoginPageSelectors.REMEMBER_ME).check()
        self.page.locator(LoginPageSelectors.NEXT_BTN_PATH).click()
        self.page.fill(LoginPageSelectors.PASSWD_PATH, password)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(LoginPageSelectors.SUBMIT_PATH).click()

    def should_have_login_error_msg(self):
        """
        Verify that error msg appears on the screen after we fill Up the Wrong username and(or) password
        :return: self reference
        """
        self.page.wait_for_load_state()
        expect(self.page.locator(LoginPageSelectors.UNABLE_TO_SIGNIN)).to_be_visible()
        return self
