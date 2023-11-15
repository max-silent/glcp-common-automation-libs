"""
Authorization app apis
"""
import logging

log = logging.getLogger()
from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession


class AuthorizationApp(AppSession):
    def __init__(self, host, sso_host, client_id, client_secret):
        super(AuthorizationApp, self).__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/authorization/app"
        self.api_version = "/v1"

    def get_user_application_role_assignments(self, application_cid, username):
        """
        Retrieve all role assignments for a user and a single application.
        :param application_cid:  Application Customer id
        :param username: username of glcp platform
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/customers/{application_cid}/users/{username}"
            log.debug(f"{url}")
            res = self.get(url=url)
            log.debug(
                f"response of role assignment for a user and a single application: {res}"
            )
            return res
        except:
            log.error(
                "\nException in while getting all role assignments for a user and a single application \n"
            )
