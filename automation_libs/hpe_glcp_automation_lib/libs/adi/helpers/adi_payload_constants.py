import datetime
import json
import logging
import time
import uuid

from hpe_glcp_automation_lib.libs.commons.enum.enum_utils import DeviceType, EventType
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class AdiInputPayload:
    @staticmethod
    def get_ip_address_list():
        return ["104.36.248.13", "100.10.1.9", "101.10.1.7", "2.7.8.9"]

    @staticmethod
    def aop_device_event():
        aop_device_event = {
            "specversion": "1.0.0",
            "id": "1056afd0-11bc-4788-90a9-d92448b48308",
            "source": "CCS",
            "type": "AOP_DEVICE_EVENT",
            "topic": "activate-internal",
            "time": "2023-01-01T10:10:10Z",
            "data": {
                "devices": [
                    {
                        "device_type": "STORAGE",
                        "serial_number": "TESTSERIAL",
                        "part_number": "TESTPART",
                        "device_model": "testLEModel",
                        "platform_customer_id": "Aruba-Factory-CCS-Platform",
                        "activate_customer_id": "Aruba-Factory-Stock",
                    }
                ]
            },
        }

        return aop_device_event

    @staticmethod
    def create_aop_device_event(
        serial_number=None, part_number=None, mac_address=None, device_type=DeviceType.AP
    ):
        aop_device_event_payload = AdiInputPayload.aop_device_event()

        if serial_number is None:
            serial_number = "SNA" + RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=True
            )

        if part_number is None:
            part_number = "PNA" + RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=True
            )

        aop_device_event_payload["id"] = uuid.uuid4().hex
        aop_device_event_payload["data"]["devices"][0]["serial_number"] = serial_number
        aop_device_event_payload["data"]["devices"][0]["part_number"] = part_number
        if mac_address:
            aop_device_event_payload["data"]["devices"][0]["eth_mac"] = mac_address
        aop_device_event_payload["data"]["devices"][0]["device_type"] = str(device_type)
        aop_device_event_payload["data"] = json.dumps(aop_device_event_payload["data"])

        return aop_device_event_payload

    @staticmethod
    def device_history_event():
        device_history_event = {
            "specversion": "1.0.0",
            "id": "1056afd0-11bc-4788-90a9-d92448b48308",
            "source": "CCS",
            "type": "CCS_DEVICE_HISTORY_EVENT",
            "topic": "activate-internal",
            "time": "2023-01-01T10:10:10Z",
            "data": {
                "device_histories": [
                    {
                        "serial_number": "TESTSERIAL",
                        "part_number": "PN101",
                        "device_model": "testHistoryModel",
                        "date": "1641600000",
                        "type": "PROVISION",
                        "source_ip": "10.3.5.67",
                        "current_version": "v1234",
                        "mode": "IAP",
                        "description": "device history ft test",
                        "status": "success",
                        "folder_id": "f12345678",
                        "folder_name": "testFolder",
                        "rule_id": "r12345678",
                        "rule_name": "testRule",
                        "app_name": "ADD",
                        "platform_customer_id": "platformCustomerId",
                    }
                ]
            },
        }

        return device_history_event

    @staticmethod
    def create_device_history_event_payload(
        serial_number=None, part_number=None, source_ip=None, platform_customer_id=None
    ):
        """
        Helper method to generate device history event
        :param serial_number: Serial number of device
        :param part_number: Part number of device
        :param source_ip: Source IP reported by device when connected to ADD for provisioning
        :return: Device history event payload
        """

        device_history_payload = AdiInputPayload.device_history_event()

        if serial_number is None:
            serial_number = "SNH" + RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=True
            )

        if part_number is None:
            part_number = "PNH" + RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=True
            )

        if source_ip is None:
            source_ip = AdiInputPayload.get_ip_address_list()[0]

        device_history_payload["id"] = uuid.uuid4().hex
        device_history_payload["data"]["device_histories"][0][
            "serial_number"
        ] = serial_number
        device_history_payload["data"]["device_histories"][0]["part_number"] = part_number
        device_history_payload["data"]["device_histories"][0]["source_ip"] = source_ip
        device_history_payload["data"]["device_histories"][0]["date"] = str(
            round(time.time())
        )
        if platform_customer_id:
            device_history_payload["data"]["device_histories"][0][
                "platform_customer_id"
            ] = platform_customer_id
        device_history_payload["data"] = json.dumps(device_history_payload["data"])

        return device_history_payload

    @staticmethod
    def app_provision_event():
        app_provision_event_data = {
            "specversion": "1.0.0",
            "id": "1056afd0-11bc-4788-90a9-d92448b48308",
            "source": "CCS",
            "type": "APP_PROVISION",
            "topic": "app.account-management.users.CCS",
            "time": "2023-01-01T10:10:10Z",
            "data": {
                "event": {
                    "username": "first-ft-user@test.com",
                    "provision_status": "PROVISIONED",
                    "account_type": "STANDALONE",
                    "region": "US-WEST2",
                    "application_id": "applicationId",
                    "platform_customer_id": "platformCustomerId",
                    "application_instance_id": "applicationInstanceId",
                    "application_customer_id": "applicationCustomerId",
                    "msp_id": None,
                },
                "operation": "CREATE",
                "status": "SUCCESS",
                "failure_reason": None,
            },
        }

        return app_provision_event_data

    @staticmethod
    def device_internal_provision_event():
        device_provision_event_data = {
            "specversion": "1.0.0",
            "id": "uuid",
            "source": "CCS",
            "type": "APP_PROVISION",
            "topic": "activate-internal",
            "time": "2023-01-01T10:10:10Z",
            "data": {
                "mac_address": None,
                "serial_number": "serialNumber",
                "device_type": "IAP",
                "part_number": "partNumber",
                "device_model": "deviceModel",
                "platform_subscription_category": None,
                "platform_subscription_category_description": None,
                "is_archived": False,
                "iaas": False,
                "entitlement_id": None,
                "location_id": None,
                "contact_id": None,
                "platform_customer": {
                    "platform_customer_id": "platformCustomerId",
                    "msp_id": None,
                },
                "application_customers": [
                    {
                        "application_customer_id": "applicationCustomerId",
                        "application_instance_id": None,
                        "application_id": None,
                        "msp_id": None,
                    }
                ],
                "extra_attributes": [
                    {"name": "extraAttributeName", "value": "extraAttributeValue"}
                ],
                "tags": [
                    {
                        "created_by": "createdByFtUser",
                        "name": "tagName",
                        "value": "tagValue",
                    }
                ],
                "resource_id": "resourceId",
            },
        }

        return device_provision_event_data

    @staticmethod
    def create_device_internal_event_payload(
        serial_number=None,
        part_number=None,
        mac_address=None,
        device_type=DeviceType.IAP,
        device_model=None,
        platform_subscription_category=None,
        is_archived=False,
        iaas=False,
        location_id=None,
        platform_customer_id=None,
        application_customer_id=None,
        application_instance_id=None,
        msp_platform_customer_id=None,
        msp_application_customer_id=None,
        event_type=EventType.DEVICE_PROVISION_INTERNAL_EVENT,
    ):
        """
        Generates event payload to send device provision/unprovision internal event
        :param serial_number:
        :param part_number:
        :param mac_address:
        :param device_type:
        :param device_model:
        :param platform_subscription_category:
        :param is_archived:
        :param iaas:
        :param location_id:
        :param platform_customer_id:
        :param application_customer_id:
        :param application_instance_id:
        :param msp_platform_customer_id:
        :param msp_application_customer_id:
        :param event_type:
        :return:
        """

        device_internal_event = AdiInputPayload.device_internal_provision_event()

        if platform_customer_id is None:
            log.error(
                "Failed to send device provision event as platform customer id is empty"
            )
            return None

        if application_customer_id is None:
            log.error(
                "Failed to send device provision event for platform customer id {} as application customer id "
                "is empty".format(platform_customer_id)
            )
            return None

        if application_instance_id is None:
            log.error(
                "Failed to send device provision event for platform customer id {} as application instance id "
                "is empty".format(platform_customer_id)
            )
            return None

        if serial_number is None:
            log.error(
                "Failed to send device provision event for platform customer id {} as device serial is empty".format(
                    platform_customer_id
                )
            )
            return None

        if part_number is None:
            log.error(
                "Failed to send device provision event for platform customer id:{}, serial: {} as device part "
                "number is empty".format(platform_customer_id, serial_number)
            )
            return None

        if device_model is None:
            log.error(
                "Failed to send device provision event for platform customer id:{}, serial: {} as device model "
                "is empty".format(platform_customer_id, serial_number)
            )
            return None

        device_internal_event["id"] = str(uuid.uuid4())
        device_internal_event["time"] = datetime.datetime.now().isoformat()
        device_internal_event["type"] = str(event_type)

        device_internal_event["data"]["serial_number"] = serial_number
        device_internal_event["data"]["part_number"] = part_number
        device_internal_event["data"]["device_model"] = device_model
        device_internal_event["data"]["device_type"] = str(device_type)
        device_internal_event["data"]["mac_address"] = mac_address
        device_internal_event["data"][
            "platform_subscription_category"
        ] = platform_subscription_category
        device_internal_event["data"]["location_id"] = location_id
        device_internal_event["data"]["is_archived"] = is_archived
        device_internal_event["data"]["iaas"] = iaas
        device_internal_event["data"]["resource_id"] = device_internal_event["id"]
        device_internal_event["data"]["platform_customer"][
            "platform_customer_id"
        ] = platform_customer_id
        device_internal_event["data"]["platform_customer"][
            "msp_id"
        ] = msp_platform_customer_id

        for i in range(0, len(device_internal_event["data"]["application_customers"])):
            device_internal_event["data"]["application_customers"][i][
                "application_customer_id"
            ] = application_customer_id
            device_internal_event["data"]["application_customers"][i][
                "application_instance_id"
            ] = application_instance_id
            device_internal_event["data"]["application_customers"][i][
                "msp_id"
            ] = msp_application_customer_id

        device_internal_event["data"] = json.dumps(device_internal_event["data"])

        return device_internal_event
