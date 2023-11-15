"""
Activate and device inventory internal apis
"""

import inspect
import logging
import pprint
import urllib.parse
import uuid
from datetime import datetime, timedelta
from functools import wraps

import jwt

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session
from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import Settings

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ActivateInventoryInternal(Session):
    """
    ActivateInventory Internal API Class
    """

    def __init__(
        self,
        max_retries=3,
        retry_timeout=5,
        debug=True,
        **kwargs,
    ):
        log.info("Initializing Activate Inventory for internal api calls")
        super(ActivateInventoryInternal, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        current_env = Settings().current_env()

        # disconnected to be used for onprem environments not shared in the common settings!
        # most commonly used while running in local mode testing
        if "disconnected" in current_env or "on-prem" in current_env:
            self.host = Settings().get_user_api_hostname()
            self.base_url = f"https://{self.host}"
            self.is_onprem = True
        else:
            self.host = "activate-inventory-svc.ccs-system.svc.cluster.local"
            self.base_url = f"http://{self.host}"
            self.is_onprem = False
        self.base_path = "/activate-inventory/internal"
        self.internal_event_path = "/activate-inventory/internal-events"
        self.app_api_path = "/activate-inventory/app"

        self.api_version_v1 = "/v1"
        self.api_version_v2 = "/v2"

    def _get_path_v1(self, path):
        return f"{self.base_path}{self.api_version_v1}/{path}"

    def _get_path_v2(self, path):
        return f"{self.base_path}{self.api_version_v2}/{path}"

    def _log_response(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            log.debug(f"{' '.join(func.__name__.title().split('_'))} API Request")
            res = func(*args, **kwargs)
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response"
                + "\n\n"
                + pprint.pformat(res)
                + "\n"
            )
            return res

        return decorated_func

    def _get_bearer_token(
        self,
        application_id="adiApplicationId",
        application_instance_id="adiApplicationInstanceId",
        scope="read_all write_all",
    ):
        claims = {
            "iss": "https://qa-sso.common.cloud.hpe.com",
            "aud": "app-to-ccs",
            "sub": "ccs",
            "scope": scope,
            "client_id": application_instance_id + "_api",
            "application_id": application_id,
            "application_instance_id": application_instance_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=15),
        }

        return jwt.encode(claims, "secret", algorithm="HS256")

    @_log_response
    def health_check_status(self):
        """
        Get status of the Activate Inventory service health check status
        :return: API Response obj
        """
        if self.is_onprem:
            return self.get(
                url=self._get_path_v1("healthcheck"),
                ignore_handle_response=True,
                verify=False,
            )
        return self.get(url=self._get_path_v1("healthcheck"), ignore_handle_response=True)

    @_log_response
    def get_devices_by_pcid(
        self,
        platform_id,
        limit=2000,
        page=0,
        device_type=None,
        archive_visibility=None,
        search_string=None,
        display_device_types=None,
        application_ids=None,
        tenant_platform_customer_id=None,
        serial_number=None,
        part_number=None,
        unassigned_only=None,
        location_id=None,
        contact_id=None,
        location_ids=None,
        location_search_strings=None,
        device_with_no_sdi_location=False,
        transaction_id=None,
    ):
        """
        Get the list of all the devices for the given platform_id
        API Example :GET  /activate-inventory/internal/v1/devices
        :param transaction_id:
        :param platform_id: platform_id
        :param limit: limit per page
        :param page: page number to get
        :param device_type: string Enum: "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY"
        :param archive_visibility: string Enum: "HIDE_ARCHIVED" "ARCHIVED_ONLY" "ALL"
        :param search_string :string
        :param display_device_types:string
        :param application_ids:string
        :param tenant_platform_customer_id	:string
        :param serial_number:string
        :param part_number:string
        :param unassigned_only	:boolean
        :param location_id:string
        :param contact_id:string
        :param location_search_strings:
        :param device_with_no_sdi_location:
        :param location_ids:
        :param location_id:
        """
        # Set query params
        qparams = {"limit": limit, "page": page}
        if device_type is not None:
            qparams["device_type"] = device_type
        if archive_visibility is not None:
            qparams["archive_visibility"] = archive_visibility
        if search_string is not None:
            qparams["search_string"] = search_string
        if display_device_types is not None:
            qparams["display_device_types"] = display_device_types
        if application_ids is not None:
            qparams["application_ids"] = application_ids
        if tenant_platform_customer_id is not None:
            qparams["tenant_platform_customer_id"] = tenant_platform_customer_id
        if serial_number is not None:
            qparams["serial_number"] = serial_number
        if part_number is not None:
            qparams["part_number"] = part_number
        if unassigned_only is not None:
            qparams["unassigned_only"] = unassigned_only
        if location_id is not None:
            qparams["location_id"] = location_id
        if contact_id is not None:
            qparams["contact_id"] = contact_id
        if location_ids:
            qparams["location_ids"] = location_ids
        if location_search_strings:
            qparams["location_search_strings"] = location_search_strings
        qparams["device_with_no_sdi_location"] = device_with_no_sdi_location

        # Set headers
        if transaction_id is None:
            transaction_id = f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}"
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_id,
                "CCS-Transaction-Id": transaction_id,
                "Content-Type": "application/json",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices"
        log.info(f"{url}")
        if self.is_onprem:
            response = self.get(
                url=url, params=qparams, ignore_handle_response=True, verify=False
            )
        else:
            response = self.get(url=url, params=qparams, ignore_handle_response=True)
        log.info(f"Response of API request[tx:{transaction_id}]: {response}")
        return response

    @_log_response
    def get_device_history(self, **params):
        """
        Get the list of devices by countries and duration
        param kwargs: Kwargs of the search query parameters. Following are the params
            countries : List of 2 letter country codes for fetching the devices
            start_time : Start time in epoch
            end_time : End time in epoch
            limit : Pagination limit. Max is 1000
            offset : Default value is set to 0
            distinct : Default is set to False
        API Example : /activate-inventory/internal/v1/device-history?start-time=1683194757630& \
                      end-time=1683194757640&countries=US,IN&limit=1000&offset=0&distinct=false
        """
        self.session.headers.update(
            {
                "accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        if self.is_onprem:
            return self.get(
                url=self._get_path_v1("device-history"),
                params=params,
                ignore_handle_response=True,
                verify=False,
            )
        return self.get(
            url=self._get_path_v1("device-history"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_blocked_devices(self, **params):
        """
        Get the list of blocked devices
        param kwargs: Kwargs of the search query parameters. Following are the params
            limit : Pagination limit. Max is 1000
            offset : Default value is set to 0
        API Example: /activate-inventory/internal/v1/firmware-blocked-devices?\
                     limit=1000&offset=0
        """
        self.session.headers.update(
            {
                "accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        if self.is_onprem:
            return self.get(
                url=self._get_path_v1("firmware-blocked-devices"),
                params=params,
                ignore_handle_response=True,
                verify=False,
            )
        return self.get(
            url=self._get_path_v1("firmware-blocked-devices"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def update_device_block_status(self, device_payload, **operation):
        """
        Update the status of blocked devices
        device_payload: List of devices in key value pairs Example: {[{"serial_number":"SN4GZJS5T","part_number":"PNQXKHCQL"},
                                                              {"serial_number":"SN9B72CQV","part_number":"PNLLCW6WI"}]}
        param kwargs: Kwargs of the search query parameters
            operation :'firmware_lock' to block a device and 'firmware_unlock' to unblock from getting firmware upgrades

        API Example: /activate-inventory/internal/v1/firmware-blocked-devices?operation=firmware_lock
        """

        self.session.headers.update(
            {
                "accept": "application/json",
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        if self.is_onprem:
            return self.patch(
                url=self._get_path_v1("firmware-blocked-devices"),
                params=operation,
                json=device_payload,
                ignore_handle_response=True,
            )
        return self.patch(
            url=self._get_path_v1("firmware-blocked-devices"),
            params=operation,
            json=device_payload,
            ignore_handle_response=True,
        )

    @_log_response
    def get_device_inventory(self, pcid, **params):
        """
        Export list of devices by platform customer (PCID) with filtering support
        to filter devices by device type and other standard filtering options.
        pcid : Platform Customer ID
        param kwargs: Kwargs of the search query parameters. Following are the params
            serialNumber : Device Serial Number
            limit : Pagination limit. Max is 2000
            offset : Pagination offset
            type : Device type 'STORAGE' or 'COMPUTE'
            select : Can be set to 'application', 'childDevices', 'folder', 'tags' or 'subscription'
            sort : Sort the results by asc or desc. Default asc
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": pcid,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        if self.is_onprem:
            return self.get(
                url=self._get_path_v2("devices"),
                params=params,
                ignore_handle_response=True,
                verify=False,
            )
        return self.get(
            url=self._get_path_v2("devices"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def upload_device_inventory(self, pcid, username, data):
        """
        Export list of devices by platform customer (PCID) with filtering support
        to filter devices by device type and other standard filtering options.
        pcid : Platform Customer ID
        username : Customer username
        data: Payload data which has device inventory info
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": pcid,
                "CCS-Username": username,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        if self.is_onprem:
            return self.post(
                url=self._get_path_v2("devices"),
                json=data,
                ignore_handle_response=True,
                verify=False,
            )
        return self.post(
            url=self._get_path_v2("devices"), json=data, ignore_handle_response=True
        )

    @_log_response
    def get_async_ops_status(self, task_id):
        """
        Get the async operation status
        task_id : Task ID of the task (upload_device_inventory)
        """
        self.session.headers.update(
            {
                "accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        if self.is_onprem:
            return self.get(
                url=self._get_path_v2(f"async-operations/{task_id}"),
                ignore_handle_response=True,
                verify=False,
            )
        return self.get(
            url=self._get_path_v2(f"async-operations/{task_id}"),
            ignore_handle_response=True,
        )

    # deprecated API
    def claim_devices_with_serial_and_entitlement_id(self, platform_id, serial):
        """
        method to claim a serial in a platform customer account using internal api
        platform customer id is in the header of the request
        """

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_id,
                "CCS-Transaction-Id": uuid.uuid1().hex,
            }
        )
        data = {"devices": [{"serial": serial, "entitlement_id": serial}]}
        url = f"{self.base_url}/activate-inventory/internal/v1/devices/claim-serialentitlement"
        log.info(url)
        if self.is_onprem:
            resp = self.get(url=url, json=data, verify=False)
        else:
            resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    def create_software_devices(self, pcid, device_type, part_number, serial_number, mac):
        """
        method to claim a serial in a platform customer account using internal api
        platform customer id is in the header of the request
        """
        url = f"{self.base_url}/activate-inventory/internal/v1/activate/softwareDevice"

        headers = {
            "CCS-Transaction-ID": uuid.uuid1().hex,
            "CCS-Platform-Customer-Id": pcid,
            "Content-Type": "application/json",
        }

        self.session.headers.update(headers)

        data = {
            "action": "register",
            "device": {
                "device_type": device_type,
                "serial_number": serial_number,
                "mac_address": mac,
                "part_number": part_number,
                "device_model": device_type,
            },
            "input_device_config_json": "string",
            "device_description": "create_description",
        }

        log.info(data)
        if self.is_onprem:
            return self.post(
                url=url, json=data, ignore_handle_response=True, verify=False
            )
        return self.post(url=url, json=data, ignore_handle_response=True)

    def get_device_tags_for_pcid(
        self,
        pcid: str,
        exact_name: str = None,
        exact_value: str = None,
        partial_name: str = None,
        partial_value: str = None,
        sort_by: str = None,
        limit=50,
        page=0,
    ) -> dict:
        """
        Get Device Tags for Platform Customer
        Args:
            pcid (str): The PCID of the platform customer.
            exact_name: name of the tag
            exact_value: value of the tag
            partial_name: partial name of the tag
            partial_value: partial_value of the tag
            sort_by: sort by the tags
            limit: limit
            page: page
        Returns:
            dict: The API response.

        """
        query_param = {"limit": limit, "page": page}
        if exact_name:
            query_param["exact_name"] = exact_name
        if exact_value:
            query_param["exact_value"] = exact_value
        if partial_name:
            query_param["partial_name"] = partial_name
        if partial_value:
            query_param["partial_value"] = partial_value
        if sort_by:
            query_param["sort_by"] = sort_by

        # Set the API endpoint URL.
        url = f"{self.base_url}/activate-inventory/internal/v1/devices/tags"

        # Set the headers for the request.
        self.session.headers["CCS-Platform-Customer-Id"] = pcid
        self.session.headers["CCS-Transaction-ID"] = uuid.uuid1().hex
        # Send the request and store the response.

        if self.is_onprem:
            response = self.get(url=url, ignore_handle_response=True, verify=False)
        else:
            response = self.get(url=url, ignore_handle_response=True)
        # Return the response.
        return response

    def edit_device_tags_by_pcid(
        self,
        pcid: str,
        devices: list,
        create_tags: list = None,
        delete_tags: list = None,
        only_validate: bool = None,
    ) -> dict:
        """
        Edit tags for devices belonging to the specified PCID.

        Args:
            pcid (str): The PCID of the platform customer whose devices' tags are being edited.
            devices (list): A list of devices to modify.
            create_tags (list, optional): A list of tags to create. Defaults to None.
            delete_tags (list, optional): A list of tags to delete. Defaults to None.
            only_validate (bool, optional): Only validate the request without actually modifying any tags. Defaults to None.

        Returns:
            dict: The API response.

        """

        # Set the API endpoint URL.
        url = f"{self.base_url}/activate-inventory/internal/v1/devices/tags"

        # Set the headers for the request.
        self.session.headers["CCS-Platform-Customer-Id"] = pcid
        self.session.headers["CCS-Transaction-ID"] = uuid.uuid1().hex
        self.session.headers["only_validate"] = only_validate

        # Build the payload for the request.
        payload = {}
        if devices:
            payload["devices"] = devices
        if create_tags:
            payload["create_tags"] = create_tags
        if delete_tags:
            payload["delete_tags"] = delete_tags

        # Log the payload.
        log.info(payload)

        # Send the request and store the response.
        if self.is_onprem:
            response = self.put(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.put(url=url, json=payload, ignore_handle_response=True)

        # Return the response.
        return response

    def assign_devices_to_application_instance(
        self,
        platform_customer_id,
        username,
        application_id: str,
        application_instance_id: str,
        dev_list: list,
    ):
        """
        - Assigns the device to an application instance
        :param :application_id : Application ID for a device
        :param :application_instance_id : Application Instance ID for a device
        :param :dev_list : device payload
        :param :platform_customer_id : PCID for a customer
        :param :username : username for a customer

        - example for dev_list is [
            {
                "serial_number": "string",
                "device_type": "ALS",
                "part_number": "string",
                "entitlement_id": "string",
                "mac_address": "string"
            }
        ]
        """

        headers = {}
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id

        if username:
            headers["CCS-Username"] = username

        headers["CCS-Transaction-Id"] = uuid.uuid1().hex
        payload = {
            "assign_list": [
                {
                    "devices": dev_list,
                    "application_id": application_id,
                    "application_instance_id": application_instance_id,
                }
            ]
        }
        url = (
            f"{self.base_url}/activate-inventory/internal/v1/devices/application-instance"
        )

        log.info(f"url: {url}, payload: {payload}")
        if self.is_onprem:
            response = self.post(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.post(
                url=url, headers=headers, json=payload, ignore_handle_response=True
            )
        return response

    def unprovision_device_from_application(
        self,
        devices: list,
        platform_customer_id: str = None,
        username: str = None,
        all_devices: bool = None,
        msp_conversion: bool = None,
    ) -> dict:
        """
        Unprovision a device from an application.

        Args:
            devices (list): A list of devices.
            platform_customer_id (str, optional): The ID of the platform customer. Defaults to None.
            username (str, optional): The username associated with the request. Defaults to None.
            all_devices (bool, optional)
            msp_conversion (bool, optional)


        Returns:
            dict: A dictionary containing the response from the API.

        """
        # Set headers for the request
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Username": username,
                "CCS-Transaction-Id": uuid.uuid1().hex,
            }
        )
        data = {"devices": devices}

        # Build the URL
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices/application-instance"

        query_params = {}

        if all_devices is not None:
            query_params["all_devices"] = all_devices
        if msp_conversion is not None:
            query_params["msp_conversion"] = msp_conversion

        if query_params:
            url += "?" + "&".join(
                [f"{key}={value}" for key, value in query_params.items()]
            )

        log.info(url)

        # Make the DELETE request and get the response
        if self.is_onprem:
            response = self.delete(
                url=url, json=data, ignore_handle_response=True, verify=False
            )
        else:
            response = self.delete(url=url, json=data, ignore_handle_response=True)

        # Log the response and return it
        log.info(response.text)
        return response

    def get_preclaim_device_info(
        self, platform_customer_id: str, devices: list = None
    ) -> dict:
        """
        Get Pre-Claim Device Info

        Args:
            devices (list): A list of device objects - serial and part number.
            platform_customer_id (str): The ID of the platform customer. Defaults to None.

        Returns:
            dict: A dictionary containing the response from the API.

        """
        # Set headers for the request
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": uuid.uuid1().hex,
            }
        )

        # Build the URL
        encoded_params = urllib.parse.quote(str(devices))
        url = (
            f"{self.base_url}{self.base_path}{self.api_version_v1}/devices/preclaim?devices="
            + encoded_params
        )

        # Make the GET request and get the response
        if self.is_onprem:
            response = self.get(url=url, ignore_handle_response=True, verify=False)
        else:
            response = self.get(url=url, ignore_handle_response=True)

        # Log the response and return it
        log.info(response.text)
        return response

    def edit_device_info(self, pcid, device_data):
        """
        Given a platform customer ID and device information to update device name and device description.
        Make a call to /activate-inventory/internal/v1/activate/{platform_customer_id}/device
        :param pcid: plaform_customer_id
        :param device_data: dict of device data e.g. {
                    "mac": 'mac',
                    "device_name": "device_name",
                    "device_full_name": "device_full_name",
                    "device_description": "device_description"
                    }
        """
        self.session.headers.update(
            {"CCS-Platform-Customer-Id": pcid, "CCS-Transaction-Id": uuid.uuid1().hex}
        )
        url = (
            f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/{pcid}/device"
        )
        if self.is_onprem:
            resp = self.put(
                url, json=device_data, ignore_handle_response=True, verify=False
            )
        else:
            resp = self.put(url, json=device_data, ignore_handle_response=True)
        log.info(f"Updated device info response:: {resp.json()}")
        return resp

    def edit_device_folders(self, pcid, device_data):
        """
        Given list of device information to update folder names for a particular folder id linked to a device
        Make a call to /activate-inventory/internal/v1/activate/devices/folder
        :param pcid: platform customer id
        :param device_data: dict of device data e.g. {"devices":
                                                [
                                                    {
                                                        "mac": created_mac,
                                                        "folder_id": "folder_id",
                                                        "folder_name": "new_folder_name"
                                                    }
                                                ]
                                            }
        return: response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": pcid,
                "CCS-Transaction-Id": "edit_device_folders_" + uuid.uuid1().hex,
            }
        )
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/devices/folder"
        if self.is_onprem:
            resp = self.post(
                url, json=device_data, ignore_handle_response=True, verify=False
            )
        else:
            resp = self.post(url, json=device_data, ignore_handle_response=True)
        log.info(f"Updated device folders response:: {resp.json()}")
        return resp

    def get_rule_in_folder_for_pcid(self, folder_id, rule_name, pcid, username):
        """
        Method to Get notification details by specific rules and folders
        Make a call to /activate-inventory/internal/v1/activate/folders/{folder_id}/rules/{rule_name}
        :param folder_id: folder id
        :param rule_name: rule name
        :param pcid: platform customer id
        :param username: user name
        :return Response object
        """
        self.session.headers["CCS-Platform-Customer-Id"] = pcid
        self.session.headers["CCS-Username"] = username
        self.session.headers["CCS-Transaction-Id"] = (
            "get_rule_in_folder_for_pcid_" + uuid.uuid1().hex
        )
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/folders/{folder_id}/rules/{rule_name}"
        if self.is_onprem:
            resp = self.get(url, ignore_handle_response=True, verify=False)
        else:
            resp = self.get(url, ignore_handle_response=True)
        log.info(f"Get notification rules with specific folder  response:: {resp.json()}")
        return resp

    # This API IS TO BE DEPRICATED SOON
    def unprovision_post_devices_from_application(
        self,
        serial_list: list,
        platform_customer_id=None,
        username=None,
        transaction_id=None,
    ) -> dict:
        """
             Method to Unprovision device(s) from an application.
             example for serial_list is ['string']
             - This API IS TO BE DEPRICATED SOON

         Args:
             :param serial_list: A list of serial number of devices
             :param platform_customer_id: platform customer id
             :param username: user name
             :param transaction_id: transaction id
        Returns:
             dict: A dictionary containing the response from the API.
        """
        local_headers = {}
        if transaction_id:
            local_headers["CCS-Transaction-Id"] = transaction_id
        else:
            local_headers = {
                "CCS-Transaction-Id": "unprovision_post_devices_from_application_"
                + uuid.uuid1().hex
            }
        if platform_customer_id:
            local_headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            local_headers["CCS-Username"] = username
        self.session.headers.update(local_headers)
        data = {"serials": serial_list}
        # Build the URL
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices/app-unassign"

        # Make the POST request and get the response
        if self.is_onprem:
            response = self.post(
                url=url, json=data, ignore_handle_response=True, verify=False
            )
        else:
            response = self.post(url=url, json=data, ignore_handle_response=True)

        # Log the response and return it
        log.debug(f"Response of the unprovision API is: {response.text}")
        return response

    def get_device_info_for_platform_customer(
        self,
        pcid,
        serial_number=None,
        part_number=None,
        device_type=None,
        search_string=None,
        display_device_type=None,
        folder_name=None,
        folder_uuid=None,
        limit=50,
        page=0,
    ):
        """
        Method to get device's info for a Platform Customer
        GET /activate-inventory/internal/v1/activate/devices
        :param pcid: platform customer id
        :param serial_number: serial number of the device
        :param part_number: part number of the device
        :param device_type: Type of device
        :param search_string: search string for get rules
        :param display_device_type: display device type
        :param folder_name: folder name
        :param folder_uuid: folder uuid
        :param limit: limit per page, default is 50
        :param page: page, default is 0
        :return response object
        """
        local_headers = {
            "CCS-Transaction-Id": "get_device_info_" + uuid.uuid1().hex,
            "CCS-Platform-Customer-Id": pcid,
        }
        self.session.headers.update(local_headers)

        query_param = {"limit": limit, "page": page}
        if search_string:
            query_param["search_string"] = search_string
        if serial_number:
            query_param["serial_number"] = serial_number
        if part_number:
            query_param["part_number"] = part_number
        if device_type:
            query_param["device_type"] = device_type
        if display_device_type:
            query_param["display_device_type"] = display_device_type
        if folder_name:
            query_param["folder_name"] = folder_name
        if folder_uuid:
            query_param["folder_uuid"] = folder_uuid

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/devices"
        if self.is_onprem:
            res = self.get(
                url=url, params=query_param, ignore_handle_response=True, verify=False
            )
        else:
            res = self.get(url=url, params=query_param, ignore_handle_response=True)
        return res

    def get_activate_customers(self, type, platform_customer_id):
        """
        Get Activate Customers by passing either platform customer ids or activate customer ids
        Args:
            type (string): could be either of -> "ACTIVATE" or "PLATFORM" or "APPLICATION".
            platform_customer_id (Array of strings): The PCID of the platform customer

        Returns:
            dict: object containing the response from the API.
        """
        self.session.headers.update(
            {
                "CCS-Transaction-Id": uuid.uuid1().hex,
            }
        )
        # Build the URL

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/customers/types/{type}/ids/{platform_customer_id}"

        # Make the POST request and get the response
        if self.is_onprem:
            response = self.get(url=url, ignore_handle_response=True, verify=False)
        else:
            response = self.get(url=url, ignore_handle_response=True)

        return response

    @_log_response
    def unclaim_devices(self, username, data):
        """
        Unclaim and unassign IaaS devices.
        username : Customer username
        data: Payload data which has device inventory info
        - example for data is [
            {
                "platform_customer_id": "string",
                "devices": [
                    {
                        "serial_number": "VE62345623001",
                        "part_number": "P28948-B211",
                        "device_type": "COMPUTE"
                    }
                ]
            }
        ]
        """
        self.session.headers.update(
            {
                "CCS-Username": username,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        log.info("Session : {}".format(self.session.headers))
        url = self._get_path_v1("devices/unclaim")
        response = self.post(url=url, json=data, ignore_handle_response=True)
        return response

    def claim_device_internal_api(
        self,
        device_category,
        serial,
        username,
        platform_customer_id,
        application_customer_id=None,
        mac=None,
        part_num=None,
        entitlement_id=None,
    ):
        """
        API:POST /activate-inventory/internal/v1/devices
        Claim a device of any kind using this internal api. Add additional optional parameters to this function if needed.
        :param device_category: device category that is to be claimed. Could be NETWORK, STORAGE, COMPUTE etc.
        :param serial: serial_number of the device to be claimed
        :param username: Account email id to be passed in header
        :param platform_customer_id: Platform customer id of the account the device is to be claimed in
        :param application_customer_id: Application Customer id of Application where devices to be assigned
        :param mac: mac_address of the device to be claimed
        :param part_num: part_number of the device to be claimed
        :param entitlement_id: Entitlement id of the device to be claimed
        :return:
        """
        data = {}
        if device_category == "NETWORK":
            data = [
                {
                    "serial_number": serial,
                    "mac_address": mac,
                    "app_category": device_category,
                }
            ]

        elif device_category == "STORAGE":
            data = [
                {
                    "serial_number": serial,
                    "entitlement_id": entitlement_id,
                    "app_category": device_category,
                }
            ]

        elif device_category == "COMPUTE":
            data = [
                {
                    "serial_number": serial,
                    "part_number": part_num,
                    "app_category": device_category,
                }
            ]
        elif device_category == "PCE":
            data = [
                {
                    "serial_number": serial,
                    "mac_address": mac,
                    "app_category": device_category,
                }
            ]

        res = self.claim_devices(
            platform_customer_id=platform_customer_id,
            username=username,
            device_list=data,
            acid=application_customer_id,
        )
        return res

    def create_folder(self, platform_customer_id, payload):
        """
        New Folder for a Platform Customer
        API:POST /activate-inventory/internal/v1/activate/folders
        :param pcid: platform customer id
        :param payload: payload for create folder
        Payload=        {
        "folder_name": "string",
        "parent_folder_id": "string",
        "description": "string",
        "created_by": "string"
        }
        :return response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/folders"
        log.info(f"Url: {url} , payload: {payload}")
        if self.is_onprem:
            response = self.post(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.post(url=url, json=payload, ignore_handle_response=True)
        return response

    def delete_folder(self, platform_customer_id, folder_id):
        """
        Remove Folder for a Platform Customer
        API:DELETE /activate-inventory/internal/v1/activate/folders
        :param pcid: platform customer id
        :param folder_id: folder id
        :return response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/folders/{folder_id}"
        if self.is_onprem:
            response = self.delete(url=url, ignore_handle_response=True, verify=False)
        else:
            response = self.delete(url=url, ignore_handle_response=True)
        return response

    def create_rule(self, platform_customer_id, payload):
        """
        Create Rule for Platform Customer
        API: Post /activate-inventory/internal/v1/activate/rules"
        :param pcid: platform customer id
        :param payload: Create rule payload - pls refer Inventory doc for example
            payload = {
        "rule_id": "string","rule_name": "string","folder_id": "string","folder_name": "string","rule_type": "provision",
        "sub_type": "iap","created_by": "string","created_date": "2019-08-24T14:15:22Z","move_to_folder_id": "string",
        "move_to_folder_name": "string","reference_rule_id": "string","reference_rule_name": "string","amp_ip": "string",
        "shared_secret": "string", "organization": "string","controller": "string","persist_controller_ip": true,
        "ap_group": "string","value": "string","enabled": true,"backup_controller": "string","backup_controller_ip": "string",
        "vpn_mac": "string","vpn_ip": "string","backup_vpn_mac": "string","country_code": "string",
        "config_group": "string","config_node_path": "string","redundancy_level": "string",
        "controller2": "string","primary_ctrl_ip2": "string","backup_controller2": "string","vpn_mac2": "string,"vpn_ip2": "string",
        "backup_vpn_mac2": "string"}
        :return Response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/rules"
        if self.is_onprem:
            response = self.post(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.post(url=url, json=payload, ignore_handle_response=True)
        return response

    def get_rules(
        self, platform_customer_id, search_string=None, folder_ids=None, limit=50, page=0
    ):
        """
        List Rules for a Platform Customer
        API:GET /activate-inventory/internal/v1/activate/rules"
        :param platform customer id: platform customer id
        :param search_string: search string for get rules
        :param folder_ids: folder id search
        :param limit: limit per page
        :param page: page
        :return response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        query_param = {}
        if limit:
            query_param["limit"] = limit
        if page:
            query_param["page"] = page
        if search_string is not None:
            query_param["search_string"] = search_string

        if folder_ids is not None:
            query_param["folder_ids"] = folder_ids

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/rules"
        if self.is_onprem:
            response = self.get(
                url=url, params=query_param, ignore_handle_response=True, verify=False
            )
        else:
            response = self.get(url=url, params=query_param, ignore_handle_response=True)
        return response

    def delete_rule(self, platform_customer_id, rule_id):
        """
        Remove rule for a Platform Customer
        API:DELETE /activate-inventory/internal/v1/activate/rules/{rule_id}"
        :param pcid: platform customer id
        :param rule_id: rule id
        :return Response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/rules/{rule_id}"
        if self.is_onprem:
            response = self.delete(url=url, ignore_handle_response=True, verify=False)
        else:
            response = self.delete(url=url, ignore_handle_response=True)
        return response

    def update_device_to_folder(self, platform_customer_id, payload):
        """
        Update  device to  Folder
        API:POST /activate-inventory/internal/v1//activate/updateDevices"
        :param pcid: platform customer id
        :param payload: payload
          payload=          {
            "devices": [
                {
                "mac": "string",
                "device_name": "string",
                "device_full_name": "string",
                "device_description": "string",
                "folder_id": "string",
                "folder_name": "string",
                "mode": "string"
                }
            ]
            }
        :return response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = (
            f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/updateDevices"
        )
        if self.is_onprem:
            response = self.post(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.post(url=url, json=payload, ignore_handle_response=True)
        return response

    def claim_devices(
        self,
        platform_customer_id,
        username,
        device_list,
        transaction_id=None,
        acid=None,
        csv_import=False,
    ):
        """
        === Method to claim a device in a platform customer account ===
        API:POST /activate-inventory/internal/v1/devices
        :param platform_customer_id: platform customer id
        :param username: username
        :param device_list: device list for the payload. -- [{"app_category": "NETWORK", "serial_number": "string",
                                                "mac_address": "string","part_number": "string","entitlement_id": "string",
                                                "cloud_activation_key": "string", "location_id": "string","contact_id": "string",
                                                "device_type": "ALS","tag_change_request": {} }]
        :param  transaction_id: transaction id to be sent in the header
        :param acid: application customer id
        :param csv_import: csv_import flag
        :return JSON object
        """
        headers = {}
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if transaction_id:
            headers["CCS-Transaction-Id"] = transaction_id
        else:
            headers["CCS-Transaction-Id"] = "claim_devices_" + uuid.uuid1().hex

        if username:
            headers["CCS-Username"] = username

        payload = {"devices": device_list}
        if acid:
            payload["application_customer_id"] = acid
        if csv_import:
            payload["csv_import"] = csv_import

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices"
        log.info(f"Payload for claim call {payload} Url:{url} headers:{headers}")
        if self.is_onprem:
            response = self.post(
                url=url,
                headers=headers,
                json=payload,
                ignore_handle_response=True,
                verify=False,
            )
        else:
            response = self.post(
                url=url, headers=headers, json=payload, ignore_handle_response=True
            )
        log.info(
            f"Response of claim device[platform_customer_id:{platform_customer_id}]: {response}"
        )
        return response

    def update_folder(self, platform_customer_id, folder_id, payload):
        """
        Update Folder for Platform Customer
        API type: /activate-inventory/internal/v1//activate/folders/{folder_id}
        :param pcid: platform customer id
        :param folder_id: folder id
        :param payload: payload for create folder
        payload = {
            "folder_name": "string",
            "parent_folder_id": "string",
            "description": "string",
            "created_by": "string"
            }
        :return response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/folders/{folder_id}"
        if self.is_onprem:
            response = self.put(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.put(url=url, json=payload, ignore_handle_response=True)
        return response

    def update_device_attributes(self, platform_customer_id, username, payload):
        """
        Given a platform customer ID and list of devices, and  archive them.
        Device Archive/Unarchive Internal
        API type: /activate-inventory/internal/v1/devices
        :param pcid: plaform_customer_id
        :param username :username
        :param payload:  payload = {
            "devices": [
                {
                "serial_number": "string",
                "device_type": "ALS",
                "mac_address": "string",
                "part_number": "string",
                "location_id": "string",
                "contact_id": "string",
                "location_name": "string",
                "contact_name": "string",
                "archive": true
                }
            ]
            }"""
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Username": username,
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices"
        log.info(f"Url:{url} => {payload}")
        if self.is_onprem:
            response = self.patch(
                url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.patch(url, json=payload, ignore_handle_response=True)
        return response

    def get_folders(
        self,
        platform_customer_id,
        folder_name=None,
        folder_id=None,
        search_name=None,
        sort_by=None,
        sort_order=None,
        limit=50,
        page=0,
    ):
        """
        Get folder information for a Platform Customer
        API Type: /activate-inventory/internal/v1/activate/folders
        :param platform_customer_id : platform customer id
        :param folder_name : folder_name
        :param folder_id: folder id
        :param search_name : search_name
        :param sort_by: sort by - Default value: name
        :param sort_order: Available values: desc, asc
        :param limit: limit
        :param page: page
        :return Response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        query_param = {}
        if limit:
            query_param["limit"] = limit
        if page:
            query_param["page"] = page
        if folder_name is not None:
            query_param["folder_name"] = folder_name
        if folder_id is not None:
            query_param["folder_id"] = folder_id
        if search_name is not None:
            query_param["search_name"] = search_name
        if sort_by is not None:
            query_param["sort_by"] = sort_by
        if sort_order is not None:
            query_param["sort_order"] = sort_order

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/folders"
        if self.is_onprem:
            response = self.get(
                url=url, params=query_param, ignore_handle_response=True, verify=False
            )
        else:
            response = self.get(url=url, params=query_param, ignore_handle_response=True)
        return response

    def update_rule(self, platform_customer_id, rule_id, payload):
        """
        Modify Rule for a Platform Customer
        API type /activate-inventory/internal/v1/activate/rules/{rule_id}
        :param platform_customer_id: platform customer id
        :param rule_id: rule id
        :param payload: Update rule payload
        payload= {
            "rule_id": "string","rule_name": "string","folder_id": "string",
            "folder_name": "string","rule_type": "provision",sub_type": "iap","created_by": "string",
            "created_date": "2019-08-24T14:15:22Z","move_to_folder_id": "string","move_to_folder_name": "string",
            "reference_rule_id": "string","reference_rule_name": "string",
            "amp_ip": "string","shared_secret": "string","organization": "string","controller": "string",
            "persist_controller_ip": true,"ap_group": "string","value": "string",
            "enabled": true,"backup_controller": "string","backup_controller_ip": "string","vpn_mac": "string",
            "vpn_ip": "string","backup_vpn_mac": "string",
            "country_code": "string","config_group": "string","config_node_path": "string","redundancy_level": "string",
            "controller2": "string","primary_ctrl_ip2": "string",
            "backup_controller2": "string","vpn_mac2": "string",
            "vpn_ip2": "string","backup_vpn_mac2": "string"
            }
        :return Response object
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/rules/{rule_id}"
        if self.is_onprem:
            response = self.put(url=url, json=payload, ignore_handle_response=True)
        else:
            response = self.put(url=url, json=payload, ignore_handle_response=True)
        return response

    def move_device_to_folder(
        self, device_list, platform_customer_id, folder_name="default", folder_id=None
    ):
        """
        Move device with serial to folder
        api:Post /activate-inventory/internal/v1/activate/devices/folder
        :param device_list: device list for the payload
        {
            "folder_id": 0,
            "folder_name": "string",
            "devices": [
                {
                "device_type": "ALS",
                "serial_number": "string",
                "mac_address": "string",
                "part_number": "string",
                "device_model": "string",
                "resource_id": "string"
                }
            ]
            }
        :param platform customer id: platform customer id
        :param folder_name: folder name to move the device to
        :param folder_id: folder id to move the device to
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = platform_customer_id
        headers[
            "CCS-Transaction-Id"
        ] = f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}"
        payload = {"folder_name": folder_name, "devices": device_list}
        if folder_id:
            payload["folder_id"] = folder_id

        move_url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/devices/folder"
        if self.is_onprem:
            response = self.post(
                url=move_url,
                headers=headers,
                json=payload,
                ignore_handle_response=True,
                verify=False,
            )
        else:
            response = self.post(
                url=move_url, headers=headers, json=payload, ignore_handle_response=True
            )
        log.debug(f"response of Move device to folder: {response}")
        return response

    def can_delete_customer_internal(self, pcid, headers):
        """
        Check whether the customer can be deleted or not.
        :param:platform_customer_id:Required
        :headers:CCS-Transaction-Id
        returns :Response of API call {"reason":"Workspace with id {platform_customer_id} has 0 devices associated",
        "can_be_deleted":true}
        """
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/customers/{pcid}/canDelete"
        log.debug(url)
        if self.is_onprem:
            res = self.get(url=url, headers=headers, verify=False)
        else:
            res = self.get(url=url, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def create_vgw_device(self, platform_customer_id):
        """
        Create a VGW (Virtual Gateway) device and associate it with a platform customer.
        Param: platform_customer_id (str): The platform customer ID to associate with the VGW device.
        Returns: An Object containing the response from the VGW device creation request.
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": "get_devices_by_pcid_" + uuid.uuid1().hex,
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/vgwRegister"
        if self.is_onprem:
            response = self.post(url=url, ignore_handle_response=True, verify=False)
        else:
            response = self.post(url=url, ignore_handle_response=True)
        return response

    def remove_vgw_device(self, platform_customer_id: str, payload: dict):
        """
        Method to remove VGW device
        param: payload should look like foloowing-> {
        "mac_address": "string",
        "serial_number": "string"
        }
        param: platform_customer_id (str): The platform customer ID
        Returns: An Object containing the response from the VGW device creation request.
        """

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": "get_devices_by_pcid_" + uuid.uuid1().hex,
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/removeVgw"
        if self.is_onprem:
            response = self.post(
                url=url, json=payload, ignore_handle_response=True, verify=False
            )
        else:
            response = self.post(url=url, json=payload, ignore_handle_response=True)
        return response

    def create_application_instance(
        self, transaction_id=None, platform_customer_id=None, username=None, payload=None
    ):
        """
        Create application instance using inventory internal API
        """
        if transaction_id is None:
            transaction_id = "app_create_application_instance_" + uuid.uuid1().hex
        else:
            transaction_id = "app_create_application_instance_" + transaction_id
        headers = {"CCS-Transaction-Id": transaction_id}
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            headers["CCS-Username"] = username
        token = self._get_bearer_token()
        headers["Authorization"] = f"Bearer {token}"

        url = f"{self.base_url}{self.app_api_path}{self.api_version_v1}/application-instances"
        response = self.post(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.info(
            f"response from create application instance using inventory internal API: {response.text}"
        )
        return response

    def get_device_summary(
        self,
        platform_customer_id,
        mac_address_list=None,
        device_names_list=None,
        serial_number_list=None,
        part_number_list=None,
        folder_id_list=None,
        folder_name_list=None,
        limit=2000,
        page=None,
        action=None,
        search_string=None,
        external_device_type=None,
        device_models_list=None,
    ):
        """
        Get the summary information of devices for the given platform_customer_id.
        API Example: POST /activate-inventory/internal/v1/activate/devicesSummary
        :param platform_customer_id:platform_customer_id
        :param mac_address_list = mac_address_list
        :param device_names_list = device_names_list
        :param serial_number_list = serial_number_list
        :param part_number_list = part_number_list
        :param folder_id_list = folder_id_list
        :param folder_name_list = folder_name_list
        :param action = action
        :param limit = 2000
        :param page = None
        :param search_string = search_string
        :param external_device_type = external_device_type
        :param device_models_list = device_models_list
            Sample payload: {
            "macs": ["string"],
            "device_names": ["string"],
            "serial_numbers": [ "string" ],
            "parts": ["string"],
            "folder_ids": ["string" ],
            "folder_names": [ "string"],
            "limit": 1,
            "page": 0,
            "last_sync_time": 0,
            "action": "QUERY", enum :"query" "device-bulk-move" "move-to-rma" "update" "whitelist" "own" "unknown"
            "external_device_type": "AP",Enum: "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY" "PCE" "SD_WAN_GW" "OPSRAMP_SAAS" "SENSOR"
            "device_models": ["string"],
            "search_string": "string"
                }
        note:when providing a values, the user should pass them as a list wherever required.
        """
        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/devicesSummary"
        payload = {}
        if mac_address_list:
            payload["macs"] = mac_address_list
        if device_names_list:
            payload["device_names"] = device_names_list
        if serial_number_list:
            payload["serial_numbers"] = serial_number_list
        if part_number_list:
            payload["parts"] = part_number_list
        if folder_id_list:
            payload["folder_ids"] = folder_id_list
        if folder_name_list:
            payload["folder_names"] = folder_name_list
        if limit:
            payload["limit"] = limit
        if page:
            payload["page"] = page
        if action:
            payload["action"] = action
        if external_device_type:
            payload["external_device_type"] = external_device_type
        if device_models_list:
            payload["device_models"] = device_models_list
        if search_string:
            payload["search_string"] = search_string

        response = self.post(url=url, json=payload, ignore_handle_response=True)
        return response

    def add_alias(
        self,
        alias=None,
        type=None,
        ccs_manager_pcid=None,
        platform_customer_id=None,
        username=None,
        transaction_id=None,
    ):
        """
        Add alias to a customer
        alias: alias to be added
        type: type of alias
        platform_customer_id: Platform Customer ID for which alias to be created
        ccs_manager_pcid : CCS Manager Platform Customer ID
        username: Username
        """
        payload = {}
        if alias:
            payload["alias"] = alias
        if type:
            payload["type"] = type

        if transaction_id is None:
            transaction_id = "add_alias" + uuid.uuid1().hex
        else:
            transaction_id = "add_alias" + transaction_id
        headers = {"CCS-Transaction-Id": transaction_id}
        if ccs_manager_pcid:
            headers["CCS-Platform-Customer-Id"] = ccs_manager_pcid
        if username:
            headers["CCS-Username"] = username
        if platform_customer_id:
            headers["CCS-Impersonated-Platform-Customer-Id"] = platform_customer_id
        log.debug(f"Add Alias Ft Session : {self.session.headers}, data: {payload}")
        response = self.post(
            url=self._get_path_v2("activate/customers/aliases"),
            json=payload,
            headers=headers,
        )
        log.debug(f"Add Alias Ft response: {response}")
        return response

    def update_alias(
        self,
        alias=None,
        type=None,
        old_alias=None,
        ccs_manager_pcid=None,
        platform_customer_id=None,
        username=None,
        transaction_id=None,
    ):
        """
        Update alias to a customer
        alias: new alias
        type: type of new alias
        old_alias: alias to be updated
        platform_customer_id: Platform Customer ID for which alias to be updated
        ccs_manager_pcid : CCS Manager Platform Customer ID
        username: Username
        """
        payload = {}
        if alias:
            payload["alias"] = alias
        if type:
            payload["type"] = type

        if transaction_id is None:
            transaction_id = "update_alias" + uuid.uuid1().hex
        else:
            transaction_id = "update_alias" + transaction_id
        headers = {"CCS-Transaction-Id": transaction_id}
        if ccs_manager_pcid:
            headers["CCS-Platform-Customer-Id"] = ccs_manager_pcid
        if username:
            headers["CCS-Username"] = username
        if platform_customer_id:
            headers["CCS-Impersonated-Platform-Customer-Id"] = platform_customer_id
        log.debug(f"Update Alias Ft Session : {self.session.headers}, data: {payload}")
        response = self.put(
            url=self._get_path_v2(f"activate/customers/aliases/{old_alias}"),
            json=payload,
            headers=headers,
        )
        log.debug(f"Update Alias Ft response: {response}")
        return response

    def delete_alias(
        self,
        alias=None,
        ccs_manager_pcid=None,
        platform_customer_id=None,
        username=None,
        transaction_id=None,
    ):
        """
        Delete alias to a customer
        alias: alias to be deleted
        platform_customer_id: Platform Customer ID for which alias to be deleted
        ccs_manager_pcid : CCS Manager Platform Customer ID
        username: Username
        """
        if transaction_id is None:
            transaction_id = "delete_alias" + uuid.uuid1().hex
        else:
            transaction_id = "delete_alias" + transaction_id
        headers = {"CCS-Transaction-Id": transaction_id}
        if ccs_manager_pcid:
            headers["CCS-Platform-Customer-Id"] = ccs_manager_pcid
        if username:
            headers["CCS-Username"] = username
        if platform_customer_id:
            headers["CCS-Impersonated-Platform-Customer-Id"] = platform_customer_id
        log.debug(f"Delete Alias Ft Session : {self.session.headers}, data: {alias}")
        response = self.delete(
            url=self._get_path_v2(f"activate/customers/aliases/{alias}"), headers=headers
        )
        log.debug(f"Delete Alias Ft response: {response}")
        return response

    def get_customer_for_alias(self, alias=None, transaction_id=None):
        """
        Get customer details by alias
        alias: alias to be searched
        """
        if transaction_id is None:
            transaction_id = "get_customer_for_alias" + uuid.uuid1().hex
        else:
            transaction_id = "get_customer_for_alias" + transaction_id
        headers = {"CCS-Transaction-Id": transaction_id}
        log.debug(
            f"Get Customer for Alias Ft Session : {self.session.headers}, data: {alias}"
        )
        response = self.get(
            url=self._get_path_v1(f"activate/customers/aliases/{alias}"), headers=headers
        )
        log.debug(f"Get Customer for Alias Ft response: {response}")
        return response

    def get_alias_by_pcid(
        self, platform_customer_id=None, alias=None, transaction_id=None
    ):
        """
        Get alias to a customer
        alias: alias to be searched
        pcid: Platform Customer ID for which alias to be searched
        """
        qparams = {}
        if alias:
            qparams["search_string"] = alias
        if transaction_id is None:
            transaction_id = "get_alias_by_pcid" + uuid.uuid1().hex
        else:
            transaction_id = "get_alias_by_pcid" + transaction_id
        headers = {"CCS-Transaction-Id": transaction_id}
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        log.debug(f"Get Alias By PCID Ft Session : {self.session.headers}, data: {alias}")
        response = self.get(
            url=self._get_path_v1(f"activate/customers/aliases"),
            params=qparams,
            headers=headers,
        )
        log.debug(f"Get Alias By PCID response: {response}")
        return response

    def send_internal_event(self, platform_customer_id=None, internal_event=None):
        """
        :param platform_customer_id: Platform customer id
        :param internal_event: Internal event
        :return:
        """

        event_type = internal_event["type"]
        headers = {
            "CCS-Platform-Customer-Id": platform_customer_id,
            "CCS-Transaction-Id": event_type + internal_event["id"],
            "Content-Type": "application/json",
        }

        log.info(
            f"Sending internal_event [platform id:{platform_customer_id}, event:{event_type}] => {internal_event}"
        )
        url = f"{self.base_url}{self.internal_event_path}{self.api_version_v1}/callback"
        log.info(url)
        response = self.post(url=url, headers=headers, json=internal_event)
        log.info(f"Response of internal_event request: {response}")
        return response

    def fetch_locations_by_platform_id_and_search_string(
        self, transaction_id=None, platform_customer_id=None, search_string=None
    ):
        if transaction_id is None:
            transaction_id = (
                "fetch_locations_by_platform_id_and_search_string_" + platform_customer_id
            )

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": transaction_id,
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/locations"
        response = None
        if search_string:
            log.info(f"{url}?search_string={search_string}")
            params = {"search_string": search_string}
            response = self.get(url=url, params=params, ignore_handle_response=True)
        else:
            log.info(f"{url}")
            response = self.get(url=url, ignore_handle_response=True)

        log.info(f"Response of API request[tx:{transaction_id}]: {response}")
        return response

    def get_devices_by_platform_cid(
        self,
        transaction_id=None,
        platform_customer_id=None,
        serial_number=None,
        location_ids=None,
        location_search_strings=None,
        device_with_no_sdi_location=False,
    ):
        """

        :param transaction_id:
        :param platform_customer_id:
        :param serial_number:
        :param location_ids:
        :param location_search_strings:
        :param device_with_no_sdi_location:
        :return:
        """
        if transaction_id is None:
            transaction_id = "get_devices_by_platform_cid_" + platform_customer_id

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": transaction_id,
            }
        )

        params = {}
        if serial_number:
            params["serial_number"] = serial_number
        if location_ids:
            params["location_ids"] = location_ids
        if location_search_strings:
            params["location_search_strings"] = location_search_strings
        params["device_with_no_sdi_location"] = device_with_no_sdi_location

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices"
        log.info(f"{url}")
        response = self.get(url=url, params=params, ignore_handle_response=True)
        log.info(f"Response of API request[tx:{transaction_id}]: {response}")

        return response

    def post_devices_by_platform_cid(
        self,
        transaction_id=None,
        platform_customer_id=None,
        device_app_search_request=None,
    ):
        """

        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param device_app_search_request: Request body
        :return:
        """
        if transaction_id is None:
            transaction_id = "get_devices_by_pcid_using_post_" + platform_customer_id

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "Content-Type": "application/json",
                "CCS-Transaction-Id": transaction_id,
            }
        )

        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/devices/filter"
        log.info(f"{url}")
        response = self.post(
            url=url, json=device_app_search_request, ignore_handle_response=True
        )
        log.info(f"Response of API request[tx:{transaction_id}]: {response}")
        return response

    def get_device_bulk_info(self, device_info_request=None, is_app_api=False):
        """
        Get bulk device(s) details
        :param device_info_request: payload {
                "serials": ["string"]
            }
        :param is_app_api: To call app api
        """
        base_path = self.base_path
        if is_app_api:
            base_path = self.app_api_path
        headers = {"Content-Type": "application/json"}
        token = self._get_bearer_token()
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.base_url}{base_path}{self.api_version_v1}/devices/bulk"
        log.info(f"Get device bulk info with payload: {device_info_request}")
        log.info(f"{url}")
        response = self.post(
            url=url,
            headers=headers,
            json=device_info_request,
            ignore_handle_response=True,
        )
        log.info(f"Response of API request: {response}")
        return response

    def get_info_device_history(
        self,
        platform_customer_id,
        mac=None,
        serial_number=None,
        transaction_id=None,
        limit=2000,
        page=0,
    ):
        """
        Retrieve device history information for a specific platform customer and device.

        Args:
            platform_customer_id (str): The unique identifier for the platform customer.
            mac (str,required): The MAC address of the device.
            serial_number (str, optional): The serial number of the device.
            transaction_id (str, optional): An optional custom transaction ID for tracking the request.
            If set to False, the `CCS-Transaction-Id` header will be set to None.
            If not provided or set to None, a default transaction ID will be generated.
            limit (int, optional): The maximum number of records to return (default is 2000).
            page (int, optional): The page number for paginated results (default is 0).

        Returns:
            dict: The device history information.
        """
        headers = {}

        if transaction_id:
            headers["CCS-Transaction-Id"] = transaction_id
        elif transaction_id is None:
            headers["CCS-Transaction-Id"] = "get_info_device_history" + uuid.uuid1().hex
        else:
            headers["CCS-Transaction-Id"] = None
        headers["CCS-Platform-Customer-Id"] = platform_customer_id
        url = (
            f"{self.base_url}{self.base_path}{self.api_version_v1}/activate/deviceHistory"
        )
        qparams = {"mac": mac}
        if mac is None:
            qparams = {}
        if serial_number is not None:
            qparams["serial_number"] = serial_number
        if limit is not None:
            qparams["limit"] = limit
        if page is not None:
            qparams["page"] = page
        log.info(f"url:{url} headers:{headers}")
        return self.get(
            url=url, params=qparams, headers=headers, ignore_handle_response=True
        )
