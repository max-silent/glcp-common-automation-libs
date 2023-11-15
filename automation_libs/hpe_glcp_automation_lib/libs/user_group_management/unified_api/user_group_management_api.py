"""
User group management unified apis
"""
import logging

from hpe_glcp_automation_lib.libs.commons.unified_api.unified_api import UnifiedSession

log = logging.getLogger(__name__)


class UserGroupManagement(UnifiedSession):
    """
    User Group Management API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret, scope="read write"):
        """
        Initialize UserGroupManagement class
        :param host: cluster under test api url
        :param sso_host: sso_host url
        :param client_id: api client_id
        :param client_secret: api client secret
        """
        log.info("Initializing user_group_management_api for unified api calls")
        super().__init__(host, sso_host, client_id, client_secret, scope=scope)
        self.base_path = "/organizations"
        self.api_version = "/v2alpha1/scim/v2"

    def list_groups(self, **kwargs):
        """
        API: GET "/organizations/v2alpha1/scim/v2/Groups"
        :param **kwargs: for postive/negative test params
        :return: json response
        """
        url_groups = f"{self.base_url}{self.base_path}{self.api_version}/Groups"
        resp = self.get(url=url_groups, **kwargs)
        return resp
