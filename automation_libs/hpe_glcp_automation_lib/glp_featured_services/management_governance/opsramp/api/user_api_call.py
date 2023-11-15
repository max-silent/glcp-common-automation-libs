import logging

from hpe_glcp_automation_lib.glp_featured_services.management_governance.opsramp.api.payload import (
    OpsrampConstantPayload,
)
from hpe_glcp_automation_lib.libs.commons.unified_api.unified_api import UnifiedSession

log = logging.getLogger(__name__)


class OpsRampUserApiCalls(UnifiedSession):
    """
    OpsRampUserApiCalls page object model class.
    """

    def __init__(self, app_api_host, sso_host, client_id, client_secret, tenant_id):
        """
        Initialize Opsramp User Api class
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

    def create_user(
        self,
        login_name,
        password,
        firstname,
        lastname,
        designation,
        address,
        city,
        state,
        country,
        email,
        mobile_number,
    ):
        """
        Creating a user in opsramp
        param: login_name
        param: password
        param: firstname
        param: lastname
        param: designation
        param: address
        param: city
        param: state
        param: country
        param: email
        param: mobile_number
        return: returns the response.
        """
        log.info("Initializing Api call for creating user")
        user_data = OpsrampConstantPayload.create_user_data(
            login_name,
            password,
            firstname,
            lastname,
            designation,
            address,
            city,
            state,
            country,
            email,
            mobile_number,
        )
        url = f"{self.url}/" + "users"
        log.info(f"url :{url}")
        response = self.post(url, json=user_data, ignore_handle_response=True)
        if not response.status_code == 200:
            create_user_response = response.json()
            log.info(f"response:{create_user_response}")
            return create_user_response
        else:
            log.error(f"response error code :{response.status_code}")

    def get_minimal_details_user(self):
        """
        Fetch the details of the users present in the opsramp
        return: returns the response
        """
        log.info("Initializing Api call for getting minimal details of user")
        url = f"{self.url}/users/minimal"
        log.info(f"url :{url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            minimal_detail_response = response.json()
            log.info(f"response: {minimal_detail_response}")
            return minimal_detail_response
        else:
            log.error(f"response error code: {response.status_code}")
            return None

    def get_user_details(self, user_id):
        """
        Getting the user details
        param: user_id
        return: returns the response
        """
        log.info("Initializing Api call for getting user details")
        url = f"{self.url}/users/" + user_id
        log.info(f"url :{url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            get_user_detail_response = response.json()
            log.info(f"response: {get_user_detail_response}")
            return get_user_detail_response
        else:
            log.error(f"error status code:{response.status_code}")
            return None
