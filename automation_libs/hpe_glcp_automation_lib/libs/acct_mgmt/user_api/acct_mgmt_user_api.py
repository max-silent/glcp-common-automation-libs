"""
Account Management UI API Library
"""
import logging
from typing import Any, Optional

import requests

from hpe_glcp_automation_lib.libs.acct_mgmt.utils import (
    log_api_response,
    verify_response_type,
)
from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class AcctMgmtUserApi(UISession):
    """
    Account Management UI API Class

    Note: The methods in this class are purposely setup with type hints and most are
    expected return a requests.Response object to allow test cases to get all data
    related to the API call. This helps with negative test cases and catching syntax
    errors in the IDE used for Python development.
    """

    def __init__(self, host: str, user: str, password: str, pcid: str, **kwargs):
        """
        Initialize the Account-Management UI API class

        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID
        """
        log.info("Initializing acct_mgmt for user api calls")
        super().__init__(host, user, password, pcid, **kwargs)
        self.base_path = "/accounts/ui"
        self.api_version = "/v1"

    def get_path(self, subpath: str) -> str:
        """
        Get the full path for the api using the base path and sub-path

        Args:
            path (str): Path for the API (ex. /users)

        Returns:
            str: The full path for the API (ie. /accounts/ui/users)
        """
        path_args = [a.strip("/") for a in [self.base_path, self.api_version, subpath]]
        return "/" + "/".join(path_args)

    def get_account_contact(self, secondary=None):
        if secondary:
            return self.get_secondary(
                f"{self.base_path}{self.api_version}/customer/profile/contact"
            )
        else:
            return self.get(
                f"{self.base_path}{self.api_version}/customer/profile/contact"
            )

    @log_api_response
    def get_status(self, **kwargs) -> requests.Response:
        """
        ARGS: session
        Returns: returns list of customer accounts
        """
        response = self.get(
            self.get_path("/status"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_users(
        self, offset: int = 0, count_per_page: Optional[int] = 300, **kwargs
    ) -> requests.Response:
        """
        ARGS: session
        Returns: returns list of customer accounts
        """
        subpath = f"/user?offset={offset}"
        if count_per_page is not None:
            subpath += f"&count_per_page={count_per_page}"

        response = self.get(
            self.get_path(subpath=subpath), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_user_details(self, username: str, **kwargs) -> requests.Response:
        """
        ARGS: session, username
        Returns: returns details of a particular user on platform account
        """
        subpath = f"/user/details?"
        subpath += f"&email={username}"

        response = self.get(self.get_path(subpath=subpath), ignore_handle_response=True)

        return verify_response_type(response)

    @log_api_response
    def get_user_preferences(self, **kwargs) -> requests.Response:
        """
        Get the user preferences
        """
        api_path = "user/profile/preferences"
        response = self.get(
            self.get_path(api_path), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def update_user_preferences(self, payload: Any, **kwargs) -> requests.Response:
        """
        Update the user preferences
        """
        api_path = "user/profile/preferences"
        response = self.put(
            self.get_path(api_path), json=payload, ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def update_contact_info(self, username: str, **kwargs) -> requests.Response:
        """
        Update details of a user

        Args:
            user (str): Username of the user

        Raises:
            TypeError: If returned object is not requests.Response

        Returns:
            requests.Response: Response from the API server
        """
        payload = {"email": username, **kwargs}
        response = self.put(
            self.get_path(f"user/profile/contact"),
            json=payload,
            ignore_handle_response=True,
        )

        return verify_response_type(response)

    @log_api_response
    def get_contact_info(self, **kwargs) -> requests.Response:
        """
        Get details of a user

        Args:
            user (str): Username of the user

        Raises:
            TypeError: If returned object is not requests.Response

        Returns:
            requests.Response: Response from the API server
        """
        response = self.get(
            self.get_path(f"user/profile/contact"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def invite_user(
        self, username: str, welcome_email: bool = True, **kwargs
    ) -> requests.Response:
        """
        Invite a user
        """
        response = self.post(
            self.get_path(f"user/invite/{username}?welcome_email={welcome_email}"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def signup_user(self, username: str, **kwargs) -> requests.Response:
        """
        Signup a user
        """
        payload = {"email": username, **kwargs}
        response = self.post(
            self.get_path(f"user/signup"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def set_password_user(
        self, verification_hash: str, password: str, **kwargs
    ) -> requests.Response:
        """
        Set a new password for the user
        """
        payload = {
            "verification_hash": verification_hash,
            "password": password,
        }
        response = self.post(
            self.get_path("user/password"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def change_password_user(
        self, old_password: str, new_password: str, **kwargs
    ) -> requests.Response:
        """
        Change password for the user
        """
        payload = {
            "old_password": old_password,
            "new_password": new_password,
        }
        response = self.post(
            self.get_path("user/password-change"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def forgot_password_user(self, username: str, **kwargs) -> requests.Response:
        """
        Forgot password for the user
        """
        response = self.post(
            self.get_path(f"user/password-recovery/{username}"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def reset_password_user(
        self, verification_hash: str, password: str, **kwargs
    ) -> requests.Response:
        """
        Reset password for the user
        """
        payload = {
            "verification_hash": verification_hash,
            "password": password,
        }
        response = self.post(
            self.get_path("user/password-reset"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def disassociate_user(self, username: str, **kwargs) -> requests.Response:
        """
        Disassociate a user
        """
        response = self.delete(
            self.get_path(f"user/disassociate/{username}"), ignore_handle_response=True
        )

        return verify_response_type(response)

    @log_api_response
    def check_msp_eligibility(self, payload: dict, **kwargs) -> requests.Response:
        """
        Convert a standalone account to an MSP
        """
        response = self.post(
            self.get_path("managed-service/eligibility/details"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def convert_msp(self, **kwargs) -> requests.Response:
        """
        Convert a standalone account to an MSP
        """
        response = self.patch(
            self.get_path("managed-service/toggle-msp"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def signup_customer(self, payload: dict, **kwargs) -> requests.Response:
        """
        Signup a customer

        Args:
            payload (dict): Data to send to signup the customer

        Returns:
            requests.Response: API response
        """
        subpath = "/customer/signup"

        response = self.post(
            self.get_path(subpath=subpath),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def get_customer_user_accounts(self, **kwargs) -> requests.Response:
        """
        Get customer's user accounts
        """
        subpath = "/customer/user-accounts"

        response = self.get(
            self.get_path(subpath=subpath), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_customer_accounts(
        self,
        offset: int = 0,
        count_per_page: Optional[int] = 300,
        ignore_current_account: bool = False,
        **kwargs,
    ) -> requests.Response:
        """
        Get customer accounts for the user
        """
        subpath = f"/customer/list-accounts?offset={offset}"
        if count_per_page is not None:
            subpath += f"&count_per_page={count_per_page}"

        subpath += f"&sort_by=RECENT_ACCESSED"
        subpath += f"&ignore_current_account={ignore_current_account}"

        response = self.get(
            self.get_path(subpath=subpath), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_tenant_accounts(
        self,
        offset: int = 0,
        count_per_page: Optional[int] = None,
        ignore_current_account: bool = False,
        **kwargs,
    ) -> requests.Response:
        """
        Get customer accounts for the user
        """
        subpath = f"/managed-service/tenants?offset={offset}"
        if count_per_page is not None:
            subpath += f"&count_per_page={count_per_page}"

        subpath += f"&ignore_current_account={ignore_current_account}"

        response = self.get(
            self.get_path(subpath=subpath), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_customer_contact(self, **kwargs) -> requests.Response:
        response = self.get(
            self.get_path(f"/customer/profile/contact"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def update_customer_contact(self, payload: dict, **kwargs) -> requests.Response:
        response = self.put(
            self.get_path(f"/customer/profile/contact"),
            ignore_handle_response=True,
            json=payload,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def get_customer_preferences(self, **kwargs) -> requests.Response:
        """
        Get the customer account preferences
        """
        response = self.get(
            self.get_path(f"customer/profile/preferences"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def update_customer_preferences(self, payload: dict, **kwargs) -> requests.Response:
        """
        Update the customer account preferences
        """
        response = self.put(
            self.get_path(f"customer/profile/preferences"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def update_customer_info(self, **kwargs) -> requests.Response:
        """
        Update profile contact details of customer

        Args:
            user (str): Username of the user

        Raises:
            TypeError: If returned object is not requests.Response

        Returns:
            requests.Response: Response from the API server
        """
        payload = {**kwargs}
        response = self.put(
            self.get_path(f"customer/profile/contact"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def get_customer_info(self, **kwargs) -> requests.Response:
        """
        Get profile contact details of customer

        Args:
            user (str): Username of the user

        Raises:
            TypeError: If returned object is not requests.Response

        Returns:
            requests.Response: Response from the API server
        """
        response = self.get(
            self.get_path(f"customer/profile/contact"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def enable_customer_mfa(self, **kwargs) -> requests.Response:
        """
        Enable multi-factor-authentication (MFA) for the customer
        """
        response = self.post(
            self.get_path(f"customer/mfa/enable"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def disable_customer_mfa(self, **kwargs) -> requests.Response:
        """
        Disable multi-factor-authentication (MFA) for the customer
        """
        response = self.post(
            self.get_path(f"customer/mfa/disable"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def enable_user_mfa(self, **kwargs) -> requests.Response:
        """
        Enable multi-factor-authentication (MFA) for the user
        """
        response = self.post(
            self.get_path(f"user/mfa/enable"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def disable_user_mfa(self, **kwargs) -> requests.Response:
        """
        Disable multi-factor-authentication (MFA) for the user
        """
        response = self.post(
            self.get_path(f"user/mfa/disable"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def active_user_mfa(self, payload: dict, **kwargs) -> requests.Response:
        """
        Active multi-factor-authentication (MFA) for the user
        """
        response = self.post(
            self.get_path(f"user/mfa/activate"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def initiate_reset_user_mfa(self, payload: dict, **kwargs) -> requests.Response:
        """
        Initiate reset multi-factor-authentication (MFA) for the user
        """
        response = self.post(
            self.get_path(f"user/mfa/initiate-reset"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def reset_user_mfa(self, payload: dict, **kwargs) -> requests.Response:
        """
        Reset multi-factor-authentication (MFA) for the user
        """
        response = self.post(
            self.get_path(f"user/mfa/reset"),
            json=payload,
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def get_tenant(self, customer_id: str, **kwargs) -> requests.Response:
        """
        Fetch a Managed Service Tenant details

        Returns: tenant details
        """
        log.info(f"Get the tenant: {customer_id}")
        response = self.get(
            self.get_path(f"managed-service/tenant/{customer_id}"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def create_tenant(self, payload: dict, **kwargs) -> requests.Response:
        """
        Create the tenant account for an MSP

        Returns: returns list of customer accounts
        """
        company_name = payload.get("company_name", "")
        log.info(f"Creating the tenant: {company_name}")
        response = self.post(
            self.get_path("managed-service/tenant"),
            ignore_handle_response=True,
            json=payload,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def remove_tenant(self, tenant_id: str, **kwargs) -> requests.Response:
        """
        Remove the tenant account for an MSP
        """
        log.info(f"Removing the tenant: {tenant_id}")
        response = self.delete(
            self.get_path(f"managed-service/tenant/{tenant_id}"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def create_ip_access_rule(self, payload: dict, **kwargs) -> requests.Response:
        """
        Return the customer IDs

        Returns: returns list of customer accounts
        """
        response = self.post(
            self.get_path("/ip-access-rule"),
            ignore_handle_response=True,
            json=payload,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def get_ip_access_rule(
        self, offset: int = 0, count_per_page: Optional[int] = 300, **kwargs
    ) -> requests.Response:
        """
        Get IP access rules
        """
        subpath = f"/ip-access-rule?offset={offset}"
        if count_per_page is not None:
            subpath += f"&count_per_page={count_per_page}"

        response = self.get(
            self.get_path(subpath=subpath), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def remove_ip_access_rule(self, payload: list = [], **kwargs) -> requests.Response:
        """
        Remove all IP access rules passed by parameter.
        """
        log.info(f"Removing the rules: {payload}")
        response = self.delete(
            self.get_path(f"/ip-access-rule"),
            ignore_handle_response=True,
            json=payload,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def toggle_ip_access_rule(self, enable: bool = False, **kwargs) -> requests.Response:
        """
        Enable/Disable all IP access rules.
        """
        log.info("Toggling the IP access rules")
        response = self.put(
            self.get_path(f"/ip-access-rule/toggle?enable={enable}"),
            ignore_handle_response=True,
            **kwargs,
        )

        return verify_response_type(response)

    @log_api_response
    def update_ip_access_rule(
        self, ip_access_rule_id: str, payload: dict, **kwargs
    ) -> requests.Response:
        """
        Update the IP access rule
        """
        response = self.put(
            self.get_path(f"/ip-access-rule?ip_access_rule_id={ip_access_rule_id}"),
            ignore_handle_response=True,
            json=payload,
            **kwargs,
        )

        return verify_response_type(response)
