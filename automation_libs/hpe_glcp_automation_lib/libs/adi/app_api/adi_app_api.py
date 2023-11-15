"""
Activate and device inventory app apis
"""
import logging
import time
import uuid

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class ActivateInventory(AppSession):
    """
    ActivateInventory App API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret, scope=None):
        """
        Initialize ActivateInventory class
        :param host: cluster under test app api url
        :param sso_host: sso_host url
        :param client_id: app api client_id
        :param client_secret: app api client secret
        """
        log.info("Initializing adi_app_api for user api calls")
        super().__init__(host, sso_host, client_id, client_secret, scope=scope)
        self.base_path = "/activate-inventory/app"
        self.api_version = "/v1"

    # Helper functions using the base app apis functions can go here

    def claim_device_app_api(
        self,
        device_category,
        serial,
        platform_id,
        username,
        mac=None,
        part_num=None,
        entitlement_id=None,
        application_customer_id=None,
        location_id=None,
    ):
        """
        API: POST /activate-inventory/app/v1/devices/claim
        Claim a device of any kind using this app api. Add additional optional parameters to this function if needed.
        :param device_category: device category that is to be claimed. Could be NETWORK, STORAGE, COMPUTE etc.
        :param serial: serial_number of the device to be claimed
        :param platform_customer_id: Platform customer id of the account the device is to be claimed in
        :param username: Account email id to be passed in header
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

        if location_id:
            data[0]["location_id"] = location_id

        resp = self.claim_devices(
            pcid=platform_id,
            username=username,
            device_list=data,
            acid=application_customer_id,
        )
        return resp

    def verify_claim_and_assignment_to_application(
        self,
        pcid,
        device_serial_number,
        device_mac_address="",
        device_part_number="",
        application_customer_id="",
    ):
        """
        Given a plaform_customer_id and serial_number of a device, check if the device can be claimed
        Makes a call to /activate-inventory/app/v1/devices/verify_claim
        :param pcid: plaform_customer_id
        :param device_serial_number: serial_number of a device
        :param device_mac_address: mac_address of a device
        :param device_part_number: part_number of a device
        :param application_customer_id: application_customer_id that the device can be assigned
        :return: API response
        """
        # Construct the header
        header = {
            "CCS-Platform-Customer-Id": pcid,
            "CCS-Transaction-Id": uuid.uuid1().hex,
        }

        data = {"serial_number": device_serial_number}
        if device_mac_address:
            data["mac_address"] = device_mac_address
        if device_part_number:
            data["part_number"] = device_part_number
        log.info(data)
        resp = self.claim_verify(payload=data, headers=header)
        # if device is already provisioned, API response code is 400 which results in exception from GLCP session library
        return resp

    def verify_device_claimed_by_pcid(
        self, platform_customer_id, device_serial_number
    ) -> bool:
        """
        Given a plaform_customer_id, check if the serial_number exists in the platform_customer account
        :param pcid: plaform_customer_id
        :param device_serial_number: serial_number of a device
        :param device_mac_address: mac_address of a device
        :param device_part_number: part_number of a device
        :return: True is serial_number is in response, False otherwise
        """
        page_num = 0
        found_device = False
        total_count = 1
        count_per_page = 0

        # Check if serial exists in each page, if not increament page and make another call
        while (total_count > count_per_page) and found_device == False:
            url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}?page={page_num}"
            resp = self.get(url=url)
            # log.info(resp)
            total_count = resp["pagination"]["total_count"]
            count_per_page = resp["pagination"]["count_per_page"]
            page_num += 1
            devices_list = resp["devices"]
            if len(devices_list) == 0:
                log.info("device is not found")
                return False
            for device in devices_list:
                if device_serial_number == device["serial_number"]:
                    found_device = True
                    break
        return found_device

    # **************************
    # Base APP API calls go here
    def get_devices_by_pcid(
        self,
        platform_customer_id,
        limit=2000,
        page=0,
        device_type=None,
        archived_only=None,
        secondary=None,
    ):
        """
        Get devices information of a platform customer
        :param platform_customer_id: platform_customer_id of the customer
        :param limit: limit per page
        :param page: page number to get
        :param device_type: string Enum: "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY"
        :param archived_only: string Enum: "HIDE_ARCHIVED" "ARCHIVED_ONLY" "ALL"
        :return response object
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}"
        if secondary:
            url = f"{self.get_secondary_app_api_hostname()}{self.base_path}{self.api_version}/devices/application/{platform_customer_id}"
        qparams = {"limit": str(limit), "page": str(page)}
        if device_type:
            qparams["device_type"] = device_type
        if archived_only:
            qparams["archive_visibility"] = archived_only
        return self.get(url=url, params=qparams, ignore_handle_response=True)

    def get_devices_by_pcid_acid(
        self, platform_customer_id, application_customer_id, limit=2000, page=0
    ):
        """
        Get devices information of a application customer
        :param platform_customer_id: platform_customer_id of the customer
        :param application_customer_id: Application customer id
        :param limit: limit per page
        :param page: page number to get
        :return response object
        """

        url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}"
            f"/application/{application_customer_id}"
        )
        qparams = {"limit": str(limit), "page": str(page)}
        return self.get(url=url, params=qparams, ignore_handle_response=True)

    def get_devices_by_acid(
        self,
        application_customer_id,
        limit=2000,
        page=0,
        device_type=None,
        internal_device_type=None,
        device_category=None,
        device_serial_number=None,
        part_number=None,
        mac_address=None,
        device_types=None,
        include_config=None,
        platform_customer_id=None,
        username=None,
        secondary=None,
    ):
        """
        Get devices information of an application customer
        :param application_customer_id: Application customer id
        :param limit: limit per page
        :param page: page number to get
        :param device_type: Enum: "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY"
        :param device_category: Enum: "ALL" "ASSIGNED" "AVAILABLE"
        :param device_serial_number: serial number of device
        :param part_number: part number of device
        :param mac_address: Mac adress of the device
        :return response object
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}"
        if secondary:
            url = f"{self.get_secondary_app_api_hostname()}{self.base_path}{self.api_version}/devices/application/{application_customer_id}"
        qparams = {"limit": str(limit), "page": str(page)}
        if device_type:
            qparams["device_type"] = device_type
        if internal_device_type:
            qparams["internal_device_type"] = internal_device_type
        if device_category:
            qparams["device_category"] = device_category
        if device_serial_number:
            qparams["device_serial_number"] = device_serial_number
        if part_number:
            qparams["part_number"] = part_number
        if mac_address:
            qparams["mac_address"] = mac_address
        if device_types:
            qparams["device_types"] = device_types
        if include_config:
            qparams["include_config"] = include_config

        headers = {}
        headers["CCS-Transaction-Id"] = "get_devices_by_acid" + uuid.uuid1().hex

        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            headers["CCS-Username"] = username

        log.info(f"Headers: {headers} params:{qparams} url:{url}")
        if headers:
            return self.get(
                url=url, headers=headers, params=qparams, ignore_handle_response=True
            )
        else:
            return self.get(url=url, params=qparams, ignore_handle_response=True)

    def get_devices_list_by_acid(
        self, application_customer_id, limit=2000, page=0, payload=None
    ):
        """
        Get devices information of an application customer
        :param application_customer_id: Application customer id
        :param limit: limit per page
        :param page: page number to get
        :param payload: {"external_device_type": "AP", "internal_device_type": "ALS","device_category": "ALL",
                          "device_filter_attributes": [{ "serial_number": "string"}]
                        }
        :return response object
        """
        url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/application/"
            + application_customer_id
        )
        data = {}
        if payload:
            data = payload
        qparams = {"limit": str(limit), "page": str(page)}
        return self.post(url=url, params=qparams, json=data, ignore_handle_response=True)

    def get_info_application_instance(self, application_instance_id):
        """
        Get information of an application instance
        :param application_instance_id: Application instance id
        :return response object
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/application-instances/{application_instance_id}"
        log.info(url)
        resp = self.get(url=url, ignore_handle_response=True)
        log.info(resp)
        return resp

    def get_prov_status_by_app_cust_id(self, application_customer_id):
        """
        Get device application provision status
        :param application_customer_id: Application customer id
        :return response object
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}/provision"
        return self.get(url=url, ignore_handle_response=True)

    def claim_devices(self, pcid, username, device_list, transaction_id=None, acid=None):
        """
        Method to claim a serial in a platform customer account
        :param pcid: platform customer id
        :param username: username
        :param device_list: device list for the payload. -- [{"app_category": "NETWORK", "serial_number": "string",
                                                "mac_address": "string","part_number": "string","entitlement_id": "string",
                                                "cloud_activation_key": "string", "location_id": "string","contact_id": "string",
                                                 "device_type": "ALS","tag_change_request": {} }]
        :param  transaction_id: transaction id to be sent in the header
        :param acid: application customer id
        :return response object
        """
        headers = {}
        if pcid:
            headers["CCS-Platform-Customer-Id"] = pcid
        if transaction_id:
            headers["CCS-Transaction-Id"] = transaction_id
        else:
            headers["CCS-Transaction-Id"] = "claim_devices" + uuid.uuid1().hex
        if username:
            headers["CCS-Username"] = username

        if acid == None:
            payload = {"devices": device_list}
        else:
            payload = {"devices": device_list, "application_customer_id": acid}

        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/claim"
        log.info(f"Payload for claim call {payload} Url:{url} headers:{headers}")
        res = self.post(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.info(f"response of claim device: {res}")
        return res

    def get_device_stats_pcid(self, pcid, headers=None):
        """
        Get devices statistics of a platform customer
        :param pcid: plarform customer if
        :param headers: headers for the api call {CCS-Platform-Customer-Id	: string, CCS-Username: string}
        :return response object
        """
        log.info("In function get_device_stats_pcid")
        url_stats = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/"
            + pcid
            + "/stats"
        )
        stats_res = self.get(url=url_stats, headers=headers, ignore_handle_response=True)
        return stats_res

    def get_history(
        self,
        application_customer_id,
        mac=None,
        serial_number=None,
        limit=2000,
        offset=0,
        CCS_Platform_Customer_Id=None,
        CCS_Username=None,
    ):
        """
        Get the device history
        :param application_customer_id: application customer id
        :param mac: Mac address of the device
        :param serial_number: serial number of the device
        :param limit: limit per page
        :param offset: page number to fetch
        :param CCS_Username: Username
        :param CCS_Platform_Customer_Id: Platform customer id
        :return response object
        """
        url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/application/"
            + application_customer_id
            + "/device/history"
        )
        qparam = {"limit": limit, "offset": offset}
        if mac:
            qparam["mac"] = mac
        if serial_number:
            qparam["serial_number"] = serial_number
        headers = {}
        if CCS_Platform_Customer_Id:
            headers["CCS-Platform-Customer-Id"] = CCS_Platform_Customer_Id
        if CCS_Username:
            headers["CCS-Username"] = CCS_Username

        log.info(f"Headers: {headers} params:{qparam} url:{url}")

        if headers:
            return self.get(
                url=url, headers=headers, params=qparam, ignore_handle_response=True
            )
        else:
            return self.get(url=url, params=qparam, ignore_handle_response=True)

    def provision_dev_acid(
        self, acid, payload, platform_customer_id=None, username=None, transaction_id=None
    ):
        """
        assign a device to given application customer id
        :param acid: application customer id
        :param platform_customer_id: platform customer id
        :param username: username
        :param transaction_id: transaction id to be sent in the header
        :return response object
        """
        local_headers = {}
        if transaction_id:
            local_headers["CCS-Transaction-Id"] = transaction_id
        else:
            local_headers = {
                "CCS-Transaction-Id": "provision_dev_acid_" + uuid.uuid1().hex
            }
        if platform_customer_id:
            local_headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            local_headers["CCS-Username"] = username
        if local_headers:
            self.session.headers.update(local_headers)

        log.info(f"****Headers prov app to device: {self.session.headers}")
        url_prov = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/provision"
        log.info(f"Prov device to acid url:{url_prov}  payload:{payload}  acid:{acid}")
        res = self.post(url=url_prov, json=payload, ignore_handle_response=True)
        log.info(f"************************* app provision Res ** :{vars(res)}")
        return res

    def update_dev_acid(
        self,
        acid,
        device_serial_number,
        device_type=None,
        part_number=None,
        pcid=None,
        username=None,
        payload=None,
    ):
        """
        Update device's acid # TODO Changes
        Update existing device information such as Name, IP-Address, Firmware Version etc in CCS.
        Future use case. Not yet implemented.
        """
        headers = {}
        if pcid:
            headers["CCS-Platform-Customer-Id"] = pcid
        if username:
            headers["CCS-Username"] = username

        qparam = {}
        if device_type:
            qparam["device_type"] = device_type
        if part_number:
            qparam["part_number"] = part_number

        url_update = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/device/{device_serial_number}"
        res = self.put(
            url=url_update,
            json=payload,
            headers=headers,
            params=qparam,
            ignore_handle_response=True,
        )
        log.info(f"response of update device: {vars(res)}")
        return res

    def get_device_bulk_info(self, payload):
        """
        Get bulk device(s) details
        :param payload {
                          "serials": [
                            "string"
                          ]
                        }
        """
        device_bulk_info_url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/bulk"
        )
        log.info(f"Get device bulk info with payload {payload}")
        result = self.post(
            url=device_bulk_info_url, json=payload, ignore_handle_response=True
        )
        return result

    def get_device_stats_for_list_of_application_customers(
        self, application_customer_id_list
    ):
        """
        Get devices statistics of one or more application customers . Accepts list of application customer id's
        :param application_customer_id_list: array of application customer id's
        :return response object
        """
        url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/application/stats"
        )
        data = {"application_customer_ids": application_customer_id_list}
        res = self.get(url=url, params=data)
        log.info(res)
        return res

    def get_device_stats_of_a_platform_customer(self, pcid):
        """
        Get device stats for a Platform Customer
        :param pcid: platform customer id
        :return response object
        """
        url_stats = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/{pcid}/stats"
        )
        stats_res = self.get(url=url_stats, ignore_handle_response=True)
        return stats_res

    def claim_verify(self, payload, headers=None):
        """
        Verify device claim
        :param payload:
        {
          "serial_number": "string",
          "mac_address": "string",
          "part_number": "string",
          "application_customer_id": "string"
        }
        :param headers: pass pcid , transaction id in the headers
        :return response object
        """

        log.info(f"Inside Verify claim with payload {payload}")
        claim_verify_url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/verify_claim"
        )
        if not headers:
            verify_res = self.post(
                url=claim_verify_url, json=payload, ignore_handle_response=True
            )
        else:
            self.session.headers.update(headers)
            verify_res = self.post(
                url=claim_verify_url, json=payload, ignore_handle_response=True
            )

        log.info(f"response claim Verify: {verify_res}")
        return verify_res

    def batch_verify_claim(self, payload):
        """
        Batch Verify the device claim
        :param payload: [
                          {
                            "serial_number": "string",
                            "mac_address": "string",
                            "part_number": "string",
                            "application_customer_id": "string"
                          }
                        ]
        :return response object
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/batch_verify_claim"
        batch_verify_res = self.post(url=url, json=payload, ignore_handle_response=True)
        log.info(f"response of batch claim Verify : {batch_verify_res}")
        return batch_verify_res

    def device_reset_afs(
        self,
        serial,
        mac_address=None,
        device_type=None,
        part_number=None,
        pcid=None,
        username=None,
    ):
        """
        Reset the device to aruba factory stock
        :param serial: Serial number of the device
        :param device_type: Device type of the device
        :param part_number: Part number of the device
        :param pcid: platform customer id
        :param username: Username
        :return response object
        """
        payload = {"serial_number": serial}
        if mac_address:
            payload["mac_address"] = mac_address
        if device_type:
            payload["device_type"] = device_type
        if part_number:
            payload["part_number"] = part_number

        headers = {}
        if pcid:
            headers["CCS-Platform-Customer-Id"] = pcid
        if username:
            headers["CCS-Username"] = username

        url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/application/reset"
        )
        if headers:
            res = self.post(
                url=url, headers=headers, json=payload, ignore_handle_response=True
            )
        else:
            res = self.post(url=url, json=payload, ignore_handle_response=True)

        log.info(f"response of device reset to AFS: {res}")
        return res

    def update_archive_status(self, pcid, devices):
        """
        Given a platform customer ID and list pf devices, archive them.
        Make a call to /activate-inventory/app/v1/devices/archive
        :param pcid: plaform_customer_id
        :param devices: list of devices e.g. {"devices": [{"serial_number": serial_number,"archive": boolean}]}
        """
        self.session.headers.update({"CCS-Platform-Customer-Id": pcid})
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/archive"
        log.info(url)
        log.info(devices)
        resp = self.patch(url, json=devices, ignore_handle_response=True)
        return resp

    def move_device_to_folder(
        self, device_list, pcid, folder_name="default", folder_id=None
    ):
        """
        Move device with serial to folder
        :param device_list: device list for the payload
        :param pcid: platform customer id
        :param folder_id: folder id to move the device to
        :param folder_name: folder name to move the device to
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        headers["CCS-Transaction-Id"] = "move_device_to_folder_" + uuid.uuid1().hex
        payload = {"folder_name": folder_name, "devices": device_list}
        if folder_id:
            payload["folder_id"] = folder_id

        move_url = f"{self.base_url}{self.base_path}{self.api_version}/devices/folder"
        res = self.post(
            url=move_url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.info(f"response of Move device to folder: {res}")
        return res

    def move_device_bw_parent_child(self, operation, device_list, pcid):
        """
        Move devices between parent and child customer
        :param operation: string
        :param device_list: device list for the payload
        :param pcid: platform customer id
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        headers["CCS-Transaction-Id"] = "move_device_bw_parent_child_" + uuid.uuid1().hex
        payload = {"devices": device_list}

        move_url = (
            f"{self.base_url}{self.base_path}{self.api_version}/devices/customer/"
            + operation
        )
        res = self.put(
            url=move_url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.info(f"response of Move devices bw parent and child: {res}")
        return res

    def get_taginfo_pcid(self, pcid, limit=2000, page=0):
        """
        Get Tag information of PCID
        :param pcid: platform customer id
        :param limit: limit per page
        :param page: page number to fetch
        :Return response object
        """
        query_param = {"limit": limit, "page": page}

        url = f"{self.base_url}{self.base_path}{self.api_version}/tags/" + pcid
        res = self.get(url=url, params=query_param, ignore_handle_response=True)
        return res

    def create_virtual_device(
        self,
        application_customer_id,
        part_number="MC-VA",
        platform_customer_id=None,
        username=None,
        device_type="GATEWAY",
    ):
        """
        Create a new device.

        :param application_customer_id: The customer ID of the application.
        :param part_number: The part number of the device.
        :param platform_customer_id: The customer ID of the platform. Defaults to None.
        :param username: The username to use. Defaults to None.
        :param device_type: The type of the device. Defaults to None.
        :return: The response from the API call.
        """
        headers = {
            "CCS-Transaction-ID": uuid.uuid1().hex,
            "Content-Type": "application/json",
        }
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            headers["CCS-Username"] = username

        self.session.headers.update(headers)
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}/device"
        payload = {"device_type": device_type, "part_number": part_number}
        response = self.post(url=url, json=payload, ignore_handle_response=True)
        log.info(f"Response from create delete vgw devices {vars(response)}")
        log.info(
            f"This is the whole response after creating the device: {response.json()}"
        )
        log.info(
            f'This is the serial number of newly created the device:  {response.json()["serial_number"]}'
        )
        return response

    def delete_virtual_device(
        self,
        application_customer_id,
        serial,
        pcid=None,
        username=None,
        device_type=None,
        part_number=None,
    ):
        """
        Delete VGW device for ACID
        :param application_customer_id: application customer id
        :param serial: serial of the device
        :param pcid: platform customer id
        :param username: username
        :param device_type: device type
        :param part_number: partnumber of the device
        :Return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        headers["CCS-Username"] = username

        qparam = {}
        if device_type:
            qparam["device_type"] = device_type
        if part_number:
            qparam["part_number"] = part_number

        url_delete_vgw = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}/device/{serial}"

        res = self.delete(
            url=url_delete_vgw,
            headers=headers,
            params=qparam,
            ignore_handle_response=True,
        )
        return res

    def unprovision_device_from_application(
        self,
        payload: dict,
        platform_customer_id: str = None,
        username: str = None,
        transaction_id: str = None,
    ) -> dict:
        """
        Unprovision a device from an application.

        Args:
            device (dict): A dictionary containing the device details.
            platform_customer_id (str, optional): The ID of the platform customer. Defaults to None.
            username (str, optional): The username associated with the request. Defaults to None.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        local_headers = {}
        if transaction_id:
            local_headers["CCS-Transaction-Id"] = transaction_id
        else:
            local_headers = {
                "CCS-Transaction-Id": "unprovision_device_from_application_"
                + uuid.uuid1().hex
            }
        if platform_customer_id:
            local_headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            local_headers["CCS-Username"] = username
        if local_headers:
            self.session.headers.update(local_headers)

        # Build the URL
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/unprovision"

        # Make the POST request and get the response
        response = self.post(url=url, json=payload, ignore_handle_response=True)

        # Log the response and return it
        log.info(f"response from unprovision device from application: {response.text}")
        return response

    def create_application_instance(self, platform_customer_id, username, payload):
        """
        Create application instance.
        """
        headers = {
            "CCS-Transaction-Id": "app_create_application_instance_" + uuid.uuid1().hex
        }
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            headers["CCS-Username"] = username

        url = f"{self.base_url}{self.base_path}{self.api_version}/application-instances"

        response = self.post(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.debug(f"response from create application instance: {response.text}")
        return response

    def application_instance_upgrade(self, platform_customer_id, username, payload):
        """
        Upgrades the application instance details.
        """
        headers = {
            "CCS-Transaction-Id": "app_update_application_instance_" + uuid.uuid1().hex
        }
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            headers["CCS-Username"] = username

        url = f"{self.base_url}{self.base_path}{self.api_version}/application-instances"

        response = self.patch(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.debug(f"response from update application instance: {response.text}")
        return response

    def get_application_instance(
        self, platform_customer_id, username, application_instance_id
    ):
        """
        Get application_instance for application instance id
        :param platform_customer_id: platform customer id
        :param username : CCS username
        :param application_instance_id: application_instance_id
        :return response object
        """

        local_headers = {
            "CCS-Transaction-Id": "app_get_application_instance_" + uuid.uuid1().hex
        }

        if platform_customer_id:
            local_headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            local_headers["CCS-Username"] = username
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/application-instances/{application_instance_id}"
        response = self.get(url=url, ignore_handle_response=True)
        log.debug(f"response from get application instance: {response.text}")
        return response

    def get_rules(self, pcid, search_string=None, folder_ids=None, limit=50, page=0):
        """
        List Rules for a Platform Customer
        :param pcid: platform customer id
        :param search_string: search string for get rules
        :param folder_ids: folder id search
        :param limit: limit per page
        :param page: page
        :return response object
        """
        local_headers = {"CCS-Transaction-Id": "app_get_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        query_param = {"limit": limit, "page": page}
        if search_string:
            query_param["search_string"] = search_string

        if folder_ids:
            query_param["folder_ids"] = folder_ids

        url = f"{self.base_url}{self.base_path}{self.api_version}/rules"
        res = self.get(url=url, params=query_param, ignore_handle_response=True)
        return res

    def create_rule(self, pcid, payload):
        """
        Create Rule for Platform Customer
        :param pcid: platform customer id
        :param payload: Create rule payload - pls refer Inventory doc for example
        :return Response object
        """
        local_headers = {"CCS-Transaction-Id": "app_create_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/rules"
        res = self.post(url=url, json=payload, ignore_handle_response=True)
        return res

    def update_rule(self, pcid, rule_id, payload):
        """
        Modify Rule for a Platform Customer
        :param pcid: platform customer id
        :param payload: Update rule payload - pls refer Inventory doc for example
        :param rule_id: rule id
        :return Response object
        """
        local_headers = {"CCS-Transaction-Id": "app_update_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/rules/{rule_id}"
        res = self.put(url=url, json=payload, ignore_handle_response=True)
        return res

    def delete_rule(self, pcid, rule_id):
        """
        Remove rule for a Platform Customer
        :param pcid: platform customer id
        :param rule_id: rule id
        :return Response object
        """
        local_headers = {"CCS-Transaction-Id": "app_delete_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/rules/{rule_id}"
        res = self.delete(url=url, ignore_handle_response=True)
        return res

    def get_folders(
        self,
        pcid,
        folder_name=None,
        search_name=None,
        folder_id=None,
        sort_by=None,
        sort_order=None,
        limit=50,
        page=0,
    ):
        """
        Get folder information for a Platform Customer
        :param pcid: platform customer id
        :param folder_name: folder name
        :param folder_id: folder id
        :param search_name: get folders by search name
        :param sort_by: sort by - Default value : name
        :param sort_order: Available values : desc, asc
        :param limit: limit
        :param page: page
        :param rule_id: rule id
        :return Response object
        """
        local_headers = {"CCS-Transaction-Id": "app_get_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        query_param = {"limit": limit, "page": page}
        if folder_name:
            query_param["folder_name"] = folder_name

        if search_name:
            query_param["search_name"] = search_name

        if folder_id:
            query_param["folder_id"] = folder_id

        if sort_by:
            query_param["sort_by"] = sort_by

        if sort_order:
            query_param["sort_order"] = sort_order

        url = f"{self.base_url}{self.base_path}{self.api_version}/folders"
        res = self.get(url=url, params=query_param, ignore_handle_response=True)
        return res

    def create_folder(self, pcid, payload):
        """
        New Folder for a Platform Customer
        :param pcid: platform customer id
        :param payload: payload for create folder
        :return response object
        """
        local_headers = {"CCS-Transaction-Id": "app_create_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)
        url = f"{self.base_url}{self.base_path}{self.api_version}/folders"
        log.info(f"Url: {url} , payload: {payload}")
        res = self.post(url=url, json=payload, ignore_handle_response=True)
        return res

    def update_folder(self, pcid, folder_id, payload):
        """
        Update Folder for Platform Customer
        :param pcid: platform customer id
        :param folder_id: folder id
        :param payload: payload for create folder
        :return response object
        """
        local_headers = {"CCS-Transaction-Id": "app_update_folder_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/folders/{folder_id}"
        res = self.put(url=url, json=payload, ignore_handle_response=True)
        return res

    def delete_folder(self, pcid, folder_id):
        """
        Remove Folder for a Platform Customer
        :param pcid: platform customer id
        :param folder_id: folder id
        :return response object
        """
        local_headers = {"CCS-Transaction-Id": "app_delete_folder_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/folders/{folder_id}"
        res = self.delete(url=url, ignore_handle_response=True)
        return res

    def get_rule_of_folder(self, pcid, folder_id, rule_name):
        """
        Get specific rule of a folder for a Platform Customer
        :param pcid: platform customer id
        :param folder_id: folder id
        :param rule_name: rule name
        :return response object
        """

        log.info(f"Folder_id: {folder_id}\n rule_name: {rule_name}")
        local_headers = {"CCS-Transaction-Id": "app_get_rules_" + uuid.uuid1().hex}
        if pcid:
            local_headers["CCS-Platform-Customer-Id"] = pcid
        if local_headers:
            self.session.headers.update(local_headers)

        url = f"{self.base_url}{self.base_path}{self.api_version}/folders/{folder_id}/rules/{rule_name}"
        res = self.get(url=url, ignore_handle_response=True)
        return res

    def create_activate_device_token(self, pcid, user_name):
        """
        Creates a token of a platform customer for activate bridge
        :param pcid: platform customer id
        :param user_name: username
        :return: response object
        """
        headers = {
            "CCS-Transaction-ID": uuid.uuid1().hex,
            "Content-Type": "application/json",
            "CCS-Platform-Customer-Id": pcid,
        }
        self.session.headers.update(headers)
        url = f"{self.base_url}/activate-bridge/internal{self.api_version}/token?email={user_name}"
        res = self.post(url=url, ignore_handle_response=True)
        return res

    def create_simulated_device(
        self,
        platform_customer_id=None,
        username=None,
        serial_number=None,
        mac_address=None,
        part_number=None,
        device_type=None,
        extra_attributes=None,
    ):
        """
        Create simulated device by platform customer
            :param platform_customer_id: Platform customer id of the account the device is to be added
            :param username: Account email id to be passed in header
            :param serial_number: serial_number of the device to be added
            :param mac_address: mac_address of the device to be added
            :param part_number: part_number of the device to be added
            :param device_type: string Enum: "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY"
            :param extra_attributes: extra attributes of device to be added while device addition
        :return Created response object(201)
        """
        headers = {}
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if username:
            headers["CCS-Username"] = username

        payload = {}
        if serial_number:
            payload["serial_number"] = serial_number
        if mac_address:
            payload["mac_address"] = mac_address
        if part_number:
            payload["part_number"] = part_number
        if device_type:
            payload["device_type"] = device_type
        if extra_attributes:
            payload["extra_attributes"] = extra_attributes

        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/simulated"
        log.info(
            f"Payload for create simulated device call: '{payload}', Url: '{url}', headers: '{headers}'."
        )
        response = self.post(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.info(f"response of create simulated device: {response}")
        return response

    def rma_devices(self, device_category, rma_devices_list):
        """
        RMA'd device:- remove the device from customer's account and move to Factory-Stock
            :param device_category: NETWORK, STORAGE, COMPUTE
            :param rma_devices_list:
                [
                    {
                        "serial_number": "",
                        "part_number": "",
                        "case_details": {
                            "case_number": "",
                            "open_timestamp": "",
                            "close_timestamp": "",
                            "contact_email": ""
                        }
                    }
                ]
                :param serial_number: serial_number of the device to be added
                :param part_number: part_number of the device to be added
                :param case_number: case_number of the raised issue
                :param open_timestamp:  creation timestamp of the case
                :param close_timestamp: closing timestamp of the case
                :param contact_email: contact_email of the point of contact

        :return Response object(200)
        """

        headers = {"CCS-Transaction-Id": uuid.uuid1().hex}
        headers.update(self.session.headers)
        payload = {"device_category": device_category, "devices": rma_devices_list}

        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/rma"

        log.info(
            f"Payload for rma devices call: '{payload}', Url: '{url}', headers: '{headers}'."
        )
        response = self.post(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        log.info(f"response of rma devices: {response}")
        return response

    def get_devconfig_node(self, pcid, username, acid, serial, part):
        """
        Method to get a device config
        :param pcid: platform customer id
        :param username: username
        :param acid: application customer id
        :param  transaction_id: transaction id to be sent in the header
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        headers["CCS-Username"] = username
        headers["CCS-Transaction-Id"] = "get_" + uuid.uuid1().hex
        url = f"{self.base_url}{self.base_path}{self.api_version}/device-config?serial_number={serial}&part_number={part}"
        log.info(f"Url:{url} headers:{headers}")
        res = self.get(url=url, headers=headers, ignore_handle_response=True)
        log.info(f"response of get device config: {res.text}")
        return res

    def add_devconfig_node(
        self,
        pcid,
        username,
        acid,
        uber_serial,
        uber_part,
        parent_serial,
        parent_part,
        new_child,
        transaction_id=None,
    ):
        """
        Method to add a node to an existing device config
        :param pcid: platform customer id
        :param username: username
        :param acid: application customer id
        :param parent_serial: parent serial
        :param parent_part: parent part
        :new_child device hierarchy to be added
        :param  transaction_id: transaction id to be sent in the header
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        if transaction_id:
            headers["CCS-Transaction-Id"] = transaction_id
        else:
            headers["CCS-Transaction-Id"] = "add_node" + uuid.uuid1().hex
        headers["CCS-Username"] = username
        payload = {
            "op": "ADD",
            "application_customer_id": acid,
            "parent_node": {"serial_number": parent_serial, "part_number": parent_part},
            "value": new_child,
        }
        url = f"{self.base_url}{self.base_path}{self.api_version}/device-config?serial_number={uber_serial}&part_number={uber_part}"
        log.info(f"Payload for add_node {payload} Url:{url} headers:{headers}")
        res = self.patch(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        time.sleep(5)
        log.info(f"response of add device config node: {res}")
        return res

    def remove_devconfig_node(
        self,
        pcid,
        username,
        acid,
        uber_serial,
        uber_part,
        parent_serial,
        parent_part,
        transaction_id=None,
    ):
        """
        Method to remove a node from an existing device config
        :param pcid: platform customer id
        :param username: username
        :param acid: application customer id
        :param parent_serial: parent serial
        :param parent_part: parent part
        :param  transaction_id: transaction id to be sent in the header
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        if transaction_id:
            headers["CCS-Transaction-Id"] = transaction_id
        else:
            headers["CCS-Transaction-Id"] = "add_node" + uuid.uuid1().hex
        headers["CCS-Username"] = username
        payload = {
            "op": "REMOVE",
            "application_customer_id": acid,
            "remove_node": {"serial_number": parent_serial, "part_number": parent_part},
        }
        url = f"{self.base_url}{self.base_path}{self.api_version}/device-config?serial_number={uber_serial}&part_number={uber_part}"
        log.info(f"Payload for add_node {payload} Url:{url} headers:{headers}")
        res = self.patch(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        time.sleep(5)
        log.info(f"response of add device config node: {res}")
        return res

    def replace_devconfig_node(
        self,
        pcid,
        username,
        acid,
        uber_serial,
        uber_part,
        parent_serial,
        parent_part,
        new_child,
        transaction_id=None,
    ):
        """
        Method to replace a node from an existing device config
        :param pcid: platform customer id
        :param username: username
        :param acid: application customer id
        :param parent_serial: parent serial
        :param parent_part: parent part
        :new_child device hierarchy to be added
        :param  transaction_id: transaction id to be sent in the header
        :return response object
        """
        headers = {}
        headers["CCS-Platform-Customer-Id"] = pcid
        if transaction_id:
            headers["CCS-Transaction-Id"] = transaction_id
        else:
            headers["CCS-Transaction-Id"] = "add_node" + uuid.uuid1().hex
        headers["CCS-Username"] = username
        payload = {
            "op": "REPLACE",
            "application_customer_id": acid,
            "replacement_node": {
                "serial_number": parent_serial,
                "part_number": parent_part,
            },
            "value": new_child,
        }
        url = f"{self.base_url}{self.base_path}{self.api_version}/device-config?serial_number={uber_serial}&part_number={uber_part}"
        log.info(f"Payload for add_node {payload} Url:{url} headers:{headers}")
        res = self.patch(
            url=url, headers=headers, json=payload, ignore_handle_response=True
        )
        time.sleep(5)
        log.info(f"response of add device config node: {res}")
        return res
