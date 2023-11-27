"""
Helper function for Activate Order Processor App Api
"""
import datetime
import logging
import re
import time

import pytest

from hpe_glcp_automation_lib.libs.aop.app_api.aop_app_api import ActivateOrder
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import (
    AopInputPayload,
    OaasConstants,
)
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)
aop_dict = {"manufacture": [], "license": [], "sds": [], "pos": []}
pytest.globalvar = {
    "runtime_testdata": {
        "STORAGE": aop_dict,
        "NETWORK": aop_dict,
        "COMPUTE": aop_dict,
        "PCE": aop_dict,
    }
}
# Global pytest variable will be intialized as pytest.globalvar['runtime_testdata']{'STORAGE': {'manufacture': [],
# 'license': [], 'sds': [], 'pos': []}, 'NETWORK': {'manufacture': [], 'license': [], 'sds': [], 'pos': []},
# 'COMPUTE': {'manufacture': [], 'license': [], 'sds': [], 'pos': []}}
test_run_data = pytest.globalvar["runtime_testdata"]


class NewDeviceOrder:
    """
    Helper class for Activate Order Processor App Api Class
    """

    def __init__(
        self,
        app_api_host,
        deviceCategory,
        deviceType,
        serialNumber,
        macAddress,
        cluster,
        endUsername,
        sso_host,
        aop_client_id,
        aop_client_secret,
    ):
        """
        Initialize NewDeviceOrder class
        :param  app_api_host: App api hostname for cluster
        :param deviceCategory: "COMPUTE" "NETWORK" "STORAGE"
        :param deviceType: IAP, SWITCH, STORAGE, COMPUTE
        :param serialNumber: Device serial number
        :param macAddress: Device mac address
        :param cluster: cluster under test
        :param endUsername: end username same used customer alias for activate inventory
        :param sso_host: sso_host
        :param aop_client_id: aop_client_id
        :param aop_client_secret: aop_client_secret
        """
        if not deviceType:
            raise RuntimeError(
                "Device device_type IAP, or SWITCH, or GATEWAY is required..."
            )

        if not serialNumber:
            raise RuntimeError("Device serial number is required...")

        SERIAL_NUMBER_LENGTH = 30
        if len(serialNumber) > SERIAL_NUMBER_LENGTH:
            raise RuntimeError(
                "Device serial number length should be upto 30 characters..."
            )
        if deviceCategory == "NETWORK":
            if not macAddress:
                raise RuntimeError("Device mac address is required...")

        MAC_REGEX = "^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$"
        if not re.match(MAC_REGEX, macAddress):
            raise RuntimeError(
                'Device mac address is invalid (Expected pattern:"^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$")'
            )

        self.payload = AopInputPayload()
        self.deviceCategory = deviceCategory
        self.device_type = deviceType
        self.serialNumber = serialNumber
        self.macAddress = macAddress
        self.cluster = cluster
        self.app_api_host = app_api_host
        self.end_username = endUsername
        self.sso_host = sso_host
        self.aop_client_id = aop_client_id
        self.aop_client_secret = aop_client_secret
        self.order = ActivateOrder(
            self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret
        )

    def create_manufacturing(self, part, part_category=None, baas=False, MinParams=False):
        """Create manufacturing payload and make manufacture call.

        :param part: Device part number.
        :param part_category: Device part category.
        :param baas: is it BaaS device or not.
        :return: serial number, macaddress
        """
        log.info(
            "Received device_type:"
            + self.device_type
            + " SerialNumber:"
            + self.serialNumber
            + " MacAddress:"
            + self.macAddress
            + " PartNumber:"
            + str(part)
        )
        payload = self.payload.mfr_payload_data()
        payload["manufacturing_data_list"][0]["parent_device"]["obj_key"] = (
            "AOP_OKY_" + self.serialNumber
        )
        payload["manufacturing_data_list"][0]["parent_device"][
            "serial_number"
        ] = self.serialNumber
        payload["manufacturing_data_list"][0]["parent_device"]["part_number"] = part
        payload["manufacturing_data_list"][0]["parent_device"][
            "part_category"
        ] = self.device_type
        payload["manufacturing_data_list"][0]["parent_device"][
            "device_type"
        ] = self.device_type
        if baas:
            payload["manufacturing_data_list"][0]["parent_device"]["extra_attributes"] = [
                {
                    "name": "baas",
                    "value": True,
                }
            ]
        if part_category:
            payload["manufacturing_data_list"][0]["parent_device"][
                "part_category"
            ] = part_category

        if part_category:
            valid_device_type = [
                "ALS",
                "AP",
                "BLE",
                "COMPUTE",
                "CONTROLLER",
                "DHCI_COMPUTE",
                "DHCI_STORAGE",
                "EINAR",
                "EINR",
                "GATEWAY",
                "IAP",
                "LTE_MODEM",
                "MC",
                "STORAGE",
                "SWITCH",
                "NW_THIRD_PARTY",
                "UNKNOWN",
            ]
            if self.device_type not in valid_device_type:
                payload["manufacturing_data_list"][0]["parent_device"][
                    "device_type"
                ] = part_category

        payload["manufacturing_data_list"][0]["parent_device"][
            "eth_mac"
        ] = self.macAddress
        payload["manufacturing_data_list"][0]["parent_device"][
            "mfg_date"
        ] = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        log.info("Manufacturing payload %s :", payload)

        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            self.order.manufacturingdata = payload
            if test_run_data:
                test_run_data[self.deviceCategory]["manufacture"].append(payload)
            res = self.order.post_manufacturing_order(payload, self.deviceCategory)
            time.sleep(2)
            log.info(res)
            log.info(payload)
            if res["code"] == 201:
                return self.serialNumber, self.macAddress
            else:
                return False

        except Exception as e:
            log.error("Failed to create manufacturing order with S/N {}".format(e))
            return False

    def create_pos_order(self, part=None, check_emdm=None, return_payload=False):
        """
        Create point of sales order payload
        part is optional in this call, as few of existing test cases calls in that way
        :return: boolean
        """
        pos_order_data = self.payload.pos_order_data()
        pos_order_data["point_of_sales_data_list"][0]["obj_key"] = (
            "AOP_OKY_" + self.serialNumber
        )
        pos_order_data["point_of_sales_data_list"][0]["end_user_name"] = self.end_username
        pos_order_data["point_of_sales_data_list"][0][
            "invoice_date"
        ] = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        pos_order_data["point_of_sales_data_list"][0][
            "ship_date"
        ] = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        pos_order_data["point_of_sales_data_list"][0]["pos_id"] = (
            "AOP_ST_posID_" + self.serialNumber
        )
        pos_order_data["point_of_sales_data_list"][0]["serial_number"] = self.serialNumber
        """
        Added below 4 in JSON path - incase of Max Params
        """
        if part:
            pos_order_data["point_of_sales_data_list"][0]["part_number"] = part

        if check_emdm == "emdm_party":
            log.info(f"Choose {check_emdm} removing emdm party list")
            del pos_order_data["point_of_sales_data_list"][0]["emdm_party_list"]

        if check_emdm == "emdm_party_list":
            log.info(f"Choose {check_emdm} Removing emdm party")
            del pos_order_data["point_of_sales_data_list"][0]["emdm_party"]

        log.info("Payload pos: %s", pos_order_data)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            self.order.point_ofsales_order_data = pos_order_data
            pos_order = self.order.post_point_of_sales_order(
                pos_order_data, self.deviceCategory
            )
            time.sleep(2)

            if return_payload and pos_order["code"] == 201:
                return True, pos_order_data

            if pos_order["code"] == 201:
                return True
            else:
                return False
        except Exception as e:
            log.error("Failed to create create_pos_order order with S/N {}".format(e))
            return False

    def create_sds_order(self, part, check_emdm=None, return_payload=False):
        """
        Create sales direct order payload
        :param part: Device part number
        :return: boolean
        """
        log.info("Checking emdm type %s", check_emdm)
        sds_order_data = self.payload.sds_order_data()
        sds_order_data["sales_direct_shipment_data_list"][0]["obj_key"] = (
            "AOP_OBJKEY_ST" + self.serialNumber
        )
        sds_order_data["sales_direct_shipment_data_list"][0][
            "serial_number"
        ] = self.serialNumber
        sds_order_data["sales_direct_shipment_data_list"][0][
            "end_user_name"
        ] = self.end_username
        sds_order_data["sales_direct_shipment_data_list"][0][
            "ship_date"
        ] = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sds_order_data["sales_direct_shipment_data_list"][0][
            "purchase_order_date"
        ] = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sds_order_data["sales_direct_shipment_data_list"][0]["part_number"] = part

        if check_emdm == "emdm_party":
            log.info(f"Choose {check_emdm} removing emdm party list")
            del sds_order_data["sales_direct_shipment_data_list"][0]["emdm_party_list"]

        if check_emdm == "emdm_party_list":
            log.info(f"Choose {check_emdm} Removing emdm party")
            del sds_order_data["sales_direct_shipment_data_list"][0]["emdm_party"]

        log.info(
            "Received Category:"
            + self.deviceCategory
            + " SerialNumber:"
            + self.serialNumber
            + " MacAddress:"
            + self.macAddress
            + " PartNumber:"
            + str(part)
        )

        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            log.info("Payload %s", sds_order_data)
            log.info("Device Category %s", self.deviceCategory)
            self.order.sales_order_data = sds_order_data
            pos_direct_order = self.order.post_sds_order(
                sds_order_data, self.deviceCategory
            )
            time.sleep(2)
            if return_payload and pos_direct_order["code"] == 201:
                return True, sds_order_data
            if pos_direct_order["code"] == 201:
                return True
            else:
                return False
        except Exception as e:
            log.error("Failed to create create_sds_order order with S/N {}".format(e))
            return False

    def create_lic_order(self, part, return_payload=False, verified_alias=None):
        """
        Create license order payload and make license order call
        :param part: Device part number
        :return: subscription_key
        """
        lic_order_payload = self.payload.lic_order_data()
        lic_order_payload["obj_key"] = "AOP_OBJKEY_ST" + self.serialNumber
        lic_order_payload["reason"] = "Creation"
        lic_order_payload["quote"] = RandomGenUtils.random_string_of_chars(
            length=4, lowercase=False, uppercase=True, digits=True
        )
        lic_order_payload["entitlements"][0][
            "line_item"
        ] = RandomGenUtils.random_string_of_chars(
            length=3, lowercase=False, uppercase=True, digits=True
        )
        lic_order_payload["entitlements"][0]["licenses"][0][
            "device_serial_number"
        ] = self.serialNumber
        lic_order_payload["entitlements"][0]["licenses"][0][
            "subscription_key"
        ] = RandomGenUtils.random_string_of_chars(
            length=5, lowercase=False, uppercase=True, digits=True
        )
        lic_order_payload["entitlements"][0]["licenses"][0][
            "end_user_name"
        ] = self.end_username
        lic_order_payload["activate"]["sono"] = RandomGenUtils.random_string_of_chars(
            length=5, lowercase=False, uppercase=True, digits=True
        )
        lic_order_payload["activate"]["po"] = RandomGenUtils.random_string_of_chars(
            length=5, lowercase=False, uppercase=True, digits=True
        )
        lic_order_payload["activate"]["end_user_name"] = self.end_username
        lic_order_payload["entitlements"][0]["product"]["sku"] = part

        if verified_alias:
            log.info("Setting verified alias for cluster %s", verified_alias)
            lic_order_payload["activate"]["end_user_name"] = verified_alias
            lic_order_payload["entitlements"][0]["licenses"][0][
                "end_user_name"
            ] = verified_alias

        log.info(
            "Received Category:"
            + self.deviceCategory
            + " SerialNumber:"
            + self.serialNumber
            + " MacAddress:"
            + self.macAddress
            + " PartNumber:"
            + str(part)
        )
        log.info("license payload : %s", lic_order_payload)
        log.info("Device Category : %s", self.deviceCategory)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            self.order.post_lic_order(lic_order_payload, self.deviceCategory)
            self.order.lic_order_data = lic_order_payload
            time.sleep(2)
            get_lic_order_resp = self.order.get_lic_order(
                self.deviceCategory, lic_order_payload["obj_key"]
            )

            if (
                return_payload
                and get_lic_order_resp["entitlements"][0]["licenses"][0][
                    "subscription_key"
                ]
                is not None
            ):
                return (
                    get_lic_order_resp["entitlements"][0]["licenses"][0][
                        "subscription_key"
                    ],
                    get_lic_order_resp,
                )

            if (
                get_lic_order_resp["entitlements"][0]["licenses"][0]["subscription_key"]
                is not None
            ):
                return get_lic_order_resp["entitlements"][0]["licenses"][0][
                    "subscription_key"
                ]
            else:
                log.error("Failed to create create_lic_order order with S/N")
                return False
        except Exception as e:
            log.info("Failed to create create_lic_order order with S/N {}".format(e))
            return False

    def create_part_name(
        self, platform=None, part_category=None, include_child_part=False, baas=False
    ):
        """
        Create part name for device
        :return: part name
        """
        part_data_payload = self.payload.part_data()
        objkey = "AOP_OKY_" + self.serialNumber
        if platform:
            objkey = platform
        parent_prt = RandomGenUtils.random_string_of_chars(
            length=7, lowercase=False, uppercase=True
        )
        part_data_payload["part_data"][0]["parent_part"]["part_number"] = parent_prt
        part_data_payload["part_data"][0]["parent_part"][
            "part_category"
        ] = self.deviceCategory
        if part_category:
            part_data_payload["part_data"][0]["parent_part"][
                "part_category"
            ] = part_category
        part_data_payload["part_data"][0]["parent_part"]["part_model"] = "test_partModel"
        if baas:
            part_data_payload["part_data"][0]["parent_part"][
                "part_model"
            ] = "BAAS-STORAGE"
        part_data_payload["part_data"][0]["parent_part"]["address_use"] = False
        part_data_payload["part_data"][0]["parent_part"]["parent_part_number"] = "IGNORED"

        if include_child_part:
            log.info("Inside Child part name %s", include_child_part)
            part_data_payload["part_data"][0]["child_parts"][0][
                "part_number"
            ] = RandomGenUtils.random_string_of_chars(
                length=5, lowercase=False, uppercase=True
            )
            part_data_payload["part_data"][0]["child_parts"][0][
                "part_category"
            ] = self.deviceCategory
            if part_category:
                part_data_payload["part_data"][0]["child_parts"][0][
                    "part_category"
                ] = part_category

            part_data_payload["part_data"][0]["child_parts"][0]["address_use"] = False
            part_data_payload["part_data"][0]["child_parts"][0][
                "parent_part_number"
            ] = parent_prt
        else:
            del part_data_payload["part_data"][0]["child_parts"]

        try:
            log.info("Payload %s ", part_data_payload)
            log.info("Device Category %s ", self.deviceCategory)
            log.info("Platform cbject Key %s ", objkey)
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            create_part = self.order.create_part_name(
                part_data_payload, self.deviceCategory, objkey
            )
            if create_part["code"] == 201:
                log.info("Parent Part %s", parent_prt)
                return parent_prt
            else:
                return False
        except Exception as e:
            log.info("Failed to create_part_name order with S/N {}".format(e))
            return False

    def get_part_name(self, part, part_category=None):
        """
        Get Part response for device
        :param: part: part number
        :param: part_category: part category
        :return: tuple(Boolean, part response)
        """
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            if part_category is not None and part_category != self.deviceCategory:
                status_code, get_part_resp = self.order.get_part_name(
                    part_category, part, get_status_code=True
                )
            else:
                status_code, get_part_resp = self.order.get_part_name(
                    self.deviceCategory, part, get_status_code=True
                )
            log.debug("Get part response: %s", get_part_resp)
            if status_code == 200:
                return True, get_part_resp
        except Exception as e:
            log.error("Failed to get part number: %s", e)
        return False, None

    def get_platform(self):
        """
        Get platform for device
        :return: boolean
        """
        objkey = "AOP_OKY_" + self.serialNumber
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            status_code, get_platform_resp = self.order.get_platform(
                self.deviceCategory, objkey, get_status_code=True
            )
            log.info("get response: %s", get_platform_resp)
            if status_code == 200:
                return (True, get_platform_resp)
        except Exception as e:
            log.info("Failed to get platform".format(e))
            return (False, None)

    def create_platform(self, mode=None, name=None):
        """
        Create platform for device
        :return: boolean
        """
        platform_data_payload = self.payload.platform_data()
        if not name:
            platform_data_payload["platform_list"][0]["name"] = (
                "AOP_OKY_" + self.serialNumber
            )
        else:
            platform_data_payload["platform_list"][0]["name"] = name
        if not mode:
            payload_mode = (
                "NETWORK"
                if self.device_type == "SD_WAN_GW" or self.device_type == "SENSOR"
                else self.device_type
            )
            platform_data_payload["platform_list"][0]["mode"] = payload_mode
        else:
            platform_data_payload["platform_list"][0]["mode"] = mode
        platform_data_payload["platform_list"][0]["xref"] = "aop_network_baseOS_1"
        platform_data_payload["platform_list"][0][
            "description"
        ] = "aop_st_platform_add_compute"

        """
        Regex validation to check xref contains only alphanumeric, underscore
        """
        xref_regex = re.compile(r"^\w+$")
        if xref_regex.match(platform_data_payload["platform_list"][0]["xref"]):
            try:
                self.order = ActivateOrder(
                    self.app_api_host,
                    self.sso_host,
                    self.aop_client_id,
                    self.aop_client_secret,
                )
                create_platform_resp = self.order.create_platform(platform_data_payload)
                if create_platform_resp["code"] == 201:
                    return True
            except Exception as e:
                log.info("Failed to create create_platform order with S/N {}".format(e))
                return False
        else:
            log.info(
                "{} Error: Invalid character in xref field".format(
                    platform_data_payload["platform_list"][0]["xref"]
                )
            )

    def update_platform(self, update_type=""):
        """
        Update platform for device
        :return: boolean, put_platform_resp
        """
        objkey = "AOP_OKY_" + self.serialNumber
        rand_string_details = {
            "length": 3,
            "lowercase": False,
            "uppercase": True,
            "digits": True,
        }
        platform_data_payload = self.payload.platform_data()
        platform_data_payload["platform_list"][0]["name"] = objkey
        platform_data_payload["platform_list"][0]["mode"] = self.deviceCategory
        platform_data_payload["platform_list"][0]["xref"] = "aop_network_baseOS_1"
        platform_data_payload["platform_list"][0][
            "description"
        ] = "aop_st_platform_add_compute"

        if "name" in update_type:
            platform_data_payload["platform_list"][0].update(
                {
                    "name": objkey
                    + RandomGenUtils.random_string_of_chars(**rand_string_details)
                }
            )

        if "mode" in update_type:
            platform_data_payload["platform_list"][0].update({"mode": "COMPUTE"})

        if "xref" in update_type:
            platform_data_payload["platform_list"][0].update(
                {
                    "xref": "aop_network_baseOS_1"
                    + RandomGenUtils.random_string_of_chars(**rand_string_details)
                }
            )

        if "code" in update_type:
            platform_data_payload["platform_list"][0].update(
                {
                    "code": RandomGenUtils.random_string_of_chars(
                        length=7, lowercase=False, uppercase=False, digits=True
                    )
                }
            )

        if "name_and_mode" in update_type:
            platform_data_payload["platform_list"][0].update(
                {
                    "name": objkey
                    + RandomGenUtils.random_string_of_chars(**rand_string_details),
                    "mode": "COMPUTE",
                }
            )
        if "description_null" in update_type:
            platform_data_payload["platform_list"][0].update({"description": ""})

        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            putpayload = platform_data_payload["platform_list"][0]
            log.info("put payload: %s", putpayload)
            status_code, put_platform_resp = self.order.update_platform(
                putpayload, self.deviceCategory, objkey, get_status_code=True
            )
            log.info("put response: %s", put_platform_resp)
            if status_code == 200:
                return (True, put_platform_resp)
        except Exception as e:
            log.info("Failed to update platform details".format(e))
            return (False, None)

    def update_lic_order(self, payload, obj_key, dev_type=None):
        """
        Update the license order. Payload is required for the PUT request
        :param payload to update license
        :param obj_key: object key
        :return: the get response and boolean
        """
        if not payload:
            log.error(
                "Payload cannot be empty. Payload is required for the PUT/update request"
            )
            return False, None

        if obj_key is None:
            obj_key = "AOP_OBJKEY_ST" + self.serialNumber
        if dev_type:
            self.deviceCategory = dev_type
        log.info("Getting the object key %s", obj_key)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            self.order.lic_order_data = payload
            update_license = self.order.update_license_order(
                self.deviceCategory, obj_key, payload
            )
            if update_license["code"] == 201:
                get_lic_order_resp = self.order.get_lic_order(
                    self.deviceCategory, obj_key
                )
                return True, get_lic_order_resp
            else:
                log.error("Failed to update license")
                return False, None
        except Exception as e:
            log.info("Failed to update license {}".format(e))
            return False

    def update_manufacturing(self, dev_type, payload, child=None):
        """
        Update the manufacturing order. Payload is required for the PUT request
        :param payload to update manufacturing
        :param obj_key:
        :return: the get response and boolean
        """
        try:
            if not child:
                objkey = payload["obj_key"]
                update_mfr = self.order.update_mfr(payload, dev_type, objkey)
            else:
                objkey = child
                update_mfr = self.order.update_new_child(payload, dev_type, objkey)
                if (
                    update_mfr["parent_device"]["status"] == "MANUFACTURED"
                    and update_mfr["parent_device"]["status"] == "MANUFACTURED"
                ):
                    return True, update_mfr
            if update_mfr["status"] == "MANUFACTURED":
                return True, update_mfr
            else:
                log.error("Failed to update manufacturing order")
                return False, None
        except Exception as e:
            log.info("Failed to update license {}".format(e))
            return False

    def get_direct_sales_order(self, obj_key):
        """
        Get the direct sales order
        :param obj_key: object key
        :return: boolean, direct sales response
        """
        log.info("Fetching direct sales orders Get Request")
        if obj_key is None:
            obj_key = "AOP_OBJKEY_ST" + self.serialNumber
        log.info("Getting the object key %s", obj_key)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            status_code, get_sds_response = self.order.get_sales_direct_order(
                self.deviceCategory, obj_key, get_status_code=True
            )
            if status_code == 200:
                return True, get_sds_response
        except Exception as e:
            log.info("Failed to get direct sales order {}".format(e))

    def get_lic_order(self, obj_key):
        """
        Get the license
        :param obj_key: object key
        :return: boolean, license response
        """
        if obj_key is None:
            obj_key = "AOP_OBJKEY_ST" + self.serialNumber
        log.info("Device Category : %s", self.deviceCategory)
        log.info("Getting the object key %s", obj_key)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            status_code, get_lic_order_resp = self.order.get_lic_order(
                self.deviceCategory, obj_key, get_status_code=True
            )
            if status_code == 200:
                log.info("get license response: %s", get_lic_order_resp)
                return True, get_lic_order_resp
        except Exception as e:
            log.info("Failed to create create_lic_order order with S/N {}".format(e))
            return False, None

    def get_pos_order(self, obj_key):
        """
        Get the point of sales order
        :param obj_key: object key
        :return: boolean, pos sales response
        """
        log.info("Fetching POS sales orders Get Request")
        if obj_key is None:
            obj_key = "AOP_OKY_" + self.serialNumber
        log.info("Getting the object key %s", obj_key)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            status_code, get_pos_response = self.order.get_point_of_sales_order(
                self.deviceCategory, obj_key, get_status_code=True
            )
            if status_code == 200:
                return True, get_pos_response
        except Exception as e:
            log.info("Failed to get point of sales order {}".format(e))
            return False

    def update_pos_order(self, payload, obj_key, dev_type=None):
        """
        Update the point of sales order. Payload is required for the PUT request
        :param obj_key: object key
        :param payload: payload to update point of sales order
        :return: boolean, pos response
        """
        if not payload:
            log.error(
                "Payload cannot be empty. Payload is required for the PUT/update request"
            )
            return False, None

        log.info("Updating the POS order")
        if not dev_type:
            dev_type = self.deviceCategory
        if obj_key is None:
            obj_key = "AOP_OKY_" + self.serialNumber
        log.info("Getting the object key %s", obj_key)
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            status_code, update_pos_response = self.order.update_point_of_sales_order(
                payload, self.deviceCategory, obj_key, get_status_code=True
            )
            if status_code == 200:
                (
                    get_pos_status_code,
                    get_pos_response,
                ) = self.order.get_point_of_sales_order(
                    self.deviceCategory, obj_key, get_status_code=True
                )
                return (get_pos_status_code, get_pos_response)
            else:
                log.error("Failed to update point of sales order")
                return (False, None)
        except Exception as e:
            log.info("Failed to update point of sales order {}".format(e))
            return False

    def update_Sds_order(self, payload, obj_key, dev_type=None):
        """
        Update the sales direct order. Payload is required for the PUT request
        :param obj_key: object key
        :param devicetype
        :param payload: payload to update point of sales order
        :return: boolean, pos response
        """
        if not payload:
            log.error(
                "Payload cannot be empty. Payload is required for the PUT/update request"
            )
            return False, None
        log.info("Updating the SDS order")
        if obj_key is None:
            obj_key = "AOP_OKY_" + self.serialNumber
        log.info("Getting the object key %s", obj_key)
        if not dev_type:
            dev_type = self.deviceCategory
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            status_code, res = self.order.update_sales_direct_order(
                payload, dev_type, obj_key, get_status_code=True
            )
            if status_code == 200:
                get_sds_status_code, get_sds_response = self.order.get_sales_direct_order(
                    dev_type, obj_key, get_status_code=True
                )
                return (True, res)
            else:
                log.error("Failed to update point of sales order")
                return (False, None)
        except Exception as e:
            log.info("Failed to update point of sales order {}".format(e))
            return False

    def create_oaas(
        self,
        part,
        part_category,
        MinParams=False,
        return_payload=False,
        pce_part_number=None,
        get_device_report=False,
        enable_extra_attributes=False,
    ):
        """
        Create Oaas using the template
        :param part: Device part number (child part number in case of PCE)
        :param part_category: Device Part category (child part category in case of PCE)
        :param pce_part_number: Device Part number for PCE device (parent)
        :param return_payload: If True, result will be extended by report_category
        :param get_device_report: only the device report
        :param enable_extra_attributes: to set extra parameters to child object (dev_config_modify)
        :return: Device config report
        """
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            oaas_template = OaasConstants()
            oaas_payload = RandomGenUtils.dev_config_modify(
                part,
                part_category,
                oaas_template.dev_config_template,
                extra_attribute=enable_extra_attributes,
            )
            if pce_part_number:
                oaas_payload["part_category"] = "PCE"
                oaas_payload["part_number"] = pce_part_number
            res = self.order.create_new_device_configuration(oaas_payload)
            report = self.order.get_oaas_report(res["report_location"])
            if get_device_report:
                return report
            for i in range(5):
                if return_payload and report["report_status"] == "COMPLETED":
                    return (
                        report["report_location"].split("/")[-1].split("__")[0],
                        report["report_category"],
                    )
                if report["report_status"] == "COMPLETED":
                    return report["report_location"].split("/")[-1].split("__")[0]
                else:
                    time.sleep(5)
                    report = self.order.get_oaas_report(res["report_location"])
            return None

        except Exception as e:
            log.error("Failed to create Oaas {}".format(e))
            return None

    def get_oaas_bykey(self, objkey):
        """
        Get Oaas by object key
        :param objkey: Object key
        :return: Device config
        """
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            res = self.order.get_oaas_by_objkey(objkey)
            return res

        except Exception as e:
            log.error("Failed to get Oaas {}".format(e))
            return None

    def create_multiple_platform(self, mode_list, same_name=False):
        """
        Creates multiple platform
        :param mode_list: List of modes to be added
        :param same_name: Flag for same_name, If True then generates a random name and appends it to payload
        :return: tuple(Boolean, create platform response)
        """
        platform_data_payload = self.payload.platform_data()
        platform_list = []
        if same_name == True:
            name = f"AOP_ST_OBJKEY_MULTIPLE_{RandomGenUtils.random_string_of_chars(length=7, lowercase=False, uppercase=True)}"
            for mode in mode_list:
                platform = {
                    "name": name,
                    "mode": mode,
                    "xref": "aop_network_baseOS",
                    "description": "aop_st_platform_add_compute",
                }
                platform_list.append(platform)
        else:
            for mode in mode_list:
                platform = {
                    "name": f"AOP_ST_OBJKEY_MULTIPLE_{RandomGenUtils.random_string_of_chars(length=7, lowercase=False, uppercase=True)}",
                    "mode": mode,
                    "xref": "aop_network_baseOS",
                    "description": "aop_st_platform_add_compute",
                }
                platform_list.append(platform)

        platform_data_payload["platform_list"] = platform_list
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            create_platform_resp = self.order.create_platform(platform_data_payload)
            if create_platform_resp["code"] == 201 or create_platform_resp["code"] == 202:
                log.debug(create_platform_resp)
                return True, create_platform_resp
        except Exception as e:
            log.info("Failed to create create_platform order with S/N {}".format(e))
            return False, None

    def get_part_by_number(self, part):
        """
        :param part: Part number
        :return: A tuple containing the status code and part response
        :raises: Exception: Error in getting part number
        """
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            get_part_status_code, get_part_response = self.order.get_all_matching_part(
                number=part, get_status_code=True
            )
            if get_part_status_code == 200:
                log.debug("Get the part response: %s", get_part_response)
                return get_part_status_code, get_part_response
            else:
                log.error("Failed to the part number response")
                return get_part_status_code, get_part_response
        except Exception as e:
            log.error("Failed to get part number response".format(e))
            return False, None

    def update_part_number(self, payload):
        """
        Updates the part number with a new random value in the given payload

        :param payload: Part payload
        :return: A tuple containing the status code and the response after updating the part number.
        :raises: Exception: Error to update the part number
        """
        if not payload:
            log.error(
                "Payload is None or empty. A valid payload is required for the update request."
            )
            return False, None

        part_number = payload["part_number"]
        payload["part_number"] = RandomGenUtils.random_string_of_chars(
            length=7, lowercase=False, uppercase=True
        )
        part_category = payload["part_category"]
        try:
            self.order = ActivateOrder(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            update_part_status_code, update_part_response = self.order.update_part_number(
                part_category, part_number, payload, get_status_code=True
            )
            if update_part_status_code == 200:
                log.debug("Update part is successful: %s", update_part_response)
                return update_part_status_code, update_part_response
            else:
                log.error("Failed to update the part number")
                return update_part_status_code, update_part_response
        except Exception as e:
            log.error("Failed to update the part number".format(e))
            return False, None
