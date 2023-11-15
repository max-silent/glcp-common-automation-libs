import logging

from hpe_glcp_automation_lib.glp_featured_services.management_governance.opsramp.api.payload import (
    OpsrampConstantPayload,
)
from hpe_glcp_automation_lib.libs.commons.unified_api.unified_api import UnifiedSession

log = logging.getLogger(__name__)


class OpsRampUserGroupApiCalls(UnifiedSession):
    """
    OpsRampUserGroupApiCalls page object model class.
    """

    def __init__(self, app_api_host, sso_host, client_id, client_secret, tenant_id):
        """
        Initialize Opsramp User Group Api class
        :param app_api_host: CCS Unified API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param tenant_id: tenant_id
        """
        log.info("Initializing opsramp user api calls")
        super().__init__(app_api_host, sso_host, client_id, client_secret)
        self.scope = "global:manage"
        self.base_path = "api"
        self.api_version = "v2"
        self.tenant_id = tenant_id
        self.url = f"{self.base_url}/{self.base_path}/{self.api_version}/tenants/{self.tenant_id}"

    def create_user_group(self, name, description, email):
        """
        creating user group
        param: name
        param: description
        param: email
        returns: returns the response
        """
        log.info("Initializing Api call for creating user group")
        data = OpsrampConstantPayload.create_user_group_data(name, description, email)
        url = f"{self.url}/" + "userGroups"
        log.info(f"url :{url}")
        response = self.post(url, json=data, ignore_handle_response=True)
        if response.status_code == 200:
            create_user_group_response = response.json()
            log.info(f"response :{create_user_group_response}")
            return create_user_group_response
        else:
            log.error(f"response error code :{response.status_code}")
            return None

    def get_user_group_details(self, user_group_id):
        """
        Getting the user group details
        param: user_group_id
        returns: returns the response
        """
        log.info("Initializing Api call for getting user group details")
        url = f"{self.url}/userGroups/" + user_group_id + "/users"
        log.info(f"url: {url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            get_user_group_response = response.json()
            log.info(f"response: {get_user_group_response}")
            return get_user_group_response
        else:
            log.error(f"response error code: {response.status_code}")

    def fetch_user_group(self):
        """
        Searching the user group
        return: returns the response
        """
        log.info("Initializing Api call for searching user group")
        url = f"{self.url}/userGroups"
        log.info(f"url: {url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            search_user_group_response = response.json()
            log.info(f"response: {response.status_code}")
            return search_user_group_response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def add_user_to_user_group(self, user_id, user_group_id):
        """
        Add user to user group
        param: user_id
        param: user_group_id
        return: returns the response
        """
        log.info("Initializing Api call for adding user to user group")
        url = f"{self.url}/userGroups/" + user_group_id + "/users"
        log.info(f"url: {url}")
        response = self.post(url, json=user_id, ignore_handle_response=True)
        if response.status_code == 200:
            log.info(f"response: {response.status_code}")
            return response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def delete_user_from_user_group(self, user_group_id, user_id):
        """
        Deletes the user from user group
        param: user_group_id
        param: user_id
        return: returns the response
        """
        log.info("Initializing Api call for deleting user from user group")
        url = f"{self.url}/userGroups/" + user_group_id + "/users"

        log.info(f"url: {url}")
        response = self.delete(url, json=user_id, ignore_handle_response=True)
        if response.status_code == 200:
            log.info(f"response: {response.status_code}")
            return response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def delete_user_group(self, user_group_id):
        """
        Deletes the user_group
        param: user_group_id
        return: returns the response
        """
        log.info("Initializing Api call for deleting user group")
        url = f"{self.url}/userGroups/" + user_group_id
        log.info(f"url :{url}")
        response = self.delete(url, ignore_handle_response=True)
        if response.status_code == 200:
            log.info(f"response: {response.status_code}")
            return response
        else:
            log.error(f"response error code:{response.status_code}")
            return None
