"""
Helper function for New Subscription order App Api Class
"""
import logging
import time
from datetime import datetime, timedelta

import pytz

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp
from hpe_glcp_automation_lib.libs.sm.helpers.sm_payload_constants import SmInputPayload

log = logging.getLogger(__name__)


class NewSubsOrder:
    """
    Helper class for New Subscription order App Api Class
    """

    def __init__(
        self, end_username, app_api_host, sso_host, aop_client_id, aop_client_secret
    ):
        """
        Initialize NewSubsOrder class
        :param app_api_host: App api hostname for cluster
        :param sso_host: sso_host
        :param aop_client_id: app client_id
        :param aop_client_secret: app client_secret
        """
        self.end_username = end_username
        self.payload = SmInputPayload()
        self.app_api_host = app_api_host
        self.sso_host = sso_host
        self.aop_client_id = aop_client_id
        self.aop_client_secret = aop_client_secret
        self.order = SubscriptionManagementApp(
            self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret
        )

    def create_svc_order(self, order_type=None):
        """
        Create service order, supported order types/payloads currently:
            default - vm_backup
            ZERTO - svc_dis_recovery_zerto
        :param order_type: Type of service order
        :return: license order key
        """
        if order_type == "ZERTO":
            svc_order_data = self.payload.svc_dis_recovery_zerto()
        else:
            svc_order_data = self.payload.vm_bakcup()

        svc_order_data["activate"]["contacts"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["activate"]["contacts"][0][
            "countryId"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["activate"]["contacts"][0][
            "globalId"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["activate"]["endUserName"] = self.end_username + " Company"
        for i in range(0, len(svc_order_data["activate"]["parties"])):
            svc_order_data["activate"]["parties"][i][
                "id"
            ] = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=False, digits=True
            )
            svc_order_data["activate"]["parties"][i][
                "countryId"
            ] = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=False, digits=True
            )
            svc_order_data["activate"]["parties"][i][
                "globalId"
            ] = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=False, digits=True
            )
        svc_order_data["activate"]["party"]["id"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["activate"]["party"][
            "countryId"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["activate"]["party"][
            "globalId"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["activate"][
            "po"
        ] = "PONUMCCS_09_170120_" + RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["entitlements"][0]["contract"] = svc_order_data[
            "contract"
        ]  # contract should be same for order
        svc_order_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["entitlements"][0][
            "quote"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True
        )
        svc_order_data["quote"] = svc_order_data["entitlements"][0][
            "quote"
        ]  # quote should be same for order
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            svc_order = self.order.create_subs_order(svc_order_data)
            if svc_order:
                lic_order = self.order.get_subs_order(svc_order_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error("Failed to create lic_order_key order with S/N {}".format(e))
            return False

    def create_compute_subs_order(self, order_type=None):
        """
        Create compute iaas order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "ALLETRA_4K":
            compute_iaas_subs_data = self.payload.subs_compute_alletra_4k()
        else:
            compute_iaas_subs_data = self.payload.subs_compute_iaas()

        compute_iaas_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        compute_iaas_subs_data["entitlements"][0]["quote"] = compute_iaas_subs_data[
            "quote"
        ]
        compute_iaas_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        compute_iaas_subs_data["entitlements"][0]["contract"] = compute_iaas_subs_data[
            "contract"
        ]
        compute_iaas_subs_data["activate"]["endUserName"] = (
            "Test_" + self.end_username + " Company"
        )
        compute_iaas_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        compute_iaas_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + compute_iaas_subs_data["customer"]["MDM"]
        )
        compute_iaas_subs_data["activate"]["party"]["id"] = compute_iaas_subs_data[
            "customer"
        ]["MDM"]
        for i in range(0, len(compute_iaas_subs_data["activate"]["parties"])):
            compute_iaas_subs_data["activate"]["parties"][i][
                "id"
            ] = compute_iaas_subs_data["customer"]["MDM"]
        for i in range(0, len(compute_iaas_subs_data["activate"]["contacts"])):
            compute_iaas_subs_data["activate"]["contacts"][i][
                "id"
            ] = compute_iaas_subs_data["customer"]["MDM"]
        compute_iaas_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            comp_iaas_order = self.order.create_subs_order(compute_iaas_subs_data)
            if comp_iaas_order:
                lic_order = self.order.get_subs_order(compute_iaas_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_compute_gecko_subs_order(self, order_type=None):
        """
        Create Gecko subscription order
        :param order_type: Type of compute order
        :return: subscription order key, subscription order quote, subscription order devices
        """
        if order_type == "PROLIANT":
            compute_iaas_subs_data = self.payload.subs_compute_gecko_iaas()
        else:
            compute_iaas_subs_data = self.payload.subs_compute_gecko_iaas()

        compute_iaas_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        compute_iaas_subs_data["entitlements"][0]["quote"] = compute_iaas_subs_data[
            "quote"
        ]
        compute_iaas_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        compute_iaas_subs_data["entitlements"][0]["contract"] = compute_iaas_subs_data[
            "contract"
        ]
        compute_iaas_subs_data["activate"]["endUserName"] = (
            "Test_" + self.end_username + " Company"
        )
        compute_iaas_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        compute_iaas_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + compute_iaas_subs_data["customer"]["MDM"]
        )
        compute_iaas_subs_data["activate"]["party"]["id"] = compute_iaas_subs_data[
            "customer"
        ]["MDM"]
        for i in range(0, len(compute_iaas_subs_data["activate"]["parties"])):
            compute_iaas_subs_data["activate"]["parties"][i][
                "id"
            ] = compute_iaas_subs_data["customer"]["MDM"]
        for i in range(0, len(compute_iaas_subs_data["activate"]["contacts"])):
            compute_iaas_subs_data["activate"]["contacts"][i][
                "id"
            ] = compute_iaas_subs_data["customer"]["MDM"]
        compute_iaas_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        compute_iaas_subs_data["entitlements"][0]["licenses"][0]["devices"][0][
            "serial"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=True
        )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            comp_iaas_order = self.order.create_subs_order(compute_iaas_subs_data)
            if comp_iaas_order:
                lic_order = self.order.get_subs_order(compute_iaas_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                lic_order_devices = lic_order[0]["entitlements"][0]["licenses"][0][
                    "devices"
                ]
                return lic_order_key, lic_order[0]["quote"], lic_order_devices
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_storage_hciaas_order(self, order_type=None):
        """
        Create storage hciaas order
        :param device_list: List of devices with material information:
        [{"serial": "AF-917497", "material": "6050"}, {"serial": "AF-917498", "material": "6050"}]
        :param order_type: Type of order
        :return: license order key
        """
        if order_type == "HCIAAS":
            storage_hciaas_subs_data = self.payload.subs_storage_hciaas()
        else:
            return False

        storage_hciaas_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        storage_hciaas_subs_data["entitlements"][0]["quote"] = storage_hciaas_subs_data[
            "quote"
        ]
        storage_hciaas_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        storage_hciaas_subs_data["entitlements"][0][
            "contract"
        ] = storage_hciaas_subs_data["contract"]
        storage_hciaas_subs_data["activate"]["endUserName"] = (
            "Test_" + self.end_username + " Company"
        )
        storage_hciaas_subs_data["customer"][
            "MDM"
        ] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        storage_hciaas_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + storage_hciaas_subs_data["customer"]["MDM"]
        )
        storage_hciaas_subs_data["activate"]["party"]["id"] = storage_hciaas_subs_data[
            "customer"
        ]["MDM"]
        for i in range(0, len(storage_hciaas_subs_data["activate"]["parties"])):
            storage_hciaas_subs_data["activate"]["parties"][i][
                "id"
            ] = storage_hciaas_subs_data["customer"]["MDM"]
        for i in range(0, len(storage_hciaas_subs_data["activate"]["contacts"])):
            storage_hciaas_subs_data["activate"]["contacts"][i][
                "id"
            ] = storage_hciaas_subs_data["customer"]["MDM"]
        storage_hciaas_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )

        # Add serial(s) and material for HCIAAS device
        serial = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=True
        )
        material = "6050"
        device_list = [{"serial": serial, "material": material}]
        for i in range(0, len(device_list)):
            storage_hciaas_subs_data["entitlements"][0]["licenses"][0]["devices"].append(
                device_list[i]
            )

        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            storage_hciaas_order = self.order.create_subs_order(storage_hciaas_subs_data)
            if "created" in storage_hciaas_order["response"]:
                lic_order = self.order.get_subs_order(storage_hciaas_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                lic_order_devices = lic_order[0]["entitlements"][0]["licenses"][0][
                    "devices"
                ]
                return lic_order_key, lic_order[0]["quote"], lic_order_devices
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_storage_baas_order(self, order_type=None):
        """
        Create compute iaas order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "HCIAAS":
            storage_baas_subs_data = None
            return False
        else:
            storage_baas_subs_data = self.payload.subs_storage_baas()

        storage_baas_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        storage_baas_subs_data["entitlements"][0]["quote"] = storage_baas_subs_data[
            "quote"
        ]
        storage_baas_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        storage_baas_subs_data["entitlements"][0]["contract"] = storage_baas_subs_data[
            "contract"
        ]
        storage_baas_subs_data["activate"]["endUserName"] = (
            "Test_" + self.end_username + " Company"
        )
        storage_baas_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        storage_baas_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + storage_baas_subs_data["customer"]["MDM"]
        )
        storage_baas_subs_data["activate"]["party"]["id"] = storage_baas_subs_data[
            "customer"
        ]["MDM"]
        for i in range(0, len(storage_baas_subs_data["activate"]["parties"])):
            storage_baas_subs_data["activate"]["parties"][i][
                "id"
            ] = storage_baas_subs_data["customer"]["MDM"]
        for i in range(0, len(storage_baas_subs_data["activate"]["contacts"])):
            storage_baas_subs_data["activate"]["contacts"][i][
                "id"
            ] = storage_baas_subs_data["customer"]["MDM"]
        storage_baas_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            storage_baas_order = self.order.create_subs_order(storage_baas_subs_data)
            if "created" in storage_baas_order["response"]:
                lic_order = self.order.get_subs_order(storage_baas_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_combined_ap_sw_gw_subs_order(self):
        """
        Create combined (ap, switch, gateway) order
        :return: license order keys for ap, switch, gateway and quote
        """
        combined_subs_data = self.payload.combined_iap_sw_gw_subs()
        combined_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        combined_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        combined_subs_data["activate"]["endUserName"] = self.end_username + " Company"
        combined_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        combined_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + combined_subs_data["customer"]["MDM"]
        )
        combined_subs_data["activate"]["party"]["id"] = combined_subs_data["customer"][
            "MDM"
        ]
        for i in range(0, len(combined_subs_data["activate"]["parties"])):
            combined_subs_data["activate"]["parties"][i]["id"] = combined_subs_data[
                "customer"
            ]["MDM"]
        for i in range(0, len(combined_subs_data["activate"]["contacts"])):
            combined_subs_data["activate"]["contacts"][i]["id"] = combined_subs_data[
                "customer"
            ]["MDM"]

        for i in range(0, len(combined_subs_data["entitlements"])):
            combined_subs_data["entitlements"][i]["quote"] = combined_subs_data["quote"]
            combined_subs_data["entitlements"][i]["contract"] = combined_subs_data[
                "contract"
            ]
            if i == 0:
                combined_subs_data["entitlements"][i]["licenses"][0]["id"] = (
                    RandomGenUtils.random_string_of_chars(
                        length=20, lowercase=False, uppercase=False, digits=True
                    )
                    + "AP"
                )
            elif i == 1:
                combined_subs_data["entitlements"][i]["licenses"][0]["id"] = (
                    RandomGenUtils.random_string_of_chars(
                        length=20, lowercase=False, uppercase=False, digits=True
                    )
                    + "SW"
                )
            elif i == 2:
                combined_subs_data["entitlements"][i]["licenses"][0]["id"] = (
                    RandomGenUtils.random_string_of_chars(
                        length=20, lowercase=False, uppercase=False, digits=True
                    )
                    + "GW"
                )
            else:
                return False

        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            combined_subs_order = self.order.create_subs_order(combined_subs_data)
            if combined_subs_order:
                lic_order = self.order.get_subs_order(combined_subs_data["quote"])

                for i in range(0, len(lic_order[0]["entitlements"])):
                    if "AP" in lic_order[0]["entitlements"][i]["licenses"][0]["id"]:
                        ap_order_key = lic_order[0]["entitlements"][i]["licenses"][0][
                            "id"
                        ]
                    elif "SW" in lic_order[0]["entitlements"][i]["licenses"][0]["id"]:
                        sw_order_key = lic_order[0]["entitlements"][i]["licenses"][0][
                            "id"
                        ]
                    elif "GW" in lic_order[0]["entitlements"][i]["licenses"][0]["id"]:
                        gw_order_key = lic_order[0]["entitlements"][i]["licenses"][0][
                            "id"
                        ]

                if (ap_order_key and sw_order_key) and gw_order_key:
                    return ap_order_key, sw_order_key, gw_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create combined order: {}, {}, {}, with quote: {}\n. Exception details: {}".format(
                    ap_order_key, sw_order_key, gw_order_key, lic_order, e
                )
            )
            return False

    def create_ap_subs_order(self):
        """
        Create Switch 6200 order
        :param order_type: Type of compute order
        :return: license order key
        """
        ap_subs_data = self.payload.subs_data_ap()
        ap_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        ap_subs_data["entitlements"][0]["quote"] = ap_subs_data["quote"]
        ap_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        ap_subs_data["entitlements"][0]["contract"] = ap_subs_data["contract"]
        ap_subs_data["activate"]["endUserName"] = self.end_username + " Company"
        ap_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        ap_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + ap_subs_data["customer"]["MDM"]
        )
        ap_subs_data["activate"]["party"]["id"] = ap_subs_data["customer"]["MDM"]
        for i in range(0, len(ap_subs_data["activate"]["parties"])):
            ap_subs_data["activate"]["parties"][i]["id"] = ap_subs_data["customer"]["MDM"]
        for i in range(0, len(ap_subs_data["activate"]["contacts"])):
            ap_subs_data["activate"]["contacts"][i]["id"] = ap_subs_data["customer"][
                "MDM"
            ]
        ap_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            ap_subs_order = self.order.create_subs_order(ap_subs_data)
            if ap_subs_order:
                lic_order = self.order.get_subs_order(ap_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_ap_subs_order_ztp_disabled(self, endUserName=None, party_id=None):
        """
        Create IAP order for ZTP Disabled
        :param endusername: endusername can be random number string / actual endusername from customer alias
        :param party_id: party_id can be random number string / actual party_id from customer alias
        :return: license order key, quote, endusername, party_id
        """
        ap_subs_data = self.payload.subs_data_ap()
        ap_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        ap_subs_data["entitlements"][0]["quote"] = ap_subs_data["quote"]
        ap_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        ap_subs_data["entitlements"][0]["contract"] = ap_subs_data["contract"]
        ap_subs_data["activate"]["endUserName"] = self.end_username + " Company"
        ap_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        ap_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + ap_subs_data["customer"]["MDM"]
        )
        ap_subs_data["activate"]["party"]["id"] = ap_subs_data["customer"]["MDM"]
        for i in range(0, len(ap_subs_data["activate"]["parties"])):
            ap_subs_data["activate"]["parties"][i]["id"] = ap_subs_data["customer"]["MDM"]
        for i in range(0, len(ap_subs_data["activate"]["contacts"])):
            ap_subs_data["activate"]["contacts"][i]["id"] = ap_subs_data["customer"][
                "MDM"
            ]
        ap_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )

        if endUserName != None:
            ap_subs_data["activate"]["endUserName"] = endUserName

        if party_id == None:
            del ap_subs_data["activate"]["party"]
            del ap_subs_data["activate"]["parties"]
        else:
            ap_subs_data["activate"]["party"]["id"] = party_id
            for index in range(len(ap_subs_data["activate"]["parties"])):
                ap_subs_data["activate"]["parties"][index]["id"] = party_id

        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            ap_subs_order = self.order.create_subs_order(ap_subs_data)
            if ap_subs_order:
                lic_order = self.order.get_subs_order(ap_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                log.info(
                    f"===ZTP_Disabled:: lic_order_key {lic_order_key} quote {lic_order[0]['quote']} endUserName {endUserName} party_id {party_id}==="
                )
                return (
                    lic_order_key,
                    lic_order[0]["quote"],
                    endUserName,
                    party_id,
                )
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_sw_subs_order(self, order_type=None, **kwargs):
        """
        Create Switch 6200 order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "6300":
            sw_6200_subs_data = self.payload.subs_data_sw_6300()
        else:
            sw_6200_subs_data = self.payload.subs_data_sw_6200()

        sw_6200_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        sw_6200_subs_data["entitlements"][0]["quote"] = sw_6200_subs_data["quote"]
        sw_6200_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        sw_6200_subs_data["entitlements"][0]["contract"] = sw_6200_subs_data["contract"]
        sw_6200_subs_data["activate"]["endUserName"] = self.end_username + " Company"
        sw_6200_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        sw_6200_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + sw_6200_subs_data["customer"]["MDM"]
        )
        sw_6200_subs_data["activate"]["party"]["id"] = sw_6200_subs_data["customer"][
            "MDM"
        ]
        for i in range(0, len(sw_6200_subs_data["activate"]["parties"])):
            sw_6200_subs_data["activate"]["parties"][i]["id"] = sw_6200_subs_data[
                "customer"
            ]["MDM"]
        for i in range(0, len(sw_6200_subs_data["activate"]["contacts"])):
            sw_6200_subs_data["activate"]["contacts"][i]["id"] = sw_6200_subs_data[
                "customer"
            ]["MDM"]
        sw_6200_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        if "endUserName" in kwargs:
            sw_6200_subs_data["activate"]["endUserName"] = kwargs.get("endUserName")
        if "party_id" in kwargs:
            if kwargs.get("party_id") is None:
                del sw_6200_subs_data["activate"]["party"]
                del sw_6200_subs_data["activate"]["parties"]
            else:
                sw_6200_subs_data["activate"]["party"]["id"] = kwargs.get("party_id")
                for index in range(len(sw_6200_subs_data["activate"]["parties"])):
                    sw_6200_subs_data["activate"]["parties"][index]["id"] = kwargs.get(
                        "party_id"
                    )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            sw_6200_subs_order = self.order.create_subs_order(sw_6200_subs_data)
            if sw_6200_subs_order:
                lic_order = self.order.get_subs_order(sw_6200_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                if "endUserName" in kwargs and "party_id" in kwargs:
                    return (
                        lic_order_key,
                        lic_order[0]["quote"],
                        kwargs.get("endUserName"),
                        kwargs.get("party_id"),
                    )
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_gw_subs_order(self, order_type=None):
        """
        Create Gateway 72xx order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "72XX":
            gw_72xx_subs_data = self.payload.subs_data_gw_72xx()
        else:
            gw_72xx_subs_data = self.payload.subs_data_gw_70xx()

        gw_72xx_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        gw_72xx_subs_data["entitlements"][0]["quote"] = gw_72xx_subs_data["quote"]
        gw_72xx_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        gw_72xx_subs_data["entitlements"][0]["contract"] = gw_72xx_subs_data["contract"]
        gw_72xx_subs_data["activate"]["endUserName"] = self.end_username + " Company"
        gw_72xx_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        gw_72xx_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + gw_72xx_subs_data["customer"]["MDM"]
        )
        gw_72xx_subs_data["activate"]["party"]["id"] = gw_72xx_subs_data["customer"][
            "MDM"
        ]
        for i in range(0, len(gw_72xx_subs_data["activate"]["parties"])):
            gw_72xx_subs_data["activate"]["parties"][i]["id"] = gw_72xx_subs_data[
                "customer"
            ]["MDM"]
        for i in range(0, len(gw_72xx_subs_data["activate"]["contacts"])):
            gw_72xx_subs_data["activate"]["contacts"][i]["id"] = gw_72xx_subs_data[
                "customer"
            ]["MDM"]
        gw_72xx_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            gw_72xx_subs_order = self.order.create_subs_order(gw_72xx_subs_data)
            if gw_72xx_subs_order:
                lic_order = self.order.get_subs_order(gw_72xx_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def create_vgw_subs_order(self, order_type=None):
        """
        Create Virtual Gateway (500M) order
        :param order_type: Type of VGW order or None for default (500M)
        :return: license order key
        """
        if order_type == "500":
            vgw_500_subs_data = self.payload.subs_data_vgw_500()
        else:
            vgw_500_subs_data = self.payload.subs_data_vgw_500()

        vgw_500_subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        vgw_500_subs_data["entitlements"][0]["quote"] = vgw_500_subs_data["quote"]
        vgw_500_subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        vgw_500_subs_data["entitlements"][0]["contract"] = vgw_500_subs_data["contract"]
        vgw_500_subs_data["activate"]["endUserName"] = self.end_username + " Company"
        vgw_500_subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        vgw_500_subs_data["activate"]["po"] = (
            "PONUMCCS_09_170120_" + vgw_500_subs_data["customer"]["MDM"]
        )
        vgw_500_subs_data["activate"]["party"]["id"] = vgw_500_subs_data["customer"][
            "MDM"
        ]
        for i in range(0, len(vgw_500_subs_data["activate"]["parties"])):
            vgw_500_subs_data["activate"]["parties"][i]["id"] = vgw_500_subs_data[
                "customer"
            ]["MDM"]
        for i in range(0, len(vgw_500_subs_data["activate"]["contacts"])):
            vgw_500_subs_data["activate"]["contacts"][i]["id"] = vgw_500_subs_data[
                "customer"
            ]["MDM"]
        vgw_500_subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        try:
            self.order = SubscriptionManagementApp(
                self.app_api_host,
                self.sso_host,
                self.aop_client_id,
                self.aop_client_secret,
            )
            vgw_500_subs_order = self.order.create_subs_order(vgw_500_subs_data)
            if vgw_500_subs_order:
                lic_order = self.order.get_subs_order(vgw_500_subs_data["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, lic_order, e
                )
            )
            return False

    def update_subs_order_to_expired(self, quote, licence=None):
        """
        Update order end date to current, subscription set to expired
        When dealing with combined licenses, you must provide a license key for
        which the subscription end date will be updated. It's important to note
        that this method can only support one license at a time.
        If you require support for multiple licenses,
        you will need to call this method again for each additional license.
        :param quote: Order type, any order
        :param licence: license key for expire subscription end date to specific license.
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        now = datetime.now()
        now_utc = now.astimezone(pytz.utc)

        if licence:
            for licence_order in lic_order[0]["entitlements"]:
                if licence_order["licenses"][0]["id"] == licence:
                    licence_order["licenses"][0]["appointments"][
                        "subscriptionEnd"
                    ] = now_utc.strftime("%d.%m.%Y %H:%M:%S")
                    log.info(f"updating subscription End date for licence {licence}")
                    break
        else:
            lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
                "subscriptionEnd"
            ] = now_utc.strftime("%d.%m.%Y %H:%M:%S")
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                if licence:
                    for get_licence_order in lic_order_updated[0]["entitlements"]:
                        if get_licence_order["licenses"][0]["id"] == licence:
                            lic_order_updated_key = get_licence_order["licenses"][0]["id"]
                            break
                else:
                    lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                        "licenses"
                    ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def terminate_subs_order(self, quote):
        """
        Terminate subscription order
        :param quote: Order type, any order
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        now = datetime.now()
        lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
            "subscriptionEnd"
        ] = now.strftime("%d.%m.%Y %H:%M:%S")
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                    "licenses"
                ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def extend_subs_order_by_seconds(self, quote, sec, licence=None):
        """
        Extend order end date by sec
        When dealing with combined licenses, you must provide a license key for
        which the subscription end date will be updated. It's important to note
        that this method can only support one license at a time.
        If you require support for multiple licenses,
        you will need to call this method again for each additional license.
        :param quote: Order type, any order
        :param sec: integer in seconds
        :param licence: license key for extend subscription end date to specific license.
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)
        lic_order[0]["reason"] = "Update"

        if licence:
            for licence_order in lic_order[0]["entitlements"]:
                if licence_order["licenses"][0]["id"] == licence:
                    curr_time = datetime.strptime(
                        licence_order["licenses"][0]["appointments"]["subscriptionEnd"],
                        "%d.%m.%Y %H:%M:%S",
                    )
                    new_time = curr_time + timedelta(seconds=sec)

                    licence_order["licenses"][0]["appointments"][
                        "subscriptionEnd"
                    ] = new_time.strftime("%d.%m.%Y %H:%M:%S")
                    log.info(
                        "\n\ncurr_time, new_time: {}, {}\n\n".format(curr_time, new_time)
                    )
                    break
        else:
            curr_time = datetime.strptime(
                lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
                    "subscriptionEnd"
                ],
                "%d.%m.%Y %H:%M:%S",
            )
            new_time = curr_time + timedelta(seconds=sec)

            lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
                "subscriptionEnd"
            ] = new_time.strftime("%d.%m.%Y %H:%M:%S")
            log.info("\n\ncurr_time, new_time: {}, {}\n\n".format(curr_time, new_time))

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                if licence:
                    for get_licence_order in lic_order_updated[0]["entitlements"]:
                        if get_licence_order["licenses"][0]["id"] == licence:
                            lic_order_updated_key = get_licence_order["licenses"][0]["id"]
                            break
                else:
                    lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                        "licenses"
                    ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to extend lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def decrease_subs_order_term_by_seconds(self, quote, sec, licence=None):
        """
        decrease order end date by sec
        When dealing with combined licenses, you must provide a license key for
        which the subscription end date will be updated. It's important to note
        that this method can only support one license at a time.
        If you require support for multiple licenses,
        you will need to call this method again for each additional license.
        :param quote: Order type, any order
        :param sec: integer in seconds
        :param licence: license key for decrease subscription term end date to specific license.
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)
        lic_order[0]["reason"] = "Update"

        if licence:
            for licence_order in lic_order[0]["entitlements"]:
                if licence_order["licenses"][0]["id"] == licence:
                    curr_time = datetime.strptime(
                        licence_order["licenses"][0]["appointments"]["subscriptionEnd"],
                        "%d.%m.%Y %H:%M:%S",
                    )
                    new_time = curr_time - timedelta(seconds=sec)

                    licence_order["licenses"][0]["appointments"][
                        "subscriptionEnd"
                    ] = new_time.strftime("%d.%m.%Y %H:%M:%S")
                    log.info(
                        "\n\ncurr_time, new_time: {}, {}\n\n".format(curr_time, new_time)
                    )
                    break
        else:
            curr_time = datetime.strptime(
                lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
                    "subscriptionEnd"
                ],
                "%d.%m.%Y %H:%M:%S",
            )
            new_time = curr_time - timedelta(seconds=sec)

            lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
                "subscriptionEnd"
            ] = new_time.strftime("%d.%m.%Y %H:%M:%S")
            log.info("\n\ncurr_time, new_time: {}, {}\n\n".format(curr_time, new_time))

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                if licence:
                    for get_licence_order in lic_order_updated[0]["entitlements"]:
                        if get_licence_order["licenses"][0]["id"] == licence:
                            lic_order_updated_key = get_licence_order["licenses"][0]["id"]
                            break
                else:
                    lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                        "licenses"
                    ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to extend lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def update_subs_order_to_cancelled(self, quote):
        """
        Update order to cancelled
        :param quote: Order type, any order
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Cancellation"
        now = datetime.now()
        lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
            "cancellationDate"
        ] = now.strftime("%d.%m.%Y %H:%M:%S")
        lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
            "subscriptionEnd"
        ] = lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
            "cancellationDate"
        ]

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                    "licenses"
                ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order to Cancellation, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def update_qty_subs_order(self, quote, qty):
        """
        Update order quantity
        :param quote: Order quote
        :param qty: Order quantity
        :return: Order quantity, license order quote
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        for i in range(0, len(lic_order[0]["entitlements"])):
            if lic_order[0]["entitlements"][i].get("total_qty"):
                lic_order[0]["entitlements"][i]["total_qty"] = qty
            if lic_order[0]["entitlements"][i]["licenses"][0].get("qty"):
                lic_order[0]["entitlements"][i]["licenses"][0]["qty"] = qty

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(5)
                lic_order_updated_qty = lic_order_updated[0]["entitlements"][0][
                    "licenses"
                ][0]["qty"]

                log.info("Quantity updated: {}".format(lic_order_updated_qty))
                return lic_order_updated_qty, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def upgrade_subs_tier_ap(self, quote):
        """
        Upgrade Subscription Tier (foundation to advanced)
        :param quote: Order quote, upgrade Tier from foundation to Advanced
        :return: Order quantity, license order quote
        """
        lic_order = self.order.get_subs_order(quote)
        time.sleep(2)

        lic_order[0]["reason"] = "Update"

        for i in range(len(lic_order[0]["entitlements"][0]["product"]["attributes"])):
            if (
                "TIER"
                == lic_order[0]["entitlements"][0]["product"]["attributes"][i]["name"]
            ) or (
                "TIER_AP"
                == lic_order[0]["entitlements"][0]["product"]["attributes"][i]["name"]
            ):
                lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                    "value"
                ] = "AD"
                lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                    "valueDisplay"
                ] = "Advanced"
                log.info(
                    "Tier updated: {}".format(
                        lic_order[0]["entitlements"][0]["product"]["attributes"][i]
                    )
                )

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(3)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)

                log.info("Tier upgraded to Advanced.")
                return lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def downgrade_subs_tier_ap(self, quote):
        """
        Downgrade Subscription Tier (advanced to foundation)
        :param quote: Order quote, downgrade Tier from Advanced to foundation
        :return: Order quantity, license order quote
        """
        lic_order = self.order.get_subs_order(quote)
        time.sleep(2)

        lic_order[0]["reason"] = "Update"

        for i in range(len(lic_order[0]["entitlements"][0]["product"]["attributes"])):
            if (
                "TIER"
                == lic_order[0]["entitlements"][0]["product"]["attributes"][i]["name"]
            ) or (
                "TIER_AP"
                == lic_order[0]["entitlements"][0]["product"]["attributes"][i]["name"]
            ):
                lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                    "value"
                ] = "FO"
                lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                    "valueDisplay"
                ] = "Foundation"
                log.info(
                    "Tier updated: {}".format(
                        lic_order[0]["entitlements"][0]["product"]["attributes"][i]
                    )
                )

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(3)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)

                log.info("Tier downgraded to Foundation.")
                return lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def set_future_flag(self, quote, boolvalue):
        """
        Update future flag to boolvalue (true or false)
        :param quote: Order quote
        :param boolvalue: True or False
        :return: boolvalue set, license order quote
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        lic_order[0]["future"] = boolvalue

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(5)
                lic_order_future_flag_val = lic_order_updated[0]["future"]

                log.info(
                    "Future flag updated with boolean value {} : {}".format(
                        boolvalue, lic_order_future_flag_val
                    )
                )
                return lic_order_future_flag_val, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update future flag value, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def set_autoRenewalDate_to_valid_date(self, quote):
        """
        Update order end date to current, subscription set to expired
        :param quote: Order type, any order
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"

        now = datetime.now()
        lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
            "autoRenewalDate"
        ] = now.strftime("%d.%m.%Y %H:%M:%S")
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                    "licenses"
                ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update autoRenewalDate, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def gt_lock_subs_tier_ap(self, quote):
        """
        GT_lock Subscription Tier
        :param quote: Order quote, GT_lock to Subscription Tier
        :return: license order quote or False
        """
        lic_order = self.order.get_subs_order(quote)
        lic_order[0]["reason"] = "GT_lock"
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                log.info("Subscription locked, GT_lock successful.")
                return lic_order_updated[0]["quote"]
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def gt_unlock_subs_tier_ap(self, quote):
        """
        GT_unlock Subscription Tier
        :param quote: Order quote, GT_unlock to Subscription Tier
        :return: license order quote or False
        """
        lic_order = self.order.get_subs_order(quote)
        lic_order[0]["reason"] = "GT_unlock"
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                log.info("Subscription unlocked, GT_unlock successful.")
                return lic_order_updated[0]["quote"]
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def update_bill_frequency_subs_order(self, quote):
        """
        Update order bill frequency to Monthly and Upfront vice versa
        :param quote: Order quote
        :return: Order bill frequency, license order quote or False
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        for i in range(len(lic_order[0]["entitlements"][0]["product"]["attributes"])):
            if (
                "BILL_FREQ"
                == lic_order[0]["entitlements"][0]["product"]["attributes"][i]["name"]
            ):
                if (
                    lic_order[0]["entitlements"][0]["product"]["attributes"][i]["value"]
                    == "UP"
                ):
                    lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                        "value"
                    ] = "M"
                    lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                        "valueDisplay"
                    ] = "MONTLY"
                else:
                    lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                        "value"
                    ] = "UP"
                    lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                        "valueDisplay"
                    ] = "Upfront"
                log.info(
                    "Tier updated: {}".format(
                        lic_order[0]["entitlements"][0]["product"]["attributes"][i]
                    )
                )
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                for i in range(
                    len(lic_order_updated[0]["entitlements"][0]["product"]["attributes"])
                ):
                    if (
                        "BILL_FREQ"
                        == lic_order_updated[0]["entitlements"][0]["product"][
                            "attributes"
                        ][i]["name"]
                    ):
                        lic_order_updated_bill_frequency = lic_order_updated[0][
                            "entitlements"
                        ][0]["product"]["attributes"][i]["value"]
                        break

                log.info(
                    "Bill Frequency updated: {}".format(lic_order_updated_bill_frequency)
                )
                return lic_order_updated_bill_frequency, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def set_update_baas_subscription_type(self, quote, subscription_type):
        """
        Update order subscription type BCP | MCP,
        :param quote: Order type, any order
        :param subscription_type: BCP(Business critical) | MCP(Mission Critical)
        :return: tuple(lic_order_updated_key , lic_order_updated_quote) | False in case of Exception or api call fail.
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        for i in range(len(lic_order[0]["entitlements"][0]["product"]["attributes"])):
            if (
                lic_order[0]["entitlements"][0]["product"]["attributes"][i]["name"]
                == "CS_TIER"
            ):
                lic_order[0]["entitlements"][0]["product"]["attributes"][i][
                    "value"
                ] = subscription_type
                log.info(
                    "subscription type update: {}".format(
                        lic_order[0]["entitlements"][0]["product"]["attributes"][i]
                    )
                )
                break

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                    "licenses"
                ][0]["id"]
                log.info("Subscription updated baas subscription type.")
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update autoRenewalDate, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def update_subs_order_to_expired_by_days(self, quote, days=1):
        """
        Update order end date to current, subscription set to expired as per day input given
        :param quote: Order type, any order
        :param days: number of days before license is set to be expired
        :return: license order key
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"
        new_date = datetime.now() - timedelta(days=days)
        lic_order[0]["entitlements"][0]["licenses"][0]["appointments"][
            "subscriptionEnd"
        ] = new_date.strftime("%d.%m.%Y %H:%M:%S")
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                lic_order_updated_key = lic_order_updated[0]["entitlements"][0][
                    "licenses"
                ][0]["id"]
                return lic_order_updated_key, lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def upgrade_subs_tier_combined(self, quote, licence_keys):
        """
        Upgrade Subscription Tier (foundation to advanced)
        :param quote: Order quote, upgrade Tier from foundation to Advanced
        :param licence_keys: should be list of license key (IAP, SWITCH)
        :return: Order quantity, license order quote or False
        """
        lic_order = self.order.get_subs_order(quote)
        lic_order[0]["reason"] = "Update"

        for i in range(len(lic_order[0]["entitlements"])):
            if lic_order[0]["entitlements"][i]["licenses"][0]["id"] in licence_keys:
                for j in range(
                    len(lic_order[0]["entitlements"][i]["product"]["attributes"])
                ):
                    if (
                        "TIER"
                        == lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "name"
                        ]
                    ) or (
                        "TIER_AP"
                        == lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "name"
                        ]
                    ):
                        lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "value"
                        ] = "AD"
                        lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "valueDisplay"
                        ] = "Advanced"

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                log.info("Checking Tier upgraded to Advanced.")
                lic_order_updated = self.order.get_subs_order(quote)
                check_tier_updated = ""
                for i in range(len(lic_order[0]["entitlements"])):
                    if (
                        lic_order[0]["entitlements"][i]["licenses"][0]["id"]
                        in licence_keys
                    ):
                        for j in range(
                            len(lic_order[0]["entitlements"][i]["product"]["attributes"])
                        ):
                            if (
                                "TIER"
                                == lic_order[0]["entitlements"][i]["product"][
                                    "attributes"
                                ][j]["name"]
                            ) or (
                                "TIER_AP"
                                == lic_order[0]["entitlements"][i]["product"][
                                    "attributes"
                                ][j]["name"]
                            ):
                                check_tier_updated = lic_order[0]["entitlements"][i][
                                    "product"
                                ]["attributes"][j]["valueDisplay"]

                if check_tier_updated == "Advanced":
                    log.info("Tier upgraded to Advanced.")
                    return lic_order_updated[0]["quote"]
                else:
                    log.info("Unable to upgraded Tier to Advanced.")
                    return False
            else:
                log.info("Unable to upgraded Tier to Advanced. From update function")
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def downgrade_subs_tier_combined(self, quote, licence_keys):
        """
        Downgrade Subscription Tier (advanced to foundation)
        :param quote: Order quote, upgrade Tier from foundation to Advanced
        :param licence_keys: should be list of license key (IAP, SWITCH)
        :return: Order quantity, license order quote or False
        """
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]["reason"] = "Update"

        for i in range(len(lic_order[0]["entitlements"])):
            if lic_order[0]["entitlements"][i]["licenses"][0]["id"] in licence_keys:
                for j in range(
                    len(lic_order[0]["entitlements"][i]["product"]["attributes"])
                ):
                    if (
                        "TIER"
                        == lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "name"
                        ]
                    ) or (
                        "TIER_AP"
                        == lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "name"
                        ]
                    ):
                        lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "value"
                        ] = "FO"
                        lic_order[0]["entitlements"][i]["product"]["attributes"][j][
                            "valueDisplay"
                        ] = "Foundation"

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            res = self.order.update_subs_order(lic_order[0])
            if res:
                log.info("Checking Tier downgraded to Foundation.")
                lic_order_updated = self.order.get_subs_order(quote)
                check_tier_updated = ""
                for i in range(len(lic_order[0]["entitlements"])):
                    if (
                        lic_order[0]["entitlements"][i]["licenses"][0]["id"]
                        in licence_keys
                    ):
                        for j in range(
                            len(lic_order[0]["entitlements"][i]["product"]["attributes"])
                        ):
                            if (
                                "TIER"
                                == lic_order[0]["entitlements"][i]["product"][
                                    "attributes"
                                ][j]["name"]
                            ) or (
                                "TIER_AP"
                                == lic_order[0]["entitlements"][i]["product"][
                                    "attributes"
                                ][j]["name"]
                            ):
                                check_tier_updated = lic_order[0]["entitlements"][i][
                                    "product"
                                ]["attributes"][j]["valueDisplay"]

                if check_tier_updated == "Foundation":
                    log.info("Tier downgraded to Foundation.")
                    return lic_order_updated[0]["quote"]
                else:
                    log.info("Unable to downgraded Tier to Foundation.")
                    return False
            else:
                log.info("Unable to downgraded Tier to Foundation. From update function")
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False

    def create_opsramp_sku_subs_order(
        self, new_subs_order_session, sku, description, payload
    ):
        """
        Create subscription order
        :param payload: Payload of opsramp subscription order
        :param description: Description of sku
        :param sku: sku to create subs order
        :param new_subs_order_session: session to get payload from lib
        :return: license order key
        """
        subs_data = payload
        subs_data["quote"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        subs_data["entitlements"][0]["quote"] = subs_data["quote"]
        subs_data["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        subs_data["entitlements"][0]["contract"] = subs_data["contract"]
        subs_data["activate"]["endUserName"] = self.end_username + " Company"
        subs_data["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        subs_data["activate"]["po"] = "PONUMCCS_09_170120_" + subs_data["customer"]["MDM"]
        subs_data["activate"]["party"]["id"] = subs_data["customer"]["MDM"]
        for i in range(0, len(subs_data["activate"]["parties"])):
            subs_data["activate"]["parties"][i]["id"] = subs_data["customer"]["MDM"]
        for i in range(0, len(subs_data["activate"]["contacts"])):
            subs_data["activate"]["contacts"][i]["id"] = subs_data["customer"]["MDM"]
        subs_data["entitlements"][0]["licenses"][0][
            "id"
        ] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True
        )
        subs_data["entitlements"][0]["product"]["sku"] = sku
        subs_data["entitlements"][0]["product"]["description"] = description
        try:
            opsramp_subs_order = new_subs_order_session.order.create_subs_order(subs_data)
            if opsramp_subs_order:
                lic_order_key = subs_data["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, subs_data["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to create opsramp lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(
                    lic_order_key, subs_data["quote"], e
                )
            )
            return False

    def create_pce_iaas_order(
        self,
        subs_order_session,
        quote_number=None,
        product_sku=None,
        subscription_key=None,
        device_serial=None,
        device_material=None,
    ):
        """
        Create iaas subscription order for PCE
        :param subs_order_session: Session to get payload from lib
        :param quote_number:  Quote number
        :param product_sku: Software product SKU for PCE
        :param device_serial: Device serial number
        :param device_material: Device material/part number
        :param subscription_key: Subscription key
        :return: subscription key, quote_number, device_list
        """

        pce_iaas_payload = self.payload.create_pce_iaas_order_payload(
            quote_number=quote_number,
            product_sku=product_sku,
            subscription_key=subscription_key,
            device_serial=device_serial,
            device_material=device_material,
        )

        try:
            pce_iaas_order = subs_order_session.order.create_subs_order(pce_iaas_payload)
            if "created" in pce_iaas_order["response"]:
                lic_order = self.order.get_subs_order(pce_iaas_payload["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                lic_order_devices = lic_order[0]["entitlements"][0]["licenses"][0][
                    "devices"
                ]
                return lic_order_key, lic_order[0]["quote"], lic_order_devices
            else:
                return None
        except Exception as e:
            log.error(
                "Failed to create pce subscription order for key: {}, with quote: {}\n. Exception details: {}".format(
                    subscription_key, quote_number, e
                )
            )
            return None

    def create_sdwan_order(
        self,
        subs_order_session,
        quote_number=None,
        product_sku=None,
        subscription_key=None,
        end_username=None,
        tier="FO",
    ):
        """
        Create iaas subscription order for PCE
        :param subs_order_session: Session to get payload from lib
        :param quote_number:  Quote number
        :param product_sku: Software product SKU for PCE
        :param subscription_key: Subscription key
        :param end_username: End username
        :param tier: Subscription tier
        :return: Subscription key, quote_number
        """

        sdwan_payload = self.payload.create_sdwan_order_payload(
            quote_number=quote_number,
            product_sku=product_sku,
            subscription_key=subscription_key,
            end_username=end_username,
            tier=tier,
        )
        try:
            sdwan_order = subs_order_session.order.create_subs_order(sdwan_payload)
            if "created" in sdwan_order["response"]:
                lic_order = self.order.get_subs_order(sdwan_order["quote"])
                lic_order_key = lic_order[0]["entitlements"][0]["licenses"][0]["id"]
                return lic_order_key, lic_order[0]["quote"]
            else:
                return None
        except Exception as e:
            log.error(
                "Failed to create sdwan subscription order for key: {}, with quote: {}\n. Exception details: {}".format(
                    subscription_key, quote_number, e
                )
            )
            return None

    def update_subs_endusername_party_id(self, quote, endUserName=None, party_id=None):
        """
        Update Subscription Key Endusername and Party ID
        :param quote: Order quote
        :param endUserName: for updating endUserName
        :param party_id: for updating party_id
        :return: license order quote for success or False for Failure
        """
        lic_order = self.order.get_subs_order(quote)
        lic_order[0]["reason"] = "Update"

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            if endUserName == None:
                log.info(f'"endUserName" cannot be None')
                return False
            lic_order[0]["activate"]["endUserName"] = endUserName

            if party_id == None:
                del lic_order[0]["activate"]["party"]
                del lic_order[0]["activate"]["parties"]
            else:
                lic_order[0]["activate"]["party"]["id"] = party_id
                for index in range(len(lic_order[0]["activate"]["parties"])):
                    lic_order[0]["activate"]["parties"][index]["id"] = party_id
            log.info(f"lic_order[0] is {lic_order[0]} !")
            res = self.order.update_subs_order(lic_order[0])
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                log.info("Subscription updated.")
                return lic_order_updated[0]["quote"]
            else:
                return False
        except Exception as e:
            log.error(
                "Failed to update lic_order, with quote: {}\n. Exception details: {}".format(
                    quote, e
                )
            )
            return False
