import logging

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session
from hpe_glcp_automation_lib.libs.inventory_nbapi.helpers.helpers import NBAPIHelpers

log = logging.getLogger()


class LifecycleStatusNBAPI(Session):
    def __init__(
        self, localhost_port=None, max_retries=3, retry_timeout=5, debug=True, **kwargs
    ):
        log.info(
            f"Initializing NBAPI internal session for api calls: localhost_port: {localhost_port}"
        )
        super().__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "http://inventory-nbapi-svc.ccs-system.svc.cluster.local:80"
        if localhost_port:
            self.host = "http://localhost:" + localhost_port
        self.base_path = "/inventory-nbapi/internal"

    def get_status(self):
        """
        Check the service status
        :return: a response payload status of true
        """
        end_point = "/lifecycle/status"
        url = f"{self.host}{self.base_path}{end_point}"
        log.info("Complete request URL: {}".format(url))
        res = self.get(url=url, ignore_handle_response=True)
        NBAPIHelpers.print_req_response_info(res, log)
        return res
