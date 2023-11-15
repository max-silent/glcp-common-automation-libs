import logging

from hpe_glcp_automation_lib.glp_featured_services.management_governance.opsramp.api.payload import (
    OpsrampConstantPayload,
)
from hpe_glcp_automation_lib.libs.commons.unified_api.unified_api import UnifiedSession

log = logging.getLogger(__name__)


class OpsRampRolesApiCalls(UnifiedSession):
    """
    OpsRampRolesApiCalls page object model class.
    """

    def __init__(self, app_api_host, sso_host, client_id, client_secret, tenant_id):
        """
        Initialize Opsramp Roles Api class
        :param app_api_host: CCS Unified API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param tenant_id: tenant_id
        """
        log.info("Initializing opsramp roles api calls")
        super().__init__(app_api_host, sso_host, client_id, client_secret)
        self.scope = "global:manage"
        self.base_path = "api"
        self.api_version = "v2"
        self.tenant_id = tenant_id
        self.url = f"{self.base_url}/{self.base_path}/{self.api_version}/tenants/{self.tenant_id}"

    def create_role(self, name, description, scope):
        """
        Creating a role in opsramp
        param: name of the role
        param: description of the role
        param: scope of the role
        return: returns the response
        """
        log.info("Initializing Api call for create role")
        data = OpsrampConstantPayload.create_role_data(name, description, scope)
        url = f"{self.url}/" + "roles"
        log.info(f"url :{url}")
        response = self.post(url, json=data, ignore_handle_response=True)
        if response.status_code == 200:
            create_role_response = response.json()
            log.info(f"response {create_role_response}")
            return create_role_response
        else:
            log.error(f"response error code {response.status_code}")
            return None

    def assign_role(self, assign_role_data, role_id):
        """
        Assign role to user/user_group
        param: assign_role_data it may be either user_id/user_group_id
        param: role_id
        return: returns the response
        """
        log.info("Initializing Api call for assign role")
        url = f"{self.url}/roles/" + str(role_id)
        log.info(f"url :{url}")
        response = self.post(url, json=assign_role_data, ignore_handle_response=True)
        if response.status_code == 200:
            assign_role_response = response.json()
            log.info(f"response :{assign_role_response}")
            return assign_role_response
        else:
            log.error(f"error status code: {response.status_code}")
            return None

    def get_all_roles(self):
        """
        Fetch all the roles present in opsramp
        return: returns the response
        """
        log.info("Initializing Api call for search role")
        url = f"{self.url}/roles/search"
        log.info(f"url: {url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            search_role_response = response.json()
            log.info(f"response: {search_role_response}")
            return search_role_response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def get_role(self, role_id):
        """
        Fetching the details of specific role in opsramp.
        param: role_id: id of the role
        return: returns the response
        """
        log.info("Initializing Api call for get roles")
        url = f"{self.url}/roles/" + str(role_id)
        log.info(f"url: {url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            get_role_response = response.json()
            log.info(f"response: {get_role_response}")
            return get_role_response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def update_role(self, role_id, user_id):
        """
        Update the details of the role
        param: role_id: id of the role
        param: user_id: id of thr user
        return: returns the response
        """
        log.info("Initializing Api call for updating role")
        url = f"{self.url}/roles/" + str(role_id)
        log.info(f"url: {url}")
        response = self.post(url, json=user_id, ignore_handle_response=True)
        if response.status_code == 200:
            update_role_response = response.json()
            log.info(f"response: {update_role_response}")
            return update_role_response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def delete_role(self, role_id):
        """
        Delete the role
        param: role_id: id of the role to be deleted
        return: returns the response
        """
        log.info("Initializing Api call for deleting role")
        url = f"{self.url}/roles/{str(role_id)}"
        log.info(f"url :{url}")
        response = self.delete(url, ignore_handle_response=True)
        if response.status_code == 200:
            log.info(f"Delete role response's status code: {response.status_code}")
            return response
        else:
            log.error(f"error status code: {response.status_code}")
            return None
