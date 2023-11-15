import logging

from hpe_glcp_automation_lib.libs.commons.unified_api.unified_api import UnifiedSession

log = logging.getLogger(__name__)


class OpsRampSpecificApiCalls(UnifiedSession):
    """
    OpsRampSpecificApiCalls Api class.
    """

    def __init__(self, app_api_host, sso_host, client_id, client_secret, tenant_id):
        """
        Initialize OpsrampSpecific APi class
        :param app_api_host: CCS Unified API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param tenant_id: tenant_id
        """
        log.info("Initializing OpsrampSpecific api calls")
        super().__init__(app_api_host, sso_host, client_id, client_secret)
        self.scope = "global:manage"
        self.base_path = "api"
        self.api_version = "v2"
        self.tenant_id = tenant_id
        self.url = f"{self.base_url}/{self.base_path}/{self.api_version}/tenants/{self.tenant_id}"

    def get_partner_details(self):
        """
        Getting the partner details of the opsramp
        returns: returns the response
        """
        log.info("Initializing the Api call got getting partner details")
        url = f"{self.url}"
        log.info(f"URL: {url}")
        response = self.get(url, ignore_handle_response=True)
        if response.status_code == 200:
            partner_response = response.json()
            log.info(f"response {partner_response}")
            return partner_response
        else:
            log.error(f"response error code :{response.status_code}")
            return None
