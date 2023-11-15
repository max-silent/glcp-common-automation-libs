import logging

from hpe_glcp_automation_lib.libs.firmware_registry.app_api.fr_app_api import AppAPIClient

log = logging.getLogger(__name__)


class AppAPIHelper(AppAPIClient):
    """
    Firmware Registry APP API Helper Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        log.info("Initializing Firmware Registry Helper for APP Api calls")
        super().__init__(host, sso_host, client_id, client_secret)

    def invoke_search_firmwares(self, cbuild, limit=1000, offset=0):
        """
        Method to invoke cbuild search for the firmware
        :param cbuild: Cbuild value for the query
        :param kwargs: Kwargs of the search query parameters
        :return: Response JSON
        """
        params = {"limit": limit, "offset": offset}
        log.info("Fetching firmwares for the query params : {} ".format(params))
        return self.search_firmwares(cbuild, **params)
