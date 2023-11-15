"""
Account Management APP API Library
"""

import logging

import requests

from automation_libs.hpe_glcp_automation_lib.libs.acct_mgmt.utils import (
    log_api_response,
    verify_response_type,
)
from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class AcctMgmtAppApi(AppSession):
    """
    Account Management APP API Class

    Note: The methods in this class are purposely setup with type hints and most are
    expected return a requests.Response object to allow test cases to get all data
    related to the API call. This helps with negative test cases and catching syntax
    errors in the IDE used for Python development.
    """

    def __init__(
        self, host: str, sso_host: str, client_id: str, client_secret: str, **kwargs
    ):
        """
        Initialize the Account-Management APP API class

        :param host: cluster under test app api url
        :param sso_host: sso_host url
        :param client_id: app api client_id
        :param client_secret: app api client secret
        """
        log.info("Initializing aop_app_api for user api calls")
        super().__init__(host, sso_host, client_id, client_secret, **kwargs)
        self.base_path = "/accounts/app"
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

    @log_api_response
    def get_users(self, **kwargs) -> requests.Response:
        """
        Return the users

        Returns: returns list of customer accounts
        """
        response = self.session.get(
            self.get_path("/users"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_usernames(self, **kwargs) -> requests.Response:
        """
        Return the users

        Returns: returns list of customer accounts
        """
        response = self.session.get(
            self.get_path("/users/usernames"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_user_from_username(self, username: str, **kwargs) -> requests.Response:
        """
        Returns: returns a list of details for a specific user
        """
        response = self.session.get(
            self.get_path(f"/users/{username}"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_customers(self, **kwargs) -> requests.Response:
        """
        Return the customers

        Returns: returns list of customer accounts
        """
        response = self.session.get(
            self.get_path("/customers"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)

    @log_api_response
    def get_customer_ids(self, **kwargs) -> requests.Response:
        """
        Return the customer IDs

        Returns: returns list of customer accounts
        """
        response = self.session.get(
            self.get_path("/customers/ids"), ignore_handle_response=True, **kwargs
        )

        return verify_response_type(response)
