import logging

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession
from hpe_glcp_automation_lib.libs.inventory_nbapi.helpers.helpers import NBAPIHelpers

log = logging.getLogger()


class InventoryNBAPI(AppSession):
    def __init__(self, host, sso_host, client_id, client_secret):
        self.base_url = host
        super(InventoryNBAPI, self).__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/inventory-nbapi/app/"
        self.api_version = "v1/"
        self.nbapi_base_url = f"{self.base_url}{self.base_path}{self.api_version}"

    def get_status(self):
        """
        Check the service status
        :return: a response payload status of true
        """
        end_point = "lifecycle/status"
        url = f"{self.nbapi_base_url}{end_point}"
        log.info("Complete request URL: {}".format(url))
        res = self.get(url=url, ignore_handle_response=True)
        NBAPIHelpers.print_req_response_info(res, log)
        return res
