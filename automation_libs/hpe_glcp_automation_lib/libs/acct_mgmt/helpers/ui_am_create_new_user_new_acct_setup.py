"""
This file holds functions to set up new user and new account
"""
import json
import logging

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_account_page import CreateAcctPage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_page import CreateUserPage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.customer_account_page import (
    CustomerAccount,
)
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.customer_details_page import (
    CustomerDetails,
)
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.commons.utils.gmail.gmail_imap2 import GmailOps_okta
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)
USER_PASSWORD = "Aruba@123456789"


class HlpCreateUserCreateAcct:
    """
    Helper class to create user and account
    """

    def __init__(self, gmail_creds):
        self.gmail_user, self.gmail_passwd = gmail_creds
        log.info("Create new user")

    def svc_new_user_signup(self, page, hostname, random_email_id, end_username):
        """
        Creates new user; verifies the user and creates new account

        :param page: page instance
        :param hostname: target hostname
        :param random_email_id: e-mail id for the new user
        :param end_username: username for the new user
        """
        user = CreateUserData
        user.email, user.password, user.business_name = (
            random_email_id,
            USER_PASSWORD,
            end_username,
        )
        gmail_session = GmailOps_okta()

        CreateUserPage(page, hostname).open().create_user(user)
        log.info("going to check email in gmail account")
        verify_url = gmail_session.get_okta_verification_link(
            my_email=user.email,
            gmail_username=self.gmail_user,
            gmail_password=self.gmail_passwd,
        )
        log.info(f"opening browser for ui_api login")
        page.goto(verify_url)
        PwrightUtils(page).wait_for_url("*choose-account")
        CreateAcctPage(page, hostname).open().create_acct(
            user
        ).wait_for_loaded_state().nav_bar.navigate_to_manage()
        pcid = ManageAccount(page, hostname).get_pcid()

        if pcid:
            setup_info = {
                "url": hostname,
                "user": user.email,
                "password": USER_PASSWORD,
                "pcid": pcid,
            }
            # TODO: Find out, why for we are converting to string and after decoding again
            res_setup_info = json.dumps(setup_info)
            log.info("user creation successful with first account")
            return res_setup_info
        else:
            raise Exception("FAIL: first account is not created successfully")


class HlpOpenCustomerDetails:
    def __init__(self):
        log.info("Opening Customer Details page")

    @staticmethod
    def open_customer_details(page, hostname, customer_name):
        """
        Load the details for the specified customer

        :param page: Playwright Page object
        :param hostname: cluster under test
        :param customer_name: name of the customer whose details to be opened.
        :return: instance of Customer details page object.
        """
        customer_accounts = (
            CustomerAccount(page, hostname)
            .load_customer(customer_name)
            .wait_for_loaded_state()
        )
        customer_accounts.nav_bar.navigate_to_manage()
        manage_account_page = ManageAccount(page, hostname)
        pcid = manage_account_page.get_pcid()
        manage_account_page.nav_bar.navigate_to_dashboard()
        customer_accounts.wait_for_loaded_state().open_return_msp_account().wait_for_loaded_state().nav_bar.navigate_to_customers()
        customer_accounts.wait_for_loaded_state()
        customer_accounts.search_customer(customer_name)
        customer_accounts.open_customer_details_by_pcid(customer_name, pcid)
        return CustomerDetails(page, hostname, pcid)
