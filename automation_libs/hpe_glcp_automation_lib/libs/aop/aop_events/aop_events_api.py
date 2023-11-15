"""
Activate Order Events App Api
"""
import logging

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class ActivateOrderEvents(AppSession):
    """
    Activate Order Events App Api Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize ActivateOrderEvents class
        :param host: cluster under test app api url
        :param sso_host: sso_host url
        :param client_id: app api client_id
        :param client_secret: app api client secret
        """
        log.info("Initializing aop_events_api for user api calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/activate-order"
        self.api_version = "/v1"

    def gts_lock_unlock(self, dev_list, reason):
        """
        Lock or unlock a device by GTS
        :param dev_list: list of devices contain serial and mac address
        :param reason: "lock" or "unlock"
        :return: JSON obj
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/event/gts"

        payload = {"reason": "GT." + reason, "orders": dev_list}

        log.info(f"url: {url} payload: {payload}")
        res = self.post(url=url, ignore_handle_response=True, json=payload)

        return res
