"""
Helper function for Activate Order Processor App Api
"""
import json
import logging
import re
import urllib.parse

from hpe_glcp_automation_lib.libs.abridge.app_api.abridge_app_api import ActivateBridge
from hpe_glcp_automation_lib.libs.abridge.helpers.abridge_payload_constants import (
    BridgePayload,
)
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class ActivateBridgeHelper:
    """
    Helper class for interacting with the ActivateBridge API.
    """

    def __init__(self, host, user, password):
        """
        Initializes an instance of ActivateBridgeHelper.

        :param host: The host of the ActivateBridge API.
        :param user: The username for authentication.
        :param password: The password for authentication.
        """
        self.payload = BridgePayload()
        self.host = host
        self.user = user
        self.password = password
        self.abridge = ActivateBridge(self.host, self.user, self.password)

    def post_bridge_login(self, username, password_token):
        """
        Login to Bridge using Username/Password or Username/Token

        :param username: The username for the login.
        :param password_token: The password or token for the login.
        :return: A tuple containing a boolean indicating the success of the bridge login, the status code, and the response.
        :raises: Exception: If an error occurs while logging in to the bridge.

        Usage:
        {
            "credential_0": "username",
            "credential_1": "password/token"
        }
        """
        try:
            get_readiness_check = self.abridge.get_readiness_check()
            if get_readiness_check.json()["running"]:
                log.info("Readiness check pass")
                try:
                    login_payload = self.payload.bridge_login()
                    login_payload["credential_0"] = username
                    login_payload["credential_1"] = password_token
                    if any(value == "" for value in login_payload.values()):
                        log.info(
                            "Invalid or missing credentials. Please provide correct credentials %s",
                            login_payload,
                        )
                        return False, None
                    bridge_login_response = self.abridge.post_bridge_login(
                        payload=login_payload
                    )
                    if bridge_login_response.status_code == 200:
                        log.info(
                            "Bridge login successful with status code: %s",
                            bridge_login_response.status_code,
                        )
                        return (
                            bridge_login_response.status_code,
                            bridge_login_response.json(),
                        )
                    else:
                        log.error("Bridge login failed")
                        return (
                            bridge_login_response.status_code,
                            bridge_login_response.json(),
                        )
                except Exception as e:
                    log.error("Bridge login failed {}".format(e))
                    return False, None
            else:
                log.error("Readiness check failed")
                return False, None
        except Exception as e:
            log.error("Readiness check failed {}".format(e))
            return False, None

    def post_bridge_logout(self):
        """
        Logs out from the bridge.

        :return: A tuple containing a boolean indicating the success of the bridge logout and the status code.
        :raises: Exception: If an error occurs while logging out from the bridge.
        """
        try:
            self.abridge = ActivateBridge(self.host, self.user, self.password)
            bridge_logout_response = self.abridge.post_bridge_logout()
            if bridge_logout_response.status_code == 200:
                log.info(
                    "Bridge logout is successful with status code: %s",
                    bridge_logout_response.status_code,
                )
                return True, bridge_logout_response.status_code
            else:
                log.error("Bridge logout failed")
                return False, None
        except Exception as e:
            log.error("Bridge logout Failed {}".format(e))
            return False, None

    def inventory_query(self, **action_param):
        """
        Performs an inventory query.

        :param action_param: The action parameter **kwargs
        :type action_param: dict
        :return: A tuple containing the status code and the response for the inventory.
        :raises: Exception: If an error occurs with inventory response

        Usage: endpoint /api/ext/inventory.json?action=query&limit=800&offset=0
        1. If all parameters are none, it will pass default action=query
        2. User can provide parameters: action=query, limit=800, offset=0
           a) It is mandatory to provide the action parameter, else return False
           b) Given method receives the value and converts it to url-encoded format: action=query&limit=800&offset=0
        """
        if all(value is None for value in action_param.values()):
            log.info("All params are empty")
            action_param = "query"
        else:
            log.info("Fetching Query Params")
            for key, value in action_param.items():
                log.info(f"{key}: {value}")
                if key == "action_param" and value is None:
                    log.info("Action parameter cannot be empty or none")
                    return False
            # action=query&limit=800&offset=0
            action_param = urllib.parse.urlencode(action_param)
            action_param = action_param.replace("action_param=", "")

        try:
            log.info("Action Parameter: %s", action_param)
            payload = self.payload.inventory_query_data()
            payload_json = "json=" + json.dumps(payload)
            self.abridge = ActivateBridge(self.host, self.user, self.password)
            inventory_response = self.abridge.post_inventory_query(
                payload=payload_json, action_param=action_param
            )
            if inventory_response.status_code == 200:
                log.debug("Get inventory response %s", inventory_response.json())
                return inventory_response.status_code, inventory_response.json()
            else:
                log.error("Failed to fetch inventory query.")
                return inventory_response.status_code, inventory_response.json()
        except Exception as e:
            log.error("Failed to fetch inventory query {}".format(e))
            return False, None

    def create_folder(self, action_param="create", user_folder_name=None):
        """
        Creates a folder.

        :param action_param: The action parameter (default: 'create').
        :param user_folder_name: Allow user to provide a folder name (default: None).
        :return: A tuple containing the status code and the response for the folder creation.
        :raises: Exception: If an error occurs while creating the folder
        """
        try:
            payload = self.payload.create_folder()
            # Get the folder name from the payload
            folder_name = payload["folder"]["folderName"]
            # folder_name:'FT_create_folder_7W25LJ2_test' extract 7W25LJ2, that will later replace with random string
            get_folder_name = re.findall(
                r"FT_create_folder_([A-Z0-9]+)_test", folder_name
            )[0]
            new_folder_name = user_folder_name

            if not user_folder_name:
                log.info("Folder name is not provided, creating random folder")
                # Generates a new folder name using random characters
                new_folder_name = RandomGenUtils.random_string_of_chars(
                    length=7, lowercase=False, uppercase=True, digits=True
                )

            # Replaces the extracted folder name with the new folder name in the original folder name
            folder_name = folder_name.replace(get_folder_name, new_folder_name)
            payload["folder"]["folderName"] = folder_name
            payload_json = "json=" + json.dumps(payload)
            self.abridge = ActivateBridge(self.host, self.user, self.password)
            create_folder_response = self.abridge.post_create_folder(
                payload=payload_json, action_param=action_param
            )
            if create_folder_response.status_code == 200:
                log.debug(
                    "Get folder creation response: %s", create_folder_response.json()
                )
                return create_folder_response.status_code, create_folder_response.json()
            else:
                log.error("Failed to create the folder.")
                return create_folder_response.status_code, create_folder_response.json()
        except Exception as e:
            log.error("Failed to create default folder {}".format(e))
            return False, None

    def get_all_folders_by_query(self, action_param="queryFid"):
        """
        Retrieves folders by query

        :param action_param: The action parameter (default: 'queryFid').
        :return: A tuple containing the status code and the response for retrieving folders.
        :raises: Exception: If an error occurs while retrieving the folders
        """
        try:
            payload = self.payload.get_folder_by_query()
            payload_json = "json=" + json.dumps(payload)
            self.abridge = ActivateBridge(self.host, self.user, self.password)
            get_all_folders_query_response = self.abridge.post_get_all_folders_by_query(
                payload=payload_json, action_param=action_param
            )
            if get_all_folders_query_response.status_code == 200:
                log.debug(
                    "Get all folder query response %s",
                    get_all_folders_query_response.json(),
                )
                return (
                    get_all_folders_query_response.status_code,
                    get_all_folders_query_response.json(),
                )
            else:
                log.error("Failed to retrieve all folders by query.")
                return (
                    get_all_folders_query_response.status_code,
                    get_all_folders_query_response.json(),
                )
        except Exception as e:
            log.error("Failed to get query response {}".format(e))
            return False, None

    def get_all_rules_by_folder(self, action_param="query"):
        """
        Retrieves all rules by folder.

        :param action_param: The action parameter (default: 'query').
        :return: A tuple containing the status code and the response for retrieving rules.
        :raises: Exception: If an error occurs while retrieving the rules
        """
        try:
            payload = self.payload.get_all_rule_by_folder()
            payload_json = "json=" + json.dumps(payload)
            self.abridge = ActivateBridge(self.host, self.user, self.password)
            get_all_rule = self.abridge.post_get_all_rules_by_folder(
                payload=payload_json, action_param=action_param
            )
            if get_all_rule.status_code == 200:
                log.debug("Get all rule response %s", get_all_rule.json())
                return get_all_rule.status_code, get_all_rule.json()
            else:
                log.error("Failed to get all the rules folders")
                return get_all_rule.status_code, get_all_rule.json()
        except Exception as e:
            log.error("Failed to get all rules folder {}".format(e))
            return False, None

    def delete_created_folder(self, folderId):
        """
        Deletes a folder identified by the given folderId.

        :param folderId: The ID(s) of the folder to be deleted
        :return: A tuple containing the status code and delete folder response.
        :raises: Exception: If there is an error in deleting the folder
        """
        try:
            payload = self.payload.delete_created_folder()
            payload["folders"] = folderId
            payload_json = "json=" + json.dumps(payload)
            self.abridge = ActivateBridge(self.host, self.user, self.password)
            delete_folder = self.abridge.post_get_all_folders_by_query(
                payload=payload_json, action_param="delete"
            )
            if delete_folder.status_code == 200:
                log.debug("Get delete folder response: %s", delete_folder.json())
                return delete_folder.status_code, delete_folder.json()
            else:
                log.error("Failed to delete folder")
                return delete_folder.status_code, delete_folder.json()
        except Exception as e:
            log.error("Failed to delete folder {}".format(e))
            return False, None

    def device_action_query(self, action_param, devices=None, mac=None, serial_no=None):
        """
        Performs a device action query.

        :param action_param:  The type of action parameter, either 'query' or 'history'.
        :param devices: The device payload (optional, default: None).
        :param mac: List of MAC addresses (optional, default: None).
        :param serial_no: List of serial numbers (optional, default: None).
        :return: A tuple containing the status code and JSON response.
        :raises: Exception: If there is an error in getting the device action response.

        Devices Usage:
        {"devices": [{"mac": "02:1A:1E:78:1C:49", "serial": "VG2206209785"}]}
        """
        try:
            log.debug("Action parameter of type %s", action_param)
            self.abridge = ActivateBridge(self.host, self.user, self.password)

            if action_param == "query":
                log.debug("Device payload received %s", devices)
                device_action_response = self.abridge.post_device_action_query(
                    payload=devices, action_param=action_param
                )
            elif action_param == "history":
                log.debug(
                    f"Device action {action_param} with MAC addresses: {mac} and serial numbers: {serial_no}"
                )
                identifier = ""
                if mac is not None:
                    identifier = "&mac=" + "&mac=".join(mac)
                if serial_no is not None:
                    identifier = "&serial=" + "&serial=".join(serial_no)
                log.debug(
                    f"Performing {action_param} action using identifier: {identifier}"
                )
                device_action_response = self.abridge.post_device_action_query(
                    action_param=action_param + identifier
                )
            else:
                log.error("Invalid action parameter")

            if device_action_response.status_code == 200:
                log.debug("Get device action response %s", device_action_response.json())
                return device_action_response.status_code, device_action_response.json()
            else:
                log.error("Failed to get device action response")
                return device_action_response.status_code, device_action_response.json()
        except Exception as e:
            log.error("Failed to get device action response: %s", e)
            return False, None
