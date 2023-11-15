"""
Payloads templates for Activate Order Processor App Api
"""
import datetime
import logging
from logging import DEBUG

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class AopInputPayload:
    pod_namespace: str = ""
    log_level = DEBUG

    def get_verified_alias_by_cluster(self, cluster):
        if "mira" in cluster:
            return "mira_verified_alias_ft1"
        elif "polaris" in cluster:
            return "polaris_verified_alias_ft1"
        elif "pavo" in cluster:
            return "pavo_verified_alias_ft1"
        elif "triton" in cluster:
            return "triton_verified_alias_ft1"
        else:
            log.error("Provide a valid cluster name")
            return False

    def mfr_payload_data(self):
        log.info("loading")
        """
        parent_serial_number is not required, nor present in documentation
        device_type is deprecated field.
        """
        mfr_payload = {
            "manufacturing_data_list": [
                {
                    "parent_device": {
                        "obj_key": "obj_key",
                        "serial_number": "serial_number",
                        "part_number": "part_number",
                        "part_category": "part_category",
                        "eth_mac": "eth_mac",
                        "mfg_date": "mfg_date",
                        "device_type": "device_type",
                    }
                }
            ]
        }
        return mfr_payload

    def pos_order_data(self):
        pos_order_payload = {
            "point_of_sales_data_list": [
                {
                    "obj_key": "AOP_OKY_",
                    "pos_id": "AOP_ST_posID_",
                    "invoice_date": "2021-02-25 01:54:52",
                    "ship_date": "2021-02-25 01:54:52",
                    "reseller_name": "AOP_ST_reseller",
                    "end_user_name": "AOP_ST_end_user",
                    "part_number": "PLACEHOLDER",
                    "quantity": 1,
                    "ext_cost": 10000,
                    "invoice_no": "AOP_ST_invoice_",
                    "order_no": "AOP_ST_order_",
                    "line_no": 1,
                    "line_type": "IN",
                    "distributor_po_no": "AOP_ST_distributor_po_no_",
                    "serial_number": "AOPST",
                    "us_zip": "95001",
                    "source": "AOP_ST_source",
                    "emdm_party": {
                        "id": "string",
                        "function": "AG",
                        "country_id": "string",
                        "global_id": "string",
                    },
                    "emdm_party_list": [
                        {
                            "id": "string",
                            "function": "AG",
                            "country_id": "string",
                            "global_id": "string",
                        }
                    ],
                }
            ]
        }
        return pos_order_payload

    def sds_order_data(self):
        sds_order_payload = {
            "sales_direct_shipment_data_list": [
                {
                    "obj_key": "obj_key",
                    "sono": "sono",
                    "part_number": "part_number",
                    "part_description": "PLACEHOLDER",
                    "serial_number": "serial_number",
                    "sold_to": "AOP_ST_Customer",
                    "sold_to_name": "AOP_ST_Customer_sold_to_name",
                    "sold_to_email": "AOP_ST_Customer@email.com",
                    "ship_to": "AOP_ST_Customer_ship_to",
                    "ship_to_name": "AOP_ST_Customer_ship_to_name",
                    "ship_to_email": "AOP_ST_Customer_ship@email.com",
                    "end_user": "AOP_ST_Customer",
                    "end_user_name": "AOP_ST_end_user",
                    "end_user_email": "AOP_ST_end_user@email.com",
                    "reseller": "AOP_ST_reseller",
                    "reseller_name": "AOP_ST_reseller_name",
                    "reseller_email": "AOP_ST_reseller@email.com",
                    "purchase_order_date": "2021-02-25 01:54:52",
                    "order_class": "NON-BRIM",
                    "customer_po": "PLACEHOLDERFFZAH",
                    "ship_date": "2021-02-25 01:54:52",
                    "emdm_party": {
                        "id": "string",
                        "function": "AG",
                        "country_id": "string",
                        "global_id": "string",
                    },
                    "emdm_party_list": [
                        {
                            "id": "string",
                            "function": "AG",
                            "country_id": "string",
                            "global_id": "string",
                        }
                    ],
                }
            ]
        }
        return sds_order_payload

    def lic_order_data(self):
        lic_order_payload = {
            "obj_key": "AOP_OKY_",
            "reason": "Creation",
            "quote": "AOPSTQ",
            "entitlements": [
                {
                    "line_item": "AOPSTLI",
                    "licenses": [
                        {
                            "subscription_key": "AOPSTSUBKEY",
                            "device_serial_number": "PLACEHOLDER",
                            "qty": "999",
                            "available_qty": "10.50",
                            "capacity": "2000GB",
                            "appointments": {
                                "term": "10DAYS",
                                "subscription_start": "2021-02-23 20:48:30",
                                "subscription_end": "2024-02-23 20:48:30",
                                "delayed_activation": "2021-03-23 20:48:30",
                            },
                        }
                    ],
                    "product": {
                        "sku": "AOP_ST_PART_NO",
                        "description": "AOP_ST_SKU_DESCRIPTION_STRING --------------------------------------",
                    },
                }
            ],
            "activate": {
                "sono": "AOPSTSONO",
                "sold_to": "AOP_ST_Customer",
                "sold_to_name": "AOP_ST_Customer_sold_to_name",
                "sold_to_email": "AOP_ST_Customer@email.com",
                "ship_to": "AOP_ST_Customer_ship_to",
                "ship_to_name": "AOP_ST_Customer_ship_to_name",
                "ship_to_email": "AOP_ST_Customer_ship@email.com",
                "end_user": "AOP_ST_Customer",
                "end_user_name": "AOP_ST_end_user",
                "end_user_email": "AOP_ST_end_user@email.com",
                "reseller": "AOP_ST_reseller",
                "reseller_name": "AOP_ST_reseller_name",
                "reseller_email": "AOP_ST_reseller@email.com",
                "po": "AOP_ST_PO_",
                "order_class": "NON-BRIM",
                "party": {
                    "id": "AOP_STPID",
                    "country_id": "AOP_STCID",
                    "global_id": "AOP_STGID",
                },
            },
        }
        return lic_order_payload

    def platform_data(self):
        platform_data_payload = {
            "platform_list": [
                {
                    "name": "platform_name",
                    "mode": "Device_type",
                    "xref": "aop_st_xref",
                    "description": "aop_st_platform_desc",
                }
            ]
        }
        return platform_data_payload

    def part_data(self):
        part_data_payload = {
            "part_data": [
                {
                    "parent_part": {
                        "part_number": "PRT_Part_Num",
                        "part_category": "Dev_Category",
                        "part_model": "test_partModel",
                        "description": "testPartDescription",
                        "address_use": False,
                        "parent_part_number": "IGNORED",
                    },
                    "child_parts": [
                        {
                            "part_number": "CHLD_Part_Num",
                            "part_category": "Dev_Category",
                            "part_model": "test_child_partModel",
                            "description": "testChildPartDescription",
                            "address_use": False,
                            "parent_part_number": "PRT_Part_Num",
                        }
                    ],
                }
            ]
        }
        return part_data_payload


class AOPDeviceConstants:
    def __init__(self):
        log.info("Initialize AOPDeviceConstants")

    @staticmethod
    def new_mfr_device_constants():
        rand_string_details = {
            "length": 5,
            "lowercase": False,
            "uppercase": True,
            "digits": True,
        }
        new_device_constants = {
            "IAP_serial": "STIAP"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "PCE_serial": "STPCE"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "SD_WAN_GW_serial": "SD_WAN"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "SENSOR_serial": "SENSOR"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "SWITCH_serial": "STSWI"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "GATEWAY_serial": "STGWA"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "CONTROLLER_serial": "STCNTRL"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "STORAGE_serial": "ST_"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "DHCI_STORAGE_serial": "STDHCI_"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "COMPUTE_serial": "COM_"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "NETWORK_serial": "NET_"
            + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "IAP_mac": RandomGenUtils.generate_random_MAC_address(),
            "PCE_mac": RandomGenUtils.generate_random_MAC_address(),
            "SD_WAN_GW_mac": RandomGenUtils.generate_random_MAC_address(),
            "SENSOR_mac": RandomGenUtils.generate_random_MAC_address(),
            "SWITCH_mac": RandomGenUtils.generate_random_MAC_address(),
            "GATEWAY_mac": RandomGenUtils.generate_random_MAC_address(),
            "CONTROLLER_mac": RandomGenUtils.generate_random_MAC_address(),
            "STORAGE_mac": RandomGenUtils.generate_random_MAC_address(),
            "DHCI_STORAGE_mac": RandomGenUtils.generate_random_MAC_address(),
            "COMPUTE_mac": RandomGenUtils.generate_random_MAC_address(),
            "NETWORK_mac": RandomGenUtils.generate_random_MAC_address(),
            "MAC_REGEX": "^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$",
            "SERIAL_NUMBER_LENGTH": 20,
            "device_category_nw": "NETWORK",
            "device_category_compute": "COMPUTE",
            "device_category_storage": "STORAGE",
            "device_category_pce": "PCE",
            "device_category_IAP": "IAP",
            "device_category_SWITCH": "SWITCH",
            "device_category_GATEWAY": "GATEWAY",
            "DEFAULT_PART_MAP": {
                "SWITCH": "JL255A",
                "IAP": "JW242AR",
                "GATEWAY": "7005-RW",
                "CONTROLLER": "3200-8-US",
                "SD_WAN_GW": "RGCTQUK",
                "SENSOR": "RGCTSENS",
            },
        }
        return new_device_constants

    @staticmethod
    def generate_devices_details():
        """Generate device-details dictionary with pre-populated general properties
            and empty lists of serial numbers and MAC-addresses.

        :return: dictionary with generated details of devices and empty lists of serial numbers and MAC-addresses.
        """
        devices_constants = {
            "IAP_serial": [],
            "SWITCH_serial": [],
            "GATEWAY_serial": [],
            "CONTROLLER_serial": [],
            "STORAGE_serial": [],
            "DHCI_STORAGE_serial": [],
            "COMPUTE_serial": [],
            "NETWORK_serial": [],
            "IAP_mac": [],
            "SWITCH_mac": [],
            "GATEWAY_mac": [],
            "CONTROLLER_mac": [],
            "STORAGE_mac": [],
            "DHCI_STORAGE_mac": [],
            "COMPUTE_mac": [],
            "NETWORK_mac": [],
            "MAC_REGEX": "^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$",
            "SERIAL_NUMBER_LENGTH": 20,
            "device_category_nw": "NETWORK",
            "device_category_compute": "COMPUTE",
            "device_category_storage": "STORAGE",
            "device_category_IAP": "IAP",
            "device_category_SWITCH": "SWITCH",
            "device_category_GATEWAY": "GATEWAY",
            "DEFAULT_PART_MAP": {
                "SWITCH": "JL255A",
                "IAP": "JW242AR",
                "GATEWAY": "7005-RW",
                "CONTROLLER": "3200-8-US",
            },
        }
        return devices_constants

    @staticmethod
    def add_device_of_type(devices_constants: dict, device_type: str):
        """Generate serial and MAC-address for new device of specified type and add them to "devices_constants".

        :param devices_constants: dictionary with details of devices in format, generated
            by 'generate_devices_details' method above.
        :param device_type: type of new device to be added to 'current_devices'. Allowed values: "IAP", "SWITCH",
            "GATEWAY", "STORAGE", "COMPUTE", "NETWORK".
        """
        serial_prefixes = {
            "IAP": "STIAP",
            "SWITCH": "STSWI",
            "GATEWAY": "STGWA",
            "CONTROLLER": "STCNTRL",
            "STORAGE": "ST_",
            "DHCI_STORAGE": "STDHCI_",
            "COMPUTE": "COM_",
            "NETWORK": "NET_",
        }
        device_type = device_type.upper()
        if device_type not in serial_prefixes.keys():
            raise ValueError(
                f"Invalid/unsupported type of device specified: '{device_type}'."
            )
        rand_string_details = {
            "length": 5,
            "lowercase": False,
            "uppercase": True,
            "digits": True,
        }
        sn_prefix = serial_prefixes[device_type]
        devices_constants[f"{device_type}_serial"].append(
            f"{sn_prefix}{RandomGenUtils.random_string_of_chars(**rand_string_details)}"
        )
        devices_constants[f"{device_type}_mac"].append(
            RandomGenUtils.generate_random_MAC_address()
        )

    def create_manufacture_payload(
        self, object_key, part_number, part_category, device_type, serial_number=None
    ):
        """
        Create manufacturing payloads with varying parameters and make manufacture call
        :param object_key: Object key or list of object keys
        :param part_number: Part number or list of part numbers
        :param part_category: Part category or list of part categories
        :param device_type: Device type or list of device types
        :param serial_number: Serial number or list of serial numbers (optional)
        :return: manufacture_payload dict
        """
        # If the input arguments are not lists, convert them to single-item lists
        if not isinstance(object_key, list):
            object_key = [object_key]
            part_number = [part_number]
            part_category = [part_category]
            device_type = [device_type]

        # Initialize an empty list to store manufacturing data
        manufacturing_data_list = []

        # Iterate through the input lists and create manufacturing data for each item
        for i, obj_key in enumerate(object_key):
            # Create a dictionary for the parent device's information
            parent_device = {
                "obj_key": obj_key,
                "serial_number": serial_number[i]
                if serial_number
                else obj_key.replace("AOP_OKY_", ""),
                "part_number": part_number[i],
                "part_category": part_category[i],
                "device_type": device_type[i],
                "eth_mac": RandomGenUtils.generate_random_MAC_address(),
                "mfg_date": datetime.datetime.strftime(
                    datetime.datetime.today(), "%Y-%m-%d %H:%M:%S"
                ),
            }
            # Add the parent device information to the manufacturing data list
            manufacturing_data_list.append({"parent_device": parent_device})

        # Create the final payload dictionary containing the manufacturing data list
        manufacture_payload = {"manufacturing_data_list": manufacturing_data_list}
        log.debug("Manufacture payload : %s", manufacture_payload)
        return manufacture_payload


class OaasConstants:
    def __init__(self):
        log.info("Initialize OaasConstants")
        self.dev_config_template = {
            "obj_key": "ROOTYSBNH33483",
            "serial_number": "ROOTYSBNH33483",
            "part_number": "STRARCUS101",
            "part_category": "STORAGE",
            "eth_mac": "52:35:83:84:D3:43",
            "boot_version": "boot.1.2.3.4",
            "fw_version": "fw.1.2.3.4",
            "mfg_date": "2020-10-10 10:10:10",
            "platform_category": "PROLIANT",
            "child_devices": [
                {
                    "obj_key": "ROOTL2OQMFA53797",
                    "serial_number": "ROOTL2OQMFA53797",
                    "part_number": "STRARCUS101",
                    "part_category": "STORAGE",
                    "eth_mac": "40:D1:42:A6:4E:B6",
                    "boot_version": "boot.1.2.3.4",
                    "fw_version": "fw.1.2.3.4",
                    "mfg_date": "2020-10-10 10:10:10",
                    "platform_category": "PROLIANT",
                    "child_devices": [
                        {
                            "obj_key": "ROOTL3SOHFN84196",
                            "serial_number": "ROOTL3SOHFN84196",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "CF:AF:AE:44:D4:EE",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3KDIHX59929",
                            "serial_number": "ROOTL3KDIHX59929",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "24:09:32:84:F8:10",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3FODVR97178",
                            "serial_number": "ROOTL3FODVR97178",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "E6:98:56:92:B2:9F",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3ERJWX32523",
                            "serial_number": "ROOTL3ERJWX32523",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "A4:57:60:12:28:DD",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                    ],
                },
                {
                    "obj_key": "ROOTL2SFPWO25111",
                    "serial_number": "ROOTL2SFPWO25111",
                    "part_number": "STRARCUS101",
                    "part_category": "STORAGE",
                    "eth_mac": "72:98:CE:F9:0F:62",
                    "boot_version": "boot.1.2.3.4",
                    "fw_version": "fw.1.2.3.4",
                    "mfg_date": "2020-10-10 10:10:10",
                    "platform_category": "PROLIANT",
                    "child_devices": [
                        {
                            "obj_key": "ROOTL3HYVCO55578",
                            "serial_number": "ROOTL3HYVCO55578",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "2F:B2:26:CD:D4:4C",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3PQSBD38601",
                            "serial_number": "ROOTL3PQSBD38601",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "C1:88:15:32:B1:13",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3OLOEY07992",
                            "serial_number": "ROOTL3OLOEY07992",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "AC:D8:45:AD:33:5D",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3HDUOD87452",
                            "serial_number": "ROOTL3HDUOD87452",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "D2:9C:E3:67:3A:89",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                    ],
                },
                {
                    "obj_key": "ROOTL2NFSLU52781",
                    "serial_number": "ROOTL2NFSLU52781",
                    "part_number": "STRARCUS101",
                    "part_category": "STORAGE",
                    "eth_mac": "3A:B6:A2:D1:BF:AF",
                    "boot_version": "boot.1.2.3.4",
                    "fw_version": "fw.1.2.3.4",
                    "mfg_date": "2020-10-10 10:10:10",
                    "platform_category": "PROLIANT",
                    "child_devices": [
                        {
                            "obj_key": "ROOTL3PWNTV86197",
                            "serial_number": "ROOTL3PWNTV86197",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "BF:55:14:37:30:78",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3WXRET06969",
                            "serial_number": "ROOTL3WXRET06969",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "E0:31:89:ED:86:4F",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3JTKMW83713",
                            "serial_number": "ROOTL3JTKMW83713",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "17:06:7B:7B:01:3A",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3ULQRD05844",
                            "serial_number": "ROOTL3ULQRD05844",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "DF:BB:DB:95:B2:FC",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                    ],
                },
                {
                    "obj_key": "ROOTL2SZZSA57233",
                    "serial_number": "ROOTL2SZZSA57233",
                    "part_number": "STRARCUS101",
                    "part_category": "STORAGE",
                    "eth_mac": "29:81:6D:CD:2F:02",
                    "boot_version": "boot.1.2.3.4",
                    "fw_version": "fw.1.2.3.4",
                    "mfg_date": "2020-10-10 10:10:10",
                    "platform_category": "PROLIANT",
                    "child_devices": [
                        {
                            "obj_key": "ROOTL3LOCEC79334",
                            "serial_number": "ROOTL3LOCEC79334",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "74:D4:1F:97:11:69",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3ZYSZK49643",
                            "serial_number": "ROOTL3ZYSZK49643",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "8D:2D:28:46:F6:69",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3EUMPS72936",
                            "serial_number": "ROOTL3EUMPS72936",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "C5:3C:54:38:BF:1B",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                        {
                            "obj_key": "ROOTL3CYRTD71219",
                            "serial_number": "ROOTL3CYRTD71219",
                            "part_number": "STRARCUS101",
                            "part_category": "STORAGE",
                            "eth_mac": "07:5D:E7:91:DE:7C",
                            "boot_version": "boot.1.2.3.4",
                            "fw_version": "fw.1.2.3.4",
                            "mfg_date": "2020-10-10 10:10:10",
                            "platform_category": "PROLIANT",
                        },
                    ],
                },
            ],
        }

    def trim_child_devices(self, payload, max_levels=2):
        """
        Recursively trims the levels of child devices in the payload dictionary.

        This function removes or trims the nested "child_devices" dictionaries within the payload
        dictionary based on the specified maximum levels.

        :param: payload (dict): The payload dictionary containing device information.
        :param: max_levels (int, optional): The maximum levels of child devices to retain. Defaults to 2.

        :return: dict: The modified payload dictionary with child devices trimmed.

        :usage:
        Suppose you have a payload dictionary with nested child devices as follows:
        payload = {
            "device_id": "parent_device",
            "child_devices": {
                "child1": {
                    "device_id": "child1_device",
                    "child_devices": {
                        "child1_1": {
                            "device_id": "child1_1_device"
                        }
                    }
                }
            }
        }
        Example 1: max_levels=0
        # Output: {}

        Example 2: max_levels=1
        # Output: {
        #     "device_id": "parent_device"
        # }
        # Explanation: With max_levels=1, only parent is retained in the payload.

        Example 3: max_levels=2
        # Output: {
        #     "device_id": "parent_device",
        #     "child_devices": {
        #         "child1": {
        #             "device_id": "child1_device"
        #         }
        #     }
        # }
        # Explanation: With max_levels=2, child devices up to two levels deep are retained in the payload.

        Similarly, it can be followed till level 'n'
        """
        log.debug(f"Max levels: {max_levels}")
        if max_levels == 0:
            log.debug(
                f"Reached max_levels (0) : {max_levels}. Returning an empty dictionary."
            )
            return {}  # Return an empty dictionary if max_levels is 0.
        if max_levels == 1:
            # If max_levels is 1, remove the entire "child_devices" key from the payload.
            log.debug(f"Removing child_devices at max_levels {max_levels}.")
            payload.pop("child_devices", None)
        else:
            if "child_devices" in payload:
                children = payload["child_devices"]
                new_children = []
                for child in children:
                    # Recursively trim child devices and reduce max_levels by 1.
                    log.debug(
                        f"Recursing into child device at current_level {max_levels}."
                    )
                    new_child = self.trim_child_devices(child, max_levels - 1)
                    new_children.append(new_child)
                payload[
                    "child_devices"
                ] = new_children  # Update child devices after trimming.
        return payload

    def assign_part_info_recursive(self, payload, category, part_number, level):
        """
        Recursively assigns part information to the payload and its child devices.

        This method assigns part category and part number information to the given payload
        dictionary and its child devices. The assignment is based on the provided category,
        part number, and level.

        :param: payload: The payload dictionary to assign part information to.
        :param: category: The part category to be assigned.
        :param: part_number: The part number to be assigned.
        :param: level: The level of the current payload in the device hierarchy.

        """
        log.debug(
            f"Assigning part info to payload: category={category}, part_number={part_number}, level={level}"
        )
        payload["part_category"] = category
        payload["part_number"] = part_number

        if "child_devices" in payload:
            for child_device in payload["child_devices"]:
                self.assign_part_info_recursive(
                    child_device, category, part_number, level + 1
                )

    def assign_part_info_multiple_levels(
        self,
        payload,
        root_category,
        root_part_number,
        child_category,
        child_part_number,
        inner_child_category=None,
        inner_child_part_number=None,
    ):
        """
        Assigns part information at different levels within the payload.

        This method assigns part information at various levels within the payload dictionary
        hierarchy. It assigns root-level, child-level, and potentially inner child-level
        part information based on the provided parameters.

        :param: payload: The payload dictionary to assign part information to.
        :param: root_category: The root part category to be assigned.
        :param: root_part_number: The root part number to be assigned.
        :param: child_category: The child part category to be assigned.
        :param: child_part_number: The child part number to be assigned.
        :param: inner_child: The inner child part category. Defaults to None.
        :param: inner_child_part_number: The inner child part number. Defaults to None.

        Returns:
            dict: The payload dictionary with assigned part information.
        """
        log.debug(
            f"Assigning part information at root level. Payload : {payload} \n\n Root category : {root_category} \t Root part number : {root_part_number}"
        )
        self.assign_part_info_recursive(payload, root_category, root_part_number, 1)

        for child_device in payload["child_devices"]:
            log.debug(
                f"Assigning part information at child level. Child device : {child_device} \n\n Child category : {child_category} \t Child part number :{child_part_number}"
            )
            self.assign_part_info_recursive(
                child_device, child_category, child_part_number, 2
            )

            if "child_devices" in child_device and len(child_device["child_devices"]) > 0:
                for inner_child_device in child_device["child_devices"]:
                    log.debug(
                        f"Assigning part information at inner child level. Inner child_device : {inner_child_device} \n\n Inner child category : {inner_child_category} \t Inner child part number :{inner_child_part_number}"
                    )
                    self.assign_part_info_recursive(
                        inner_child_device,
                        inner_child_category,
                        inner_child_part_number,
                        3,
                    )
        return payload
