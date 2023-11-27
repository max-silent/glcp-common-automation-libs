import logging
import time
import uuid
from copy import deepcopy

from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.adi.app_api.adi_payload_constants import AdiInputPayload
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class AdiAppApiHelper(ActivateInventory):
    """

    Helper class for ADI App Api Class

    """

    def __init__(self, host, sso_host, client_id, client_secret):
        log.info("Initializing app_api_helper for user api calls")
        super().__init__(host, sso_host, client_id, client_secret)

    def is_device_provisioned_to_pcid(
        self, platform_customer_id, serial_number, mac_address=None, part_number=None
    ):
        """
        Use this function to check if the device is assigned to an application (provisioned) for a given PCID
        platform_customer_id: PCID of customer
        serial_number: device serial number
        return: True if device is provisioned/assigned. False if device is not assigned
        """
        header = {
            "CCS-Platform-Customer-Id": platform_customer_id,
            "CCS-Transaction-Id": "is_device_provisioned_to_pcid" + uuid.uuid1().hex,
        }

        data = {"serial_number": serial_number}
        if mac_address is not None:
            data["mac_address"] = mac_address
        if part_number is not None:
            data["part_number"] = part_number
        resp = self.claim_verify(payload=data, headers=header)
        if resp.status_code == 409:
            return False
        elif resp.status_code == 200 or resp.status_code == 400:
            resp_message = resp.json().get("response")
            log.info(
                "Response message from is_device_provisioned_to_pcid {}".format(
                    resp_message
                )
            )

            if resp_message == "device already provisioned":
                return True
            elif resp_message == "claimable":
                return False
        return False

    def _update_provisioning_info(self, existing_provisioning_info, updated_info):
        """
        Update provision info for API /application-instances
        """
        device_family = updated_info["device_family"]
        existing_info = next(
            (
                info
                for info in existing_provisioning_info
                if info["device_family"] == device_family
            ),
            None,
        )
        if existing_info:
            existing_info["device_endpoint_url"] = updated_info["device_endpoint_url"]
        else:
            existing_provisioning_info.append(updated_info)

    def prepare_provision_info(
        self, application_instance_id, provisioning_data, device_types
    ):
        """
        Prepares the Provision info for API /application-instances
        """
        provision_info = {
            "application_instance_id": application_instance_id,
            "provisioning_info": provisioning_data,
            "device_types": device_types,
        }

        return provision_info

    def application_instance_upgrade_helper(
        self,
        platform_customer_id,
        username,
        provisioning_data,
        application_instance_id,
        device_types,
    ):
        """
        Invokes the library function application_instance_upgrade to upgrade the application instance details.
        """
        provision_info = self.prepare_provision_info(
            application_instance_id, provisioning_data, device_types
        )
        response = self.application_instance_upgrade(
            platform_customer_id, username, provision_info
        )
        return response

    def invoke_create_application_instance(
        self,
        platform_customer_id,
        username,
        application_instance_id,
        application_id,
        provisioning_data,
        device_types=None,
        deployment_private=True,
    ):
        """
        Method to build payload to create application_instance. Sample payload: {
        "application_instance_id": "string",
        "application_id": "string",
        "provisioning_info": [{"device_family": "IAP","device_endpoint_url": "string"}],
        "device_types": ["AP"],
        "deployment_private": true
        }

        payload = {
            "application_instance_id": application_instance_id,
            "application_id": application_id,
            "provisioning_info": AdiInputPayload().get_provisioning_info(),
            "device_types": ["AP", "GATEWAY", "SWITCH", "COMPUTE", "STORAGE", "PCE"],
            "deployment_private": "False"
        }
        """

        payload = {
            "application_instance_id": application_instance_id,
            "application_id": application_id,
            "provisioning_info": provisioning_data,
            "device_types": device_types,
            "deployment_private": deployment_private,
        }

        # build payload here
        return self.create_application_instance(platform_customer_id, username, payload)

    def get_unprovisioned_device_for_pcid(self, platform_customer_id, device_type="AP"):
        """
        Use this function to get a device that is unassigned to any application for a given PCID
        platform_customer_id: PCID of customer
        return: Device that unassigned, False if not such device found
        """
        device_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id, device_type=device_type
        )

        if device_response:
            # loop until we find a device for given device_type that is unassigned
            dict_response = device_response.json()
            for device in dict_response["devices"]:
                log.debug("DEVICE INFO {}".format(device))
                if not self.is_device_provisioned_to_pcid(
                    platform_customer_id=platform_customer_id,
                    serial_number=device["serial_number"],
                    mac_address=device.get("mac_address"),
                    part_number=device.get("part_number"),
                ):
                    return device
        return False

    def get_provisioned_device_for_pcid(self, platform_customer_id, device_type="AP"):
        """
        Use this function to get a device that is assigned to an application (provisioned) for a given PCID
        platform_customer_id: PCID of customer
        device_type: type of device. Can be one of ["ALS" "AP" "BLE" "COMPUTE" "CONTROLLER" "DHCI_COMPUTE" "DHCI_STORAGE" "EINAR" "EINR" "GATEWAY" "IAP" "LTE_MODEM" "MC" "STORAGE" "SWITCH" "NW_THIRD_PARTY" "PCE" "UNKNOWN"]
        return: Device that is provisioned for given PCID and device_type, False if such device not found
        """
        device_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id, device_type=device_type
        )

        if device_response:
            # loop until we find a device for given device_type that is unassigned
            dict_response = device_response.json()
            for device in dict_response["devices"]:
                log.debug("DEVICE INFO {}".format(device))
                if self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    return device
        return False

    def get_unarchived_unprovisioned_device_for_pcid(
        self, platform_customer_id, device_type="SWITCH"
    ):
        """
        Use this function to get a device that is in unarchived and unassigned state and for the given device_type for a given PCID
        platform_customer_id: PCID of customer
        device_type: type of device. Can be one of ["ALS" "AP" "BLE" "COMPUTE" "CONTROLLER" "DHCI_COMPUTE" "DHCI_STORAGE" "EINAR" "EINR" "GATEWAY" "IAP" "LTE_MODEM" "MC" "STORAGE" "SWITCH" "NW_THIRD_PARTY" "PCE" "UNKNOWN"]
        return: Device that is unarchived for given PCID and device_type, False if such device not found
        """
        devices_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id,
            device_type=device_type,
            archived_only="HIDE_ARCHIVED",
        )

        if devices_response:
            # loop until we find a device that is unassigned
            dict_response = devices_response.json()
            for device in dict_response["devices"]:
                log.debug("DEVICE INFO {}".format(device))
                if not self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    return device

        return False

    def get_unarchived_device_for_pcid(self, platform_customer_id, device_type) -> list:
        """
        Get unarchived devices for Platform customer.
        return: List of unarchived devices.
        """
        unarchived_devices_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id,
            device_type=device_type,
            archived_only="HIDE_ARCHIVED",
        )

        log.info(unarchived_devices_response.json())

        unarchived_device = unarchived_devices_response.json()["devices"]
        if len(unarchived_device) == 0:
            log.info("No device found in the account!!")
            return unarchived_device
        return unarchived_device

    @staticmethod
    def get_device_of_type_for_pcid(app_api_session, pcid, device_type="AP"):
        """
        Method to get a device of given type
        :param app_api_session: Authorization bearer token
        :param pcid: Platform Customer ID
        :param device_type: device type. default is AP
        :return: a device for given type
        """

        response = app_api_session.get_devices_by_pcid(
            platform_customer_id=pcid, device_type=device_type
        )

        response_dict = response.json()
        response_pagination = response_dict["pagination"]

        # if account has devices, return device
        if response_pagination["total_count"] > 0:
            return response_dict["devices"][0]

        return False

    @staticmethod
    def get_a_device_for_pcid(app_api_session, pcid):
        """
        Method to get a device for a platform customer
        :param app_api_session: Authorization bearer token
        :param pcid: Platform Customer ID
        :return: a device for given type
        """

        response = app_api_session.get_devices_by_pcid(platform_customer_id=pcid)

        response_dict = response.json()
        response_pagination = response_dict["pagination"]

        # if account has devices, return device
        if response_pagination["total_count"] > 0:
            return response_dict["devices"][0]

        return False

    @staticmethod
    def remove_rma_devices_from_customer_account(
        rma_app_api_session, device_category, device_list
    ):
        """
         Remove the RMA device from customer's account and move to Factory-Stock
           :param rma_app_api_session: API session.
           :param device_category: device category of devices
           :param device_list: type (list) List of device details to removed from customer account
        :return API response for removal of RMA API call
        """
        rma_devices_list = []
        if isinstance(device_list, list):
            for device in device_list:
                sample_device_data = {
                    "serial_number": device["serial_number"],
                    "part_number": device["part_number"],
                    "case_details": {
                        "case_number": RandomGenUtils.random_string_of_chars(
                            7, digits=True
                        ),
                        "open_timestamp": int(time.time() - 24 * 60 * 60),
                        "close_timestamp": int(time.time()),
                        "contact_email": f"{RandomGenUtils.random_string_of_chars(7)}@gamil.com",
                    },
                }
                rma_devices_list.append(deepcopy(sample_device_data))
        return rma_app_api_session.rma_devices(device_category, rma_devices_list)

    def get_multiple_device_data_for_rma(
        self, device_number, device_status, platform_customer_id, device_type="AP"
    ):
        """
         Use this function to get given number of device that is either unassigned or assigned to any application for a given PCID
           :param device_number: number of devices
           :param device_status: Status of devices either provisioned or unprovisoned
           :param platform_customer_id: Platform customer id of the account
           :param device_type: device type of device
        :return device details for given PCID and device_type, False if no device found
        """
        device_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id, device_type=device_type
        )
        device_list = []
        if device_response:
            dict_response = device_response.json()
            for device in dict_response["devices"]:
                log.info("DEVICE INFO {}".format(device))
                if device_status == "provisioned" and self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    device_list.append(device)
                elif (
                    device_status == "unprovisioned"
                    and not self.is_device_provisioned_to_pcid(
                        platform_customer_id, device["serial_number"]
                    )
                ):
                    device_list.append(device)
                if len(device_list) == device_number:
                    return device_list
        return False

    def claim_multiple_devices(
        self, device_list, pcid, username, app_category, acid=None
    ):
        """
         Method to claim devices in a platform customer account
           :param device_list:type(list) list of devices
           :param pcid: Platform customer id of the account
           :param username: username of customer
           :param app_category: app category for devices
           :param acid: application customer id of application
        :return  response for claim device
        """
        for device in device_list:
            device.update({"app_category": app_category})
        claim_response = self.claim_devices(pcid, username, device_list, acid)
        return claim_response

    def fetch_unprovisioned_device_from_activate(
        self, platform_customer_id, device_type="AP", username=None
    ):
        """
        Retrieves an unprovisioned device for a given PCID.

        This function searches for an unassigned device of the specified type ('AP' by default) associated with the given PCID.
        If an unprovisioned device is found, it returns a dictionary containing device information.
        If no unprovisioned device is found, it attempts to obtain a provisioned device and unassign it, returning it as an unprovisioned device.
        If no suitable device is found in the PCID, it claims a device from the AFS PCID and returns its information.

        :param: platform_customer_id (str): The PCID of the customer.
        :param: device_type (str, optional): Type of device to search for (default is 'AP').
        :param: username (str, optional): The username associated with the device (default is None).

        :returns: dict: A dictionary containing device information.
        :raises: Exception: If an invalid device_type is provided or if any provisioning or claiming operation fails.
        """
        # Check if the provided device_type is valid
        get_device = AdiInputPayload()
        if device_type not in get_device.app_category_for_device_type():
            raise Exception(f"Invalid device_type: {device_type}")

        # Get the corresponding category for the device_type
        app_category = get_device.app_category_for_device_type()[device_type]

        device_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id, device_type=device_type
        )

        if device_response:
            # loop until we find a device for given device_type that is unassigned
            dict_response = device_response.json()
            for device in dict_response["devices"]:
                if not self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    return device

        # If no unprovisioned device is found, move to provisioned device search
        device = self.get_provisioned_device_for_pcid(
            platform_customer_id, device_type=device_type
        )
        if device:
            serial_number = device["serial_number"]
            part_number = device["part_number"]
            if "mac_address" in device:
                mac_address = device["mac_address"]
            else:
                mac_address = None

            payload = {
                "serial_number": serial_number,
                "mac_address": mac_address,
                "device_type": device_type,
                "part_number": part_number,
            }
            # Unprovision the provisioned device
            unprovision_device_response = self.unprovision_device_from_application(
                payload=payload
            )
            log.info(
                "Response of unassign the provisioned_device {}".format(
                    unprovision_device_response.json()
                )
            )
            if unprovision_device_response.status_code != 200:
                raise Exception(
                    f"Unprovisioning failed with status_code {unprovision_device_response.status_code}"
                )
            return device

        # If no suitable device is found, move to AFS search
        afs_pcid = "Aruba-Factory-CCS-Platform"
        device_response = self.get_devices_by_pcid(
            platform_customer_id=afs_pcid, limit=1, device_type=device_type
        )
        dict_response = device_response.json()

        device_found = False  # Add a flag to track if a device is found

        for device in dict_response.get("devices", []):
            serial_number = device["serial_number"]
            part_number = device["part_number"]
            mac_address = device.get("mac_address", None)
            log.info("Found the device using AFS pcid: {}".format(device))
            device_found = True  # Set the flag to True when a device is found
            break

        if not device_found:
            raise Exception("No device found.")

        # Prepare device payload
        device_list = [
            {
                "app_category": app_category,
                "serial_number": serial_number,
                "mac_address": mac_address,
                "part_number": part_number,
            }
        ]
        # Attempt to claim the device
        claim_response = self.claim_devices(
            pcid=platform_customer_id, username=username, device_list=device_list
        )

        log.info("Claim response :{}".format(claim_response.json()))
        if (
            claim_response.status_code != 200
            or serial_number not in claim_response.json()["meta"]["claimed"]
        ):
            raise Exception(
                f"Claiming the device failed with status_code {claim_response.status_code}"
            )

        if self.is_device_provisioned_to_pcid(platform_customer_id, serial_number):
            payload = {
                "serial_number": serial_number,
                "device_type": device_type,
                "part_number": part_number,
                "mac_address": mac_address,
            }
            # Unprovision the device
            unprovisioned_device = self.unprovision_device_from_application(
                payload=payload
            )
            log.info(
                "Response of unprovisioned device {}".format(unprovisioned_device.json())
            )
            if unprovisioned_device.status_code != 200:
                raise Exception(
                    f"Unprovisioning failed with status_code {unprovisioned_device.status_code}"
                )

        return device

    def fetch_provisioned_device_from_activate(
        self, platform_customer_id, device_type="AP", username=None, acid=None
    ):
        """
        Retrieves a provisioned device for a given PCID.

        This function searches for a device of the specified type ('AP' by default) associated with the given PCID that is already provisioned (assigned to an application).
        If a provisioned device is found, it returns a dictionary containing device information.
        If no provisioned device is found, it attempts to obtain an unprovisioned device, assign it, and return it as a provisioned device.
        If no suitable device is found in the PCID, it claims a device from the AFS PCID, assigns it to an application, and returns its information.

        :param: platform_customer_id (str): The PCID of the customer.
        :param: device_type (str, optional): Type of device to search for (default is 'AP').
        :param: username (str, optional): The username associated with the device (default is None).
        :param: acid (str, optional): The acid associated with the device (default is None).

        :returns: dict: A dictionary containing device information.
        :raises: Exception: If an invalid device_type is provided or if any provisioning or claiming operation fails.
        """
        # Check if the provided device_type is valid
        get_device = AdiInputPayload()
        if device_type not in get_device.app_category_for_device_type():
            raise Exception(f"Invalid device_type: {device_type}")

        # Get the corresponding category for the device_type
        app_category = get_device.app_category_for_device_type()[device_type]

        device_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id, device_type=device_type
        )

        if device_response:
            # loop until we find a device for given device_type that is unassigned
            dict_response = device_response.json()
            for device in dict_response["devices"]:
                if self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    return device

        # If no provisioned device is found, move to unprovisioned device search
        device = self.get_unprovisioned_device_for_pcid(
            platform_customer_id, device_type=device_type
        )
        if device:
            serial_number = device["serial_number"]
            part_number = device["part_number"]
            if "mac_address" in device:
                mac_address = device["mac_address"]
            else:
                mac_address = None

            payload = {
                "serial_number": serial_number,
                "device_type": device_type,
                "part_number": part_number,
                "mac_address": mac_address,
            }
            # Provision the unprovisioned device
            provisioned_device = self.provision_dev_acid(payload=payload, acid=acid)
            log.info(
                "Response of provisioned_device {}".format(provisioned_device.json())
            )
            if provisioned_device.status_code != 200:
                raise Exception(
                    f"Provisioning failed with status_code {provisioned_device.status_code}"
                )

            return device

        # If no suitable device is found, move to AFS search
        afs_pcid = "Aruba-Factory-CCS-Platform"
        device_response = self.get_devices_by_pcid(
            platform_customer_id=afs_pcid, limit=1, device_type=device_type
        )
        dict_response = device_response.json()

        device_found = False  # Add a flag to track if a device is found

        for device in dict_response.get("devices", []):
            serial_number = device["serial_number"]
            part_number = device["part_number"]
            mac_address = device.get("mac_address", None)
            log.info("Found the device using AFS pcid: {}".format(device))
            device_found = True  # Set the flag to True when a device is found
            break

        if not device_found:
            raise Exception("No device found.")

        # Prepare device list
        device_list = [
            {
                "app_category": app_category,
                "serial_number": serial_number,
                "part_number": part_number,
                "mac_address": mac_address,
            }
        ]
        # Attempt to claim the device
        claim_response = self.claim_devices(
            pcid=platform_customer_id,
            username=username,
            device_list=device_list,
            acid=acid,
        )

        log.info("Claim response :{}".format(claim_response.json()))
        if (
            claim_response.status_code != 200
            or serial_number not in claim_response.json()["meta"]["claimed"]
        ):
            raise Exception(
                f"Claiming the device failed with status_code {claim_response.status_code}"
            )

        if not self.is_device_provisioned_to_pcid(platform_customer_id, serial_number):
            # Prepare payload
            payload = {
                "serial_number": serial_number,
                "device_type": device_type,
                "part_number": part_number,
                "mac_address": mac_address,
            }
            # Provision the unprovisioned device
            provisioned_device_response = self.provision_dev_acid(
                acid=acid, payload=payload, platform_customer_id=platform_customer_id
            )
            log.info(
                "Response of the device {}".format(provisioned_device_response.json())
            )
            if provisioned_device_response.status_code != 200:
                raise Exception(
                    f"Provisioning failed with status_code {provisioned_device_response.status_code}"
                )

        return device

    def get_multiple_unprovisioned_device_data(
        self, device_number, platform_customer_id, device_type="AP"
    ):
        """
        Use this function to get given number of device that is either unassigned or assigned to any application for a
        given PCID
        :param device_number: number of devices
        :param platform_customer_id: Platform customer id of the account
        :param device_type: device type of device
        :return device details for given PCID and device_type, False if no device found
        """
        device_response = self.get_devices_by_pcid(
            platform_customer_id=platform_customer_id, device_type=device_type
        )
        device_list = []
        if device_response:
            dict_response = device_response.json()
            for device in dict_response["devices"]:
                if not self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    device_list.append(device)
                if len(device_list) == device_number:
                    return device_list
        return False
