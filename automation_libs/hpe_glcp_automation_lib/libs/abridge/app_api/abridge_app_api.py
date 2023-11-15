"""
Activate Bridge App Api
"""
import logging

from hpe_glcp_automation_lib.libs.commons.app_api.abridge_session import (
    ActivateBridgeCookies,
)

log = logging.getLogger(__name__)


class ActivateBridge(ActivateBridgeCookies):
    """
    API client for interacting with the Activate Bridge App
    """

    def __init__(self, host, user, password):
        """
        Initializes an instance of ActivateBridge API client.

        :param host: The host of the ActivateBridge API.
        :param user: The username for authentication.
        :param password: The password for authentication.
        """
        log.info("Initializing Activate Bridge for API calls")
        super().__init__(host, user, password)
        self.base_path = "/api/ext"
        self.api_version_v1 = "/v1"

    def post_bridge_login(self, payload):
        """
        Logs in to the Activate Bridge App.

        :param payload: json login payload.
        """
        url = f"{self.base_url}/LOGIN"
        res = self.post(url=url, json=payload, ignore_handle_response=True)
        return res

    def post_bridge_logout(self):
        """
        Logs out from the Activate Bridge App.
        """
        url = f"{self.base_url}/LOGOUT"
        res = self.post(url=url, headers=self.headers, ignore_handle_response=True)
        return res

    def post_inventory_query(self, payload, action_param):
        """
        Performs an inventory query.

        :param payload
        :param action_param: The action parameter
        """
        url = f"{self.base_url}{self.base_path}/inventory.json?action={action_param}"
        res = self.post(
            url=url, data=payload, headers=self.headers, ignore_handle_response=True
        )
        return res

    def post_create_folder(self, payload, action_param):
        """
        Creates a folder.

        :param payload
        :param action_param: The action parameter
        """
        url = f"{self.base_url}{self.base_path}/folder.json?action={action_param}"
        res = self.post(
            url=url, data=payload, headers=self.headers, ignore_handle_response=True
        )
        return res

    def post_get_all_folders_by_query(self, payload, action_param):
        """
        Retrieves folders by query.

        :param payload
        :param action_param: The action parameter.
        """
        url = f"{self.base_url}{self.base_path}/folder.json?action={action_param}"
        res = self.post(
            url=url, data=payload, headers=self.headers, ignore_handle_response=True
        )
        return res

    def post_get_all_rules_by_folder(self, payload, action_param):
        """
        Retrieves all rules by folder.

        :param payload
        :param action_param: The action parameter
        """
        url = f"{self.base_url}{self.base_path}/rule.json?action={action_param}"
        res = self.post(
            url=url, data=payload, headers=self.headers, ignore_handle_response=True
        )
        return res

    def get_readiness_check(self):
        """
        Do the readiness check before login
        """
        url = f"{self.base_url}/activate-bridge/internal{self.api_version_v1}/status"
        res = self.get(url=url, headers=self.headers, ignore_handle_response=True)
        return res

    def post_device_action_query(self, action_param, payload=None):
        """
        Perform device action
        :param payload optional (device history)
        :param action_param: The action parameter
        :return: requests.Response
        """
        url = f"{self.base_url}{self.base_path}/device.json?action={action_param}"
        res = self.post(
            url=url, data=payload, headers=self.headers, ignore_handle_response=True
        )
        return res
