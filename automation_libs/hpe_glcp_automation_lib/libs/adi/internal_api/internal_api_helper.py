import logging
import random
import uuid

from hpe_glcp_automation_lib.libs.acct_mgmt.helpers.acct_mgmt_payload_constants import (
    AmInputPayload,
)
from hpe_glcp_automation_lib.libs.adi.helpers.adi_payload_constants import AdiInputPayload
from hpe_glcp_automation_lib.libs.adi.internal_api.adi_internal_api import (
    ActivateInventoryInternal,
)
from hpe_glcp_automation_lib.libs.commons.enum.enum_utils import (
    AccountType,
    DeviceType,
    Operation,
    OperationStatus,
    ProvisionStatus,
)
from hpe_glcp_automation_lib.libs.locations.helpers.lm_payload_constants import (
    LMInputPayload,
)

log = logging.getLogger(__name__)


class ActivateInventoryInternalApiHelper(ActivateInventoryInternal):
    """
    ActivateInventory Internal API Helper Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Activate Inventory Helper for internal api calls")
        super(ActivateInventoryInternalApiHelper, self).__init__(
            max_retries=max_retries,
            retry_timeout=retry_timeout,
            debug=debug,
            **kwargs,
        )

    def invoke_get_devices_history(
        self,
        start_time,
        end_time,
        countries,
        offset=0,
        limit=1000,
        distinct=True,
    ):
        """
        Method to fetch list of devices by countries and duration
        countries : List of 2 letter country codes for fetching the devices
        start_time : Start time in epoch
        end_time : End time in epoch
        limit : Pagination limit. Max is 1000
        offset : Default value is set to 0
        distinct : Default is set to False
        """
        log.info(
            "Fetching the device history from the countries : {} and in the time range Start time: {} and End time : {}".format(
                countries, start_time, end_time
            )
        )
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "countries": countries,
            "offset": offset,
            "limit": limit,
            "distinct": distinct,
        }
        return self.get_device_history(**params)

    def invoke_get_blocked_devices(self, offset=0, limit=1000):
        """
        Method to get list of blocked devices
        limit : Pagination limit. Max is 1000
        offset : Default value is set to 0
        """
        log.info("Getting the blocked list of devices")
        params = {"offset": offset, "limit": limit}
        return self.get_blocked_devices(**params)

    def invoke_update_device_block_status(self, operation, devices):
        """
        Method to update the status of the blocked devices
        operation : Set the value to 'firmware_lock' to block a device and 'firmware_unlock' to unblock
        devices: List of devices in key value pairs Example: [{"serial_number":"SN4GZJS5T","part_number":"PNQXKHCQL"},
                                                              {"serial_number":"SN9B72CQV","part_number":"PNLLCW6WI"}]
        """
        log.info(
            "Updating the device(s) status with the operation : {}".format(operation)
        )
        params = {"operation": operation}
        device_payload = {"devices": devices}
        return self.update_device_block_status(device_payload, **params)

    def invoke_get_device_inventory(
        self,
        pcid,
        serialNumber=None,
        type=None,
        select=None,
        sort=None,
        limit=None,
        offset=None,
    ):
        """
        Method to get device inventory for the given Platform Customer ID and with optional params
        serialNumber : Device Serial Number
        limit : Pagination limit. Max is 2000
        offset : Pagination offset
        type : Device type 'STORAGE' or 'COMPUTE'
        select : Can be set to 'application', 'childDevices', 'folder', 'tags' or 'subscription'
        sort : Sort the results by asc or desc. Default asc
        """
        params = dict()
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if serialNumber:
            params["serialNumber"] = serialNumber
        if type:
            params["type"] = type
        if sort:
            params["sort"] = sort
        if select:
            params["select"] = select
        return self.get_device_inventory(pcid, **params)

    def get_unprovisioned_device_for_pcid(self, platform_customer_id, device_type="IAP"):
        """
        Use this function to get a device that is unassigned to any application for a given PCID.
        platform_customer_id: PCID of customer
        device_type: Device type (default: 'IAP')
        return: Device that is unassigned
        """
        devices_response = self.get_devices_by_pcid(
            platform_id=platform_customer_id, device_type=device_type
        )

        if devices_response:
            dict_response = devices_response.json()
            devices = dict_response.get("devices", [])

            for device in devices:
                if not self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    return device

        return {}

    def get_provisioned_device_for_pcid(self, platform_customer_id, device_type="IAP"):
        """
        Use this function to get a device that is assigned to any application for a given PCID.
        pcid: Platform Customer ID
        device_type: Device type (default: 'IAP')
        return: Device that is assigned
        """
        devices_response = self.get_devices_by_pcid(
            platform_id=platform_customer_id, device_type=device_type
        )

        if devices_response:
            dict_response = devices_response.json()
            devices = dict_response.get("devices", [])

            for device in devices:
                if self.is_device_provisioned_to_pcid(
                    platform_customer_id, device["serial_number"]
                ):
                    return device

        return {}

    def is_device_provisioned_to_pcid(
        self, platform_customer_id, serial_number=None, mac_address=None
    ):
        """
        Use this function to check if the device is assigned to an application (provisioned) for a given PCID.
        platform_customer_id: PCID of customer
        serial_number: Device serial number (optional)
        mac_address: Device MAC address (optional)
        return: True if any device is provisioned/assigned, False if no device is provisioned
        """
        devices_response = self.get_devices_by_pcid(
            platform_id=platform_customer_id, serial_number=serial_number
        )
        if devices_response:
            devices = devices_response.json().get("devices", [])

            for device_data in devices:
                if (
                    serial_number and device_data.get("serial_number") == serial_number
                ) or (mac_address and device_data.get("mac_address") == mac_address):
                    return device_data.get("application_customer_id") is not None

        return False

    def onboard_application_instance(
        self,
        platform_customer_id,
        username,
        application_instance_id,
        application_id,
        provisioning_data,
        device_types=None,
        deployment_private=False,
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

        # Create application instance
        return self.create_application_instance(
            transaction_id=None,
            platform_customer_id=platform_customer_id,
            username=username,
            payload=payload,
        )

    def verify_claim_device(self, platform_customer_id, serial_number):
        """
        "Verify if the device is claimed by the platform customer given the serial number using the prepare_device_summary method."
        Returns True if the serial number is found in the list of devices, False otherwise.
        :param  platform_customer_id :platform_customer_id
        :param serial_number:serial_number of the device
        """

        # Assuming the self.get_device_summary() method takes serial_number as a filter argument
        device_summary = self.get_device_summary(
            platform_customer_id=platform_customer_id, serial_number_list=[serial_number]
        ).json()
        devices = device_summary.get("devices", [])
        if devices:
            return True
        return False

    def send_platform_customer_event(
        self, platform_customer_id=None, account_type=AccountType.STANDALONE
    ):
        try:
            # 1. Generate Platform customer event payload
            platform_event = AmInputPayload.create_platform_event_payload(
                platform_customer_id=platform_customer_id, account_type=account_type
            )
            log.info(
                f"Platform customer event for {platform_customer_id} => {platform_event}"
            )
            # 2. Publish platform event
            response = self.send_internal_event(
                platform_customer_id=platform_customer_id, internal_event=platform_event
            )

            log.info(
                f"Response of platform customer event for {platform_customer_id} => {response}"
            )
            return platform_event, response
        except Exception as ex:
            log.error(
                f"Error while sending platform customer event[{platform_customer_id}]:\n{ex}"
            )
            return None

    def send_app_provision_event(
        self,
        platform_customer_id=None,
        provision_status=ProvisionStatus.PROVISIONED,
        account_type=AccountType.STANDALONE,
        application_id=None,
        application_instance_id=None,
        application_customer_id=None,
        msp_application_customer_id=None,
    ):
        """

        :param platform_customer_id:
        :param provision_status:
        :param account_type:
        :param application_id:
        :param application_instance_id:
        :param application_customer_id:
        :param msp_application_customer_id:
        :return:
        """

        try:
            # 1. Generate App provision event payload
            application_provision_event = (
                AmInputPayload.create_app_provision_event_payload(
                    provision_status=provision_status,
                    account_type=account_type,
                    application_id=application_id,
                    application_instance_id=application_instance_id,
                    platform_customer_id=platform_customer_id,
                    application_customer_id=application_customer_id,
                    operation=Operation.CREATE,
                    operation_status=OperationStatus.SUCCESS,
                    msp_application_customer_id=msp_application_customer_id,
                )
            )

            log.info(
                f"Application provision event for platform_id:{platform_customer_id}, application_customer_id:"
                f"{application_customer_id} => {application_provision_event}"
            )

            # 2. Publish application provision event
            response = self.send_internal_event(
                platform_customer_id=platform_customer_id,
                internal_event=application_provision_event,
            )
            log.info(
                f"Response of application provision event for platform_id:{platform_customer_id}, "
                f"application_customer_id:{application_customer_id} => {response}"
            )
            return application_provision_event, response
        except Exception as ex:
            log.error(
                f"Error while sending application provision event[platform_id: {platform_customer_id},"
                f" application_customer_id:{application_customer_id}]:\n{ex}"
            )
            return None

    def send_aop_device_event(
        self,
        platform_customer_id=None,
        serial_number=None,
        part_number=None,
        mac_address=None,
        device_type=DeviceType.AP,
    ):
        try:
            # 1. Generate aop device event payload
            if serial_number is None:
                log.error(
                    f"Received empty serial number while publishing aop device event for "
                    f"platform_id {platform_customer_id}"
                )
                return None
            if part_number is None:
                log.error(
                    f"Received empty part number while publishing aop device event for "
                    f"platform_id:{platform_customer_id}, serial number:{serial_number}"
                )
                return None

            aop_device_event = AdiInputPayload.create_aop_device_event(
                serial_number=serial_number,
                part_number=part_number,
                mac_address=mac_address,
                device_type=device_type,
            )
            log.info(f"AOP device event => {aop_device_event}")
            # 2. Publish aop device event
            response = self.send_internal_event(
                platform_customer_id=platform_customer_id, internal_event=aop_device_event
            )
            log.info(f"Response of aop device event => {response}")
            return aop_device_event, response
        except Exception as ex:
            log.error(f"Error while sending aop device event:\n{ex}")
            return None

    def send_device_history_event(
        self,
        platform_customer_id=None,
        serial_number=None,
        part_number=None,
        source_ip=None,
    ):
        try:
            if serial_number is None:
                log.error(
                    f"Received empty serial number while publishing device history event for "
                    f"platform_id {platform_customer_id}"
                )
                return None
            if part_number is None:
                log.error(
                    f"Received empty part number while publishing device history event for "
                    f"platform_id:{platform_customer_id}, serial number:{serial_number}"
                )
                return None
            if source_ip is None:
                ind = random.randrange(len(AdiInputPayload.get_ip_address_list()))
                source_ip = AdiInputPayload.get_ip_address_list()[ind]

            # 1. Generate Platform customer event payload
            device_history_event = AdiInputPayload.create_device_history_event_payload(
                serial_number=serial_number,
                part_number=part_number,
                source_ip=source_ip,
                platform_customer_id=platform_customer_id,
            )
            log.info(f"Device history event => {device_history_event}")
            # 2. Publish internal event for device history
            response = self.send_internal_event(
                platform_customer_id=platform_customer_id,
                internal_event=device_history_event,
            )
            log.info(f"Response of device history event => {response}")
            return device_history_event, response
        except Exception as ex:
            log.error(f"Error while sending device history event:\n{ex}")
            return None

    def send_location_update_event(
        self,
        platform_customer_id=None,
        old_location_id=None,
        new_location_name=None,
        new_location_id=None,
        new_street_address="1 America Dr",
        new_county="Unites States",
        new_state="CA",
        new_city="San Jose",
    ):
        try:
            if old_location_id is None:
                log.error(
                    f"Received empty old_location_id while publishing location update event for "
                    f"platform_id {platform_customer_id}"
                )
                return None
            if new_location_name is None:
                log.error(
                    f"Received empty new_location_name while publishing location update event for "
                    f"platform_id {platform_customer_id}"
                )
                return None
            if new_location_id is None:
                log.error(
                    f"Received empty new_location_id while publishing location update event for "
                    f"platform_id {platform_customer_id}"
                )
                return None

            # 1. Generate location delete event payload
            location_update_event = LMInputPayload.update_location_event(
                platform_customer_id=platform_customer_id,
                old_location_id=old_location_id,
                new_location_name=new_location_name,
                new_location_id=new_location_id,
                new_street_address=new_street_address,
                new_county=new_county,
                new_state=new_state,
                new_city=new_city,
            )
            log.info(f"Location update event => {location_update_event}")
            # 2. Publish internal event for location update
            response = self.send_internal_event(
                platform_customer_id=platform_customer_id,
                internal_event=location_update_event,
            )
            log.info(f"Response of location update event => {response}")
            return location_update_event, response
        except Exception as ex:
            log.error(f"Error while sending location update event:\n{ex}")
            return None

    def send_location_delete_event(self, platform_customer_id=None, location_id=None):
        try:
            if location_id is None:
                log.error(
                    f"Received empty location_id while publishing location delete event for "
                    f"platform_id {platform_customer_id}"
                )
                return None

            # 1. Generate location delete event payload
            location_delete_event = LMInputPayload.delete_location_event(
                platform_customer_id=platform_customer_id, location_id=location_id
            )
            log.info(f"Location delete event => {location_delete_event}")
            # 2. Publish internal event for location update
            response = self.send_internal_event(
                platform_customer_id=platform_customer_id,
                internal_event=location_delete_event,
            )
            log.info(f"Response of location delete event => {response}")
            return location_delete_event, response
        except Exception as ex:
            log.error(f"Error while sending location delete event:\n{ex}")
            return None

    def get_locations_by_platform_id_and_search_string(
        self, transaction_id, platform_customer_id, search_string
    ):
        """
        Helper method to get locations for given platform customer id and search string
        :param transaction_id: Transaction id
        :param platform_customer_id:
        :param search_string:
        :return:
        """
        try:
            if transaction_id is None:
                transaction_id = (
                    "find_locations_by_platform_id_and_search_string_" + uuid.uuid1().hex
                )

            if platform_customer_id is None:
                log.error(
                    f"Received empty platform_customer_id for find_locations_by_platform_id_and_search_string "
                    f"[transaction_id: {transaction_id}], search_string: {search_string}"
                )
                return None

            response = self.fetch_locations_by_platform_id_and_search_string(
                transaction_id=transaction_id,
                platform_customer_id=platform_customer_id,
                search_string=search_string,
            )
            log.info(
                f"Response of find_locations_by_platform_id_and_search_string "
                f"[platform_id:{platform_customer_id}] => {response.json()}"
            )
            return response
        except Exception as ex:
            log.error(
                f"Error while fetching locations for platform_id: {platform_customer_id} search_string: "
                f"{search_string}\n{ex}"
            )
            return None

    def patch_device_attributes(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        serial_number=None,
        part_number=None,
        mac_address=None,
        archive=None,
        location_id=None,
        location_name=None,
    ):
        try:
            if transaction_id is None:
                transaction_id = "update_device_attributes_" + uuid.uuid1().hex

            if platform_customer_id is None:
                log.error(
                    f"Received empty platform_customer_id for update_device_attributes "
                    f"[transaction_id: {transaction_id}]"
                )
                return None

            if username is None:
                log.error(
                    f"Received empty username for update_device_attributes "
                    f"[transaction_id: {transaction_id}]"
                )
                return None

            device = {}
            if serial_number:
                device["serial_number"] = serial_number
            if part_number:
                device["part_number"] = part_number
            if mac_address:
                device["mac_address"] = mac_address
            if location_id:
                device["location_id"] = location_id
            if location_name:
                device["location_name"] = location_name
            if archive:
                device["archive"] = archive

            device_update_attr_request = {"devices": [device]}

            response = self.update_device_attributes(
                platform_customer_id, username, device_update_attr_request
            )
            return response
        except Exception as ex:
            log.error(
                f"Error while updating device attributes for transaction_id: {transaction_id}, "
                f"platform_id: {platform_customer_id}\n{ex}"
            )
            return None

    def claim_device(
        self,
        transaction_id=None,
        platform_customer_id=None,
        application_customer_id=None,
        username=None,
        device_category="NETWORK",
        serial_number=None,
        mac_address=None,
        part_number=None,
        entitlement_id=None,
        location_id=None,
        csv_import=False,
    ):
        try:
            device_list = {}
            if device_category == "NETWORK":
                device_list = [
                    {
                        "serial_number": serial_number,
                        "mac_address": mac_address,
                        "app_category": device_category,
                    }
                ]

            elif device_category == "STORAGE":
                device_list = [
                    {
                        "serial_number": serial_number,
                        "entitlement_id": entitlement_id,
                        "app_category": device_category,
                    }
                ]

            elif device_category == "COMPUTE":
                device_list = [
                    {
                        "serial_number": serial_number,
                        "part_number": part_number,
                        "app_category": device_category,
                    }
                ]
            elif device_category == "PCE":
                device_list = [
                    {
                        "serial_number": serial_number,
                        "app_category": device_category,
                    }
                ]

            if location_id:
                device_list[0]["location_id"] = location_id

            if transaction_id is None:
                transaction_id = uuid.uuid1().hex

            transaction_id = "claim_device_" + transaction_id

            if platform_customer_id is None:
                log.error(
                    f"Received empty platform_customer_id for claim device"
                    f"[transaction_id: {transaction_id}]"
                )
                return None

            if username is None:
                log.error(
                    f"Received empty username for update_device_attributes "
                    f"[transaction_id: {transaction_id}]"
                )
                return None

            response = self.claim_devices(
                platform_customer_id,
                username,
                device_list,
                transaction_id=transaction_id,
                acid=application_customer_id,
                csv_import=csv_import,
            )
            return response
        except Exception as ex:
            log.error(
                f"Error while claiming device [transaction_id: {transaction_id}, "
                f"platform_id: {platform_customer_id}]\n{ex}"
            )
            return None

    def get_devices_for_platform_cid(
        self,
        platform_customer_id=None,
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
        :param platform_customer_id:
        :param limit:
        :param page:
        :param device_type:
        :param archive_visibility:
        :param search_string:
        :param display_device_types:
        :param application_ids:
        :param tenant_platform_customer_id:
        :param serial_number:
        :param part_number:
        :param unassigned_only:
        :param location_id:
        :param contact_id:
        :param location_ids:
        :param location_search_strings:
        :param device_with_no_sdi_location:
        :param transaction_id:
        :return:
        """
        try:
            if platform_customer_id is None:
                log.error(
                    f"Received empty platform customer id while calling get devices by platform id"
                )
                return None

            if transaction_id is None:
                transaction_id = platform_customer_id
            transaction_id = "get_devices_by_pcid_" + transaction_id

            log.info(
                f"Get devices by platform id:{platform_customer_id}, transaction_id:{transaction_id}"
            )
            response = self.get_devices_by_pcid(
                platform_id=platform_customer_id,
                limit=limit,
                page=page,
                archive_visibility=archive_visibility,
                search_string=search_string,
                display_device_types=display_device_types,
                device_type=device_type,
                application_ids=application_ids,
                tenant_platform_customer_id=tenant_platform_customer_id,
                serial_number=serial_number,
                part_number=part_number,
                unassigned_only=unassigned_only,
                location_id=location_id,
                contact_id=contact_id,
                location_ids=location_ids,
                location_search_strings=location_search_strings,
                device_with_no_sdi_location=device_with_no_sdi_location,
                transaction_id=transaction_id,
            )
            return response
        except Exception as ex:
            log.error(
                f"Error while get_devices_by_platform_pcid for transaction_id: {transaction_id}, "
                f"platform_id: {platform_customer_id}\n{ex}"
            )
            return None

    def post_devices_by_platform_pcid(
        self,
        transaction_id=None,
        platform_customer_id=None,
        serial_number=None,
        part_number=None,
        search_string=None,
        location_id=None,
        location_ids=[],
        location_search_strings=[],
        device_with_no_sdi_location=False,
    ):
        """

        :param transaction_id:
        :param platform_customer_id:
        :param serial_number:
        :param part_number:
        :param search_string:
        :param location_id:
        :param location_ids:
        :param location_search_strings:
        :param device_with_no_sdi_location:
        :return:
        """
        try:
            if transaction_id is None:
                transaction_id = uuid.uuid1().hex

            transaction_id = "post_devices_by_platform_pcid_" + transaction_id

            if platform_customer_id is None:
                log.error(
                    f"Received empty platform_customer_id for post_devices_by_platform_pcid "
                    f"[transaction_id: {transaction_id}]"
                )
                return None

            device_app_search_request = {}
            if serial_number:
                device_app_search_request["serial_number"] = serial_number
            if part_number:
                device_app_search_request["part_number"] = part_number
            if location_id:
                device_app_search_request["location_id"] = location_id
            if location_ids:
                device_app_search_request["location_ids"] = location_ids
            if location_search_strings:
                device_app_search_request[
                    "location_search_strings"
                ] = location_search_strings
            device_app_search_request[
                "device_with_no_sdi_location"
            ] = device_with_no_sdi_location

            log.info(
                f"Get[Post] devices by platform id:{platform_customer_id}, transaction_id:{transaction_id},"
                f" request:{device_app_search_request}"
            )
            response = self.post_devices_by_platform_cid(
                transaction_id=transaction_id,
                platform_customer_id=platform_customer_id,
                device_app_search_request=device_app_search_request,
            )
            return response
        except Exception as ex:
            log.error(
                f"Error while filtering devices by platform_pcid for transaction_id: {transaction_id}, "
                f"platform_id: {platform_customer_id}\n{ex}"
            )
            return None

    def get_device_bulk_info_details(self, serials=[], is_app_api=False):
        try:
            if serials is None:
                log.error(f"Received empty serials for get_device_bulk_info.")
                return None

            device_info_request = {"serials": serials}
            log.info(f"Get device details bulk request: {device_info_request}")
            response = self.get_device_bulk_info(
                device_info_request=device_info_request, is_app_api=is_app_api
            )
            return response
        except Exception as ex:
            log.error(
                f"Error while fetching bulk devices by serials: {device_info_request}\n{ex}"
            )
            return None
