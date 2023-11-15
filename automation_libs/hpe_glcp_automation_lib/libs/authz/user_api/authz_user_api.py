"""
Authz User API
"""
import json
import logging
import pprint
import time
from functools import wraps
from typing import Dict

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import (
    SessionException,
)
from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class AuthzUserApi(UISession):
    """
    Authz UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing authz for user api calls")
        super().__init__(host, user, password, pcid)
        self.base_path = "/authorization/ui"
        self.api_version = "/v1"

    def _log_response(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            log.debug(f"{' '.join(func.__name__.title().split('_'))} API Request")
            res = func(*args, **kwargs)
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response"
                + "\n\n"
                + pprint.pformat(res)
                + "\n"
            )
            return res

        return decorated_func

    @_log_response
    def role_assign(self, platform_cust_id, invited_username, role_data):
        """
        Create role in authz
        :param platform_cust_id: Platform Customer ID
        :param invited_username: username
        :param role_data: Details of the role to assign
        :return: response_code, response body
        """
        return self.put(
            f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/users/{invited_username}/roles",
            data=json.dumps(role_data),
        )

    @_log_response
    def role_assign_v2(self, invited_username, role_data):
        """
        Create role in authz
        :param platform_cust_id: Platform Customer ID
        :param invited_username: username
        :param role_data: Details of the role to assign
        :return: response_code, response body
        """
        return self.put(
            f"{self.base_path}/v2/customers/users/{invited_username}/roles",
            json=role_data,
        )

    @_log_response
    def role_unassign(self, platform_cust_id, user_name, application_id, role_slug):
        """
        Update an role in authz
        :param platform_cust_id: Platform Customer ID
        :param user_name: username
        :param application_id: Application ID
        :param role_slug: Details to update for the role
        :return: response_code, response body
        """
        role_data = {"delete": [{"application_id": application_id, "slug": role_slug}]}
        return self.put(
            f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/users/{user_name}/roles",
            data=json.dumps(role_data),
        )

    @_log_response
    def create_role_for_app(self, application_id, platform_cust_id, role_data):
        logging.info("role_data {}".format(role_data))
        return self.post(
            f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/applications/{application_id}/roles",
            data=json.dumps(role_data),
        )

    @_log_response
    def role_delete(self, platform_cid, application_id, role_slug):
        """
        Delete an role from authz
        :param platform_cid: Platform Customer ID
        :param application_id: Application ID
        :param role_slug: Slug for the role to delete
        :return: response_code, response body
        """
        return self.delete(
            f"{self.base_path}{self.api_version}/customers/{platform_cid}/applications/{application_id}/roles/{role_slug}"
        )

    @_log_response
    def ccs_get_role(self, platform_cust_id, secondary=None):
        """
        get ccs role
        :param platform_cid: Platform Customer ID
        :return: response_code, response body
        """
        if secondary:
            return self.get_secondary(
                f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/roles"
            )
        else:
            self.get(
                f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/roles"
            )

    @_log_response
    def app_get_role(self, platform_cust_id, application_id, secondary=None, params=None):
        """
        get app role
        :param platform_cid: Platform Customer ID
        :return: response_code, response body
        """
        if secondary:
            return self.get_secondary(
                f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/applications/{application_id}/roles",
                params=params,
                tuple_response=True,
            )
        else:
            return self.get(
                f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/applications/{application_id}/roles",
                params=params,
                tuple_response=True,
            )

    @_log_response
    def offboard_app(self, application_id):
        """
        Offboard an app id in authz
        :param application_id: Application ID
        :return: Response object
        """
        return self.delete(
            f"{self.base_path}{self.api_version}/applications/{application_id}",
            ignore_handle_response=True,
        )

    def _set_headers(self, headers: Dict) -> None:
        self.session.headers.update(headers)

    def _get_authn_path(self, path: str) -> str:
        base_path = "/authn"
        return f"{base_path}{self.api_version}/{path}"

    def get_credentials(self, cred_name: str) -> Dict[str, str]:
        get_credentials_path = self._get_authn_path("token-management/credentials")
        resp = self.get(get_credentials_path)
        for cred in resp:
            if cred["credential_name"] == cred_name:
                return cred
        return {}

    def create_credentials(self, payload: Dict[str, str]) -> Dict[str, str]:
        create_credentials_path = self._get_authn_path("token-management/credentials")
        # We have to put this "sleep" due to the credentials' API
        # rate limiting;
        time.sleep(1)
        self._set_headers({"Content-type": "application/json"})
        return self.post(
            create_credentials_path,
            data=json.dumps(payload),
        )

    def delete_credentials(self, cred_name: str) -> None:
        delete_credentials_path = self._get_authn_path(
            f"token-management/credentials/{cred_name}"
        )
        # We have to put this "sleep" due to the credentials' API
        # rate limiting;
        time.sleep(1)
        try:
            response = self.delete(delete_credentials_path)
            assert response.status_code == 204
        except SessionException as err:
            if err.response is not None and err.response.status_code == 412:
                raise err
