"""
Subscription Management Internal Apis
"""
import inspect
import logging
import uuid
from datetime import datetime, timedelta

import jwt

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session
from hpe_glcp_automation_lib.libs.commons.enum.enum_utils import SubscriptionType
from hpe_glcp_automation_lib.libs.sm.helpers.sm_payload_constants import SmInputPayload

log = logging.getLogger()


class SubscriptionManagementInternal(Session):
    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing sm_internal_api for user api calls")
        super().__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "http://subscription-management-svc.ccs-system.svc.cluster.local:80"
        self.internal_api_path = "/subscription-management/internal"
        self.app_api_path = "/subscription-management/app"
        self.internal_event_path = "/subscription-management/internal-events"
        self.api_version_v1 = "/v1"
        self.api_version_v2 = "/v2"
        self.payload = SmInputPayload()

    def _get_path_v1(self, path):
        return f"{self.host}{self.internal_api_path}{self.api_version_v1}/{path}"

    def _get_path_v2(self, path):
        return f"{self.host}{self.internal_api_path}{self.api_version_v2}/{path}"

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

    def extend_subscription_internal(self, params, headers):
        """
        Extend subscription modifies subscription end date and/or quantity of subscription
        :param:app
        :param:sku
        :param:force_flag
        :param:subscription_tier
        :param:subscription_key
        :param:subscription_type
        :param:increase_quantity_by:Required
        :param:extend_end_seconds:Required
        :headers:CCS-Impersonated-Platform-Customer-Id:Required
        :headers:CCS-Username
        :headers:CCS-Platform-Customer-Id:Required
        returns :Response of API call
        """

        url = f"{self.host}{self.internal_api_path}{self.api_version_v2}/subscription/management"
        log.info(url)
        res = self.post(url=url, params=params, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def transfer_subscription_internal(self, params, headers):
        """
        Transfer subscription transfers subscription from one customer to another customer
        :param:force_flag
        :param:platform_customer_id_new:Required
        :param:subscription_key:Required
        :headers:CCS-Platform-Customer-Id:Required
        :headers:CCS-Username
        returns :Response of API call
        """

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/transfer"
        log.info(url)
        res = self.put(url=url, params=params, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def cancel_subscription_internal(self, pcid, params, headers):
        """
        Cancels subscription of customer
        :param:platform_customer_id_new:Required
        :param:subscription_key:Required
        :headers:CCS-Platform-Customer-Id:Required
        :headers:CCS-Username
        returns :Response of API call
        """

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/{pcid}/management"
        log.info(url)
        res = self.put(url=url, params=params, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def genarate_vgw_aubscription_internal(self, pcid, params, headers):
        """
        Create VGW specific subscriptions, e.g. VGW2G, VGW4G, VGW500M
        :param:subscription_tiers
        returns :Response of API call
        """
        url = f"{self.base_url}{self.internal_api_path}{self.api_version_v1}/subscription/{pcid}/eval"
        res = self.post(url=url, params=params, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def get_subscription_info_pre_claim(self, pcid, subscription_key, params):
        """
        Get the pre-claim subscription information for given subscription-key
        :param subscription_key: Subscription Key, Required
        :param params: Request uri params, Required
        :param headers: CCS-Platform-Customer-Id, Required
        returns :Response of API call
        """
        headers = {
            "CCS-Platform-Customer-Id": pcid,
            "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            "Content-Type": "application/json",
        }
        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/{subscription_key}/preclaim"
        log.debug(url)
        res = self.get(url=url, params=params, headers=headers)
        return res

    def can_delete_customer_internal(self, pcid, headers):
        """
        Check whether the customer can be deleted or not.
        :param:platform_customer_id:Required
        :headers:CCS-Transaction-Id
        returns :Response of API call {"reason":"Workspace with id {platform_customer_id} has 0 subscriptions associated",
        "can_be_deleted":true}
        """

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/customers/{pcid}/canDelete"
        log.debug(url)
        res = self.get(url=url, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def claim_subscription(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        license_key=None,
        claim_request=None,
    ):
        """
        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param username: Username
        :param license_key: License key
        :param claim_request: Claim request
        :return:
        """

        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "claim_subscription_" + transaction_id
        else:
            transaction_id = "claim_subscription_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id

        if license_key is None:
            log.error(
                "Failed to claim subscription order as empty license key was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        if claim_request is None:
            log.error(
                "Failed to claim subscription order as empty claim_request was received in tx: {} for "
                "license_key: {}".format(transaction_id, license_key)
            )
            return None

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/{license_key}"
        log.info(url)
        res = self.post(
            url=url, headers=headers, json=claim_request, ignore_handle_response=True
        )
        log.info(f"response of claim subscription request[{transaction_id}]: {res}")
        return res

    def get_subs_for_platform_id(
        self, transaction_id=None, username=None, platform_customer_id=None
    ):
        """
        Get application subscription for devices
        :param:pcid: required - Platform customer ID
        returns :Response of API call
        """
        if platform_customer_id is None:
            log.error(
                "Failed to get_subscriptions by platform customer id as empty platform customer id was "
                "received in tx: {}".format(transaction_id)
            )
            return None

        headers = {}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "get_subs_by_pcid_" + transaction_id
        else:
            transaction_id = "get_subs_by_pcid_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username

        headers["CCS-Platform-Customer-Id"] = platform_customer_id

        params = {}

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscriptions"
        res = self.get(url=url, params=params, headers=headers)
        log.info(url)
        log.info(f"Response of API request[tx:{transaction_id}]: {res}")
        return res

    def get_sub_assignment_for_devices(
        self,
        transaction_id=None,
        username=None,
        platform_customer_id=None,
        subscription_type=None,
        subscription_key=None,
    ):
        """
        Get application subscription for devices
        :param:pcid: required - Platform customer ID
        returns :Response of API call
        """
        if platform_customer_id is None:
            log.error(
                "Failed to get_sub_assignment_for_devices by platform customer id as empty platform customer id was "
                "received in tx: {}".format(transaction_id)
            )
            return None

        headers = {}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "get_sm_devices_by_acid_" + transaction_id
        else:
            transaction_id = "get_sm_devices_by_acid_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username

        headers["CCS-Platform-Customer-Id"] = platform_customer_id

        params = {}
        if subscription_type and (subscription_type in SubscriptionType._member_names_):
            params["subscription_type"] = subscription_type
        if subscription_key:
            params["subscription_key"] = subscription_key

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/devices"
        res = self.get(url=url, params=params, headers=headers)
        log.info(url)
        log.info(f"Response of API request[tx:{transaction_id}]: {res}")
        return res

    def assign_subscription(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        application_customer_id=None,
        assignment_request=None,
        ignore_handle_response=False,
    ):
        """
        :param ignore_handle_response:
        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param username: Username
        :param application_customer_id:
        :param assignment_request: [{"device_serial": "SERIAL", "part_number": "PART", "subscription_key": "key"}]
        :return:
        """

        if platform_customer_id is None:
            log.error(
                "Failed to assign subscription to devices as empty platform customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        headers = {"Content-Type": "application/json"}
        headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if transaction_id:
            headers["CCS-Transaction-Id"] = "assign_sub_" + transaction_id
        else:
            transaction_id = "assign_sub_" + platform_customer_id
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        if application_customer_id:
            headers["CCS-Application-Customer-Id"] = application_customer_id

        if assignment_request is None:
            log.error(
                "Failed to assign subscription to device as empty assignment_request is received in tx: {} for "
                "platform customer id: {}".format(transaction_id, platform_customer_id)
            )
            return None

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/devices"
        log.info(url)
        res = self.post(
            url=url,
            headers=headers,
            json=assignment_request,
            ignore_handle_response=ignore_handle_response,
        )
        log.info(f"response of assign subscription request[{transaction_id}]: {res}")
        return res

    def assign_subscription_by_application_cid(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        application_customer_id=None,
        assignment_request=None,
        ignore_handle_response=False,
    ):
        """
        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param username: Username
        :param application_customer_id:
        :param assignment_request: [{"device_serial": "SERIAL", "part_number": "PART", "subscription_key": "key"}]
        :return:
        """
        if platform_customer_id is None:
            log.error(
                "Failed to assign subscription to devices as empty platform customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        if application_customer_id is None:
            log.error(
                "Failed to assign subscription to devices as empty application customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        headers = {"Content-Type": "application/json"}
        headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if transaction_id:
            headers["CCS-Transaction-Id"] = "assign_app_sub_" + transaction_id
        else:
            transaction_id = "assign_app_sub_" + platform_customer_id
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        if application_customer_id:
            headers["CCS-Application-Customer-Id"] = application_customer_id
        token = self._get_bearer_token()
        headers["Authorization"] = f"Bearer {token}"

        if assignment_request is None:
            log.error(
                "Failed to assign subscription to device as empty assignment_request is received in tx: {} for "
                "platform customer id: {}".format(transaction_id, platform_customer_id)
            )
            return None

        url = (
            f"{self.host}{self.app_api_path}{self.api_version_v1}/subscription/{platform_customer_id}"
            f"/application/{application_customer_id}/devices"
        )
        log.info(url)
        res = self.post(
            url=url,
            headers=headers,
            json=assignment_request,
            ignore_handle_response=ignore_handle_response,
        )
        log.info(
            f"response of assign subscription request using application customer id[{transaction_id}]: {res}"
        )
        return res

    def get_subscriptions_by_application_cid(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        application_customer_id=None,
    ):
        """
        :param application_customer_id:
        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param username: Username
        :return:
        """
        if platform_customer_id is None:
            log.error(
                "Failed to get subscriptions for application customer id  as empty platform customer id was "
                "received in tx: {}".format(transaction_id)
            )
            return None

        if application_customer_id is None:
            log.error(
                "Failed to get subscriptions for application customer id as empty application customer id was "
                "received in tx: {}".format(transaction_id)
            )
            return None

        headers = {"Content-Type": "application/json"}
        headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if transaction_id:
            headers["CCS-Transaction-Id"] = "assign_app_sub_" + transaction_id
        else:
            transaction_id = "assign_app_sub_" + platform_customer_id
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        if application_customer_id:
            headers["CCS-Application-Customer-Id"] = application_customer_id
        token = self._get_bearer_token()
        headers["Authorization"] = f"Bearer {token}"

        params = {}
        url = (
            f"{self.host}{self.app_api_path}{self.api_version_v1}/subscription/{platform_customer_id}"
            f"/application/{application_customer_id}"
        )
        log.info(url)
        res = self.get(url=url, headers=headers, params=params)
        log.info(
            f"response of get subscriptions using application customer id[{transaction_id}]: {res}"
        )
        return res

    def assign_iaas_subscription(
        self,
        transaction_id=None,
        platform_customer_id=None,
        application_customer_id=None,
        username=None,
        assignment_request=None,
    ):
        """
        :param application_customer_id:
        :param headers:
        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param username: Username
        :param assignment_request: [{"device_serial": "SERIAL", "part_number": "PART", "device_type": "PCE"}]
        :return:
        """

        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "assign_iaas_sub_" + transaction_id
        else:
            transaction_id = "assign_iaas_sub_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username

        if platform_customer_id is None:
            log.error(
                "Failed to assign iaas subscription order as empty platform customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        headers["CCS-Platform-Customer-Id"] = platform_customer_id

        if application_customer_id is None:
            log.error(
                "Failed to assign iaas subscription order as empty application customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        headers["CCS-Application-Customer-Id"] = application_customer_id

        if assignment_request is None:
            log.error(
                "Failed to assign iaas subscription order as empty assignment_request is received in tx: {} for "
                "platform customer id: {}".format(transaction_id, platform_customer_id)
            )
            return None

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/devices/iaas"
        log.info(url)
        res = self.post(url=url, headers=headers, json=assignment_request)
        log.info(
            f"response of assign iaas subscription request[tx:{transaction_id}]: {res}"
        )
        return res

    def claim_and_assign_iaas_subscription(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        subscription_key=None,
        subscription_and_device_claim_request=None,
        **kwargs,
    ):
        """
        :param transaction_id: Transaction id
        :param platform_customer_id: Platform customer id
        :param username: Username
        :param subscription_key: Subscription key
        :param subscription_and_device_claim_request:
                   {
                        "devices": [
                            {
                            "serial_number": "SERIAL",
                            "part_number": "PART",
                            "application": {
                                "application_customer_id": "acid"
                                },
                            "device_type": "COMPUTE/STORAGE"
                            }
                        ]
                    }
        :return:
        """

        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "claim_and_assign_iaas_sub_" + transaction_id
        else:
            transaction_id = "claim_and_assign_iaas_sub_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/{subscription_key}/claim"
        log.info(url)
        res = self.post(
            url=url, headers=headers, json=subscription_and_device_claim_request, **kwargs
        )
        log.info(
            f"Response of claim and assign iaas subscription request[tx:{transaction_id}]: {res}"
        )
        return res

    def get_async_operation_resource(
        self,
        identifier=None,
    ):
        """
        :param identifier: Identifier
        :return:
        """
        headers = {"Content-Type": "application/json"}
        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/async-operations/{identifier}"
        log.info(url)
        res = self.get(url=url, headers=headers)
        log.info(f"Response of API get async operation resource request: {res}")
        return res

    def get_subscription_for_iaas_device(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        device_serial=None,
        device_material=None,
    ):
        """

        :param transaction_id:
        :param platform_customer_id:
        :param username:
        :param device_serial:
        :param device_material:
        :return:
        """

        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "get_subs_iaas_" + transaction_id
        else:
            transaction_id = "get_subs_iaas_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        if platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id

        params = {"device_serial": device_serial, "material": device_material}

        url = (
            f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/iaas"
        )
        log.info(url)
        res = self.get(url=url, params=params, headers=headers)
        log.info(f"Response of API request[tx:{transaction_id}]: {res}")
        return res

    def remove_assignment(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        device_serial_numbers=[],
    ):
        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "remove_assignment_" + transaction_id
        else:
            transaction_id = "remove_assignment_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username

        if platform_customer_id is None:
            log.error(
                "Failed to remove_assignment as empty platform customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        headers["CCS-Platform-Customer-Id"] = platform_customer_id

        params = {"deviceSerialNumbers": device_serial_numbers}

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscription/devices"
        log.info(url)
        res = self.delete(url=url, params=params, headers=headers)
        log.info(f"Response of API request[tx:{transaction_id}]: {res}")
        return res

    def activate_subscription(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        subscription_key=None,
    ):
        """

        :param transaction_id:
        :param platform_customer_id:
        :param username:
        :param subscription_key:
        :return:
        """

        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "activate_sub_" + transaction_id
        else:
            transaction_id = "activate_sub_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username

        if platform_customer_id is None:
            log.error(
                "Failed to activate subscription as empty platform customer id was received in tx: {}".format(
                    transaction_id
                )
            )
            return None

        headers["CCS-Platform-Customer-Id"] = platform_customer_id

        if subscription_key is None:
            log.error(
                "Failed to activate subscription as empty subscription key was received in tx: {}, "
                "platform id:{}".format(transaction_id, platform_customer_id)
            )
            return None

        params = {
            "platform_customer_id": platform_customer_id,
            "subscription_key": subscription_key,
        }

        url = f"{self.host}{self.internal_api_path}{self.api_version_v1}/subscriptions"
        log.info(url)
        res = self.patch(
            url=url, params=params, headers=headers, ignore_handle_response=True
        )
        log.info(f"Response of API request[tx:{transaction_id}]: {res}")
        return res

    def create_subs_order(self, data, transaction_id=None, username=None):
        """
        Create subscription order
        :param transaction_id:
        :param data : Required for creating order
        returns :Response of API call
        """
        headers = {"Content-Type": "application/json"}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "create_subs_" + transaction_id
        else:
            transaction_id = "create_subs_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        token = self._get_bearer_token()
        headers["Authorization"] = f"Bearer {token}"

        url = f"{self.host}{self.app_api_path}{self.api_version_v1}/orders"
        log.info(url)
        res = self.post(url=url, headers=headers, json=data)
        log.info(f"response of subscription status check[tx:{transaction_id}]: {res}")
        return res

    def get_subs_order(self, quote_number, transaction_id=None, username=None):
        """
        Get subscription order based on quote_number
        :param transaction_id:
        :param quote_number : Quote Number
        returns :Response of API call
        """
        headers = {}
        if transaction_id:
            headers["CCS-Transaction-Id"] = "get_subs_" + transaction_id
        else:
            transaction_id = "get_subs_" + uuid.uuid1().hex
            headers["CCS-Transaction-Id"] = transaction_id
        if username:
            headers["CCS-Username"] = username
        token = self._get_bearer_token()
        headers["Authorization"] = f"Bearer {token}"

        url = f"{self.host}{self.app_api_path}{self.api_version_v1}/orders/{quote_number}"
        log.info(url)
        res = self.get(url=url, headers=headers)
        log.info(f"response of subscription status check[tx:{transaction_id}]: {res}")
        return res

    def send_platform_customer_event(
        self, platform_customer_id=None, platform_customer_event=None
    ):
        """

        :param platform_customer_id: Platform customer id
        :param platform_customer_event: CUSTOMER_EVENT
        :return:
        """

        if platform_customer_event is not None:
            headers = {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": "platform_customer_"
                + platform_customer_event["id"],
                "Content-Type": "application/json",
            }

            log.info(f"Sending platform_customer_event: {platform_customer_event}")
            url = f"{self.host}{self.internal_event_path}{self.api_version_v1}/callback"
            log.info(url)
            response = self.post(url=url, headers=headers, json=platform_customer_event)
            log.info(f"Response of platform_customer_event request: {response}")
            return response
        else:
            return None

    def send_app_provision_event(
        self, platform_customer_id=None, app_provision_event=None
    ):
        """

        :param platform_customer_id: Platform custome id
        :param app_provision_event: APP_PROVISION event
        :return:
        """

        if app_provision_event is not None:
            headers = {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": "app_provision_" + app_provision_event["id"],
                "Content-Type": "application/json",
            }

            log.info(f"Sending app_provision_event: {app_provision_event}")
            url = f"{self.host}{self.internal_event_path}{self.api_version_v1}/callback"
            log.info(url)
            response = self.post(url=url, headers=headers, json=app_provision_event)
            log.info(f"Response of app_provision_event request: {response}")
            return response
        else:
            return None

    def send_device_provision_internal_event(
        self, platform_customer_id=None, device_provision_internal_event=None
    ):
        """

        :param platform_customer_id: Platform customer id
        :param device_provision_internal_event: DEVICE_PROVISION_INTERNAL_EVENT
        :return:
        """

        if device_provision_internal_event is not None:
            headers = {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": "device_provision_"
                + device_provision_internal_event["id"],
                "Content-Type": "application/json",
            }

            log.info(
                f"Sending device_internal_provision_event: {device_provision_internal_event}"
            )
            url = f"{self.host}{self.internal_event_path}{self.api_version_v1}/callback"
            log.info(url)
            response = self.post(
                url=url, headers=headers, json=device_provision_internal_event
            )
            log.info(f"Response of device_internal_provision_event request: {response}")
            return response
        else:
            return None

    def send_device_unprovision_internal_event(
        self, platform_customer_id=None, device_unprovision_internal_event=None
    ):
        """

        :param platform_customer_id: Platform customer id
        :param device_unprovision_internal_event: DEVICE_UNPROVISION_INTERNAL_EVENT
        :return:
        """

        if device_unprovision_internal_event is not None:
            headers = {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Transaction-Id": "device_unprovision_"
                + device_unprovision_internal_event["id"],
                "Content-Type": "application/json",
            }

            log.info(
                f"Sending device_internal_unprovision_event: {device_unprovision_internal_event}"
            )
            url = f"{self.host}{self.internal_event_path}{self.api_version_v1}/callback"
            log.info(url)
            response = self.post(
                url=url, headers=headers, json=device_unprovision_internal_event
            )
            log.info(f"Response of device_internal_provision_event request: {response}")
            return response
        else:
            return None

    def gen_sm_order_internal_event(self, params, headers):
        """
        Create an SM order event (https://bit.ly/3Qb0x1o)
        :param: order_event
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscriptions/kafka/orderEvent"
        res = self.post(url=url, params=params, headers=headers)
        log.info(f"Response of API request: {res}")
        return res

    def get_eval_subscription_requests(self, pcid, params):
        """
        Get the eval subscription requests
        :param pcid: platformcustomer_id, Required
        :param params: Request uri params, Required
        :param headers: CCS-Platform-Customer-Id, Required
        returns :Response of API call
        """
        headers = {
            "CCS-Platform-Customer-Id": pcid,
            "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            "Content-Type": "application/json",
        }
        url = f"{self.host}{self.base_path}{self.api_version_v1}/subscription/eval"
        log.debug(url)
        res = self.get(url=url, params=params, headers=headers)
        return res
