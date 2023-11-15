"""
Create platform customer event, application customer event payload template
"""
import datetime
import json
import logging
import uuid
from logging import DEBUG

from hpe_glcp_automation_lib.libs.commons.enum.enum_utils import (
    AccountStatus,
    AccountType,
    EventType,
    Operation,
    OperationalMode,
    OperationStatus,
    ProvisionStatus,
)

log = logging.getLogger(__name__)


class AmInputPayload(object):
    pod_namespace: str = ""
    log_level = DEBUG

    def create_msp_tenant(self):
        msp_create_tenant_data = {
            "tenant": {
                "customer_id": "string",
                "company_name": "string",
                "description": "string",
                "address": {
                    "street_address": "string",
                    "city": "string",
                    "state_or_region": "string",
                    "zip": "string",
                    "country_code": "AW",
                    "street_address_2": "string",
                },
                "created_at": "2019-08-24T14:15:22Z",
                "updated_at": "2019-08-24T14:15:22Z",
                "accessed_at": "string",
                "phone_number": "string",
                "email": "user@example.com",
                "customer_logo": {},
            },
            "created_by": "user@example.com",
            "platform_cid": "string",
        }
        return msp_create_tenant_data

    @staticmethod
    def platform_event():
        platform_event_data = {
            "specversion": "1.0.0",
            "id": "uuid",
            "source": "CCS",
            "type": "CUSTOMER_EVENT",
            "topic": "app.account-management.users.CCS",
            "time": "2023-01-01T10:10:10Z",
            "data": {
                "event": {
                    "contact": {
                        "created_by": "first-ft-user@test.com",
                        "email": None,
                        "company_name": "GLCP AUTO HPE INC",
                        "address": {
                            "street_address": "6280 America Center Drive",
                            "city": "San Jose",
                            "state_or_region": "CA",
                            "zip": "94089",
                            "country_code": "USA",
                        },
                        "phone_number": "1404404404",
                    },
                    "customer_id": "platformCustomerId",
                    "msp_id": None,
                    "account": {
                        "account_type": "STANDALONE",
                        "status": "ACTIVE",
                        "operation_mode": "DEFAULT",
                        "created_at": None,
                        "updated_at": None,
                    },
                    "region": "US-WEST2",
                    "preferences": None,
                },
                "operation": "CREATE",
                "status": "SUCCESS",
                "failure_reason": None,
            },
        }

        return platform_event_data

    @staticmethod
    def create_platform_event_payload(
        platform_customer_id=None,
        msp_platform_customer_id=None,
        account_type=AccountType.STANDALONE,
        account_status=AccountStatus.ACTIVE,
        operation=Operation.CREATE,
        operation_mode=OperationalMode.DEFAULT,
    ):
        """

        :param platform_customer_id:
        :param msp_platform_customer_id:
        :param account_type:
        :param account_status:
        :param operation:
        :param operation_mode:
        :return:
        """

        platform_customer_event = AmInputPayload.platform_event()

        if platform_customer_id is None:
            platform_customer_id = uuid.uuid4().hex

        if account_type == AccountType.TENANT and msp_platform_customer_id is None:
            log.error(
                "Failed to send platform event for platform_customer_id: {}, operation: {} as MSP platform id is empty"
                " for account_type: {}".format(
                    platform_customer_id, operation, account_type
                )
            )
            return None

        platform_customer_event["id"] = str(uuid.uuid4())
        platform_customer_event["time"] = datetime.datetime.now().isoformat()
        platform_customer_event["type"] = str(EventType.CUSTOMER_EVENT)
        platform_customer_event["operation"] = str(operation)
        platform_customer_event["status"] = str(OperationStatus.SUCCESS)

        platform_customer_event["data"]["event"]["customer_id"] = platform_customer_id
        if msp_platform_customer_id is not None:
            platform_customer_event["data"]["event"]["msp_id"] = msp_platform_customer_id
        platform_customer_event["data"]["event"]["account"]["account_type"] = str(
            account_type
        )
        platform_customer_event["data"]["event"]["account"]["status"] = str(
            account_status
        )
        platform_customer_event["data"]["event"]["account"]["operation_mode"] = str(
            operation_mode
        )

        platform_customer_event["data"] = json.dumps(platform_customer_event["data"])

        return platform_customer_event

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
    def create_app_provision_event_payload(
        provision_status=ProvisionStatus.PROVISIONED,
        account_type=AccountType.STANDALONE,
        application_id=None,
        application_instance_id=None,
        platform_customer_id=None,
        application_customer_id=None,
        operation=Operation.CREATE,
        operation_status=OperationStatus.SUCCESS,
        msp_application_customer_id=None,
    ):
        """

        :param provision_status:
        :param account_type:
        :param application_id:
        :param application_instance_id:
        :param platform_customer_id:
        :param application_customer_id:
        :param operation:
        :param operation_status:
        :param msp_application_customer_id:
        :return:
        """

        app_provision_event = AmInputPayload.app_provision_event()

        if application_customer_id is None:
            application_customer_id = uuid.uuid4().hex

        if platform_customer_id is None:
            log.error(
                "Failed to send app provision event for application_customer_id: {}, operation: {} as platform "
                "customer id is empty for account_type: {}".format(
                    application_customer_id, operation, account_type
                )
            )
            return None

        if account_type == AccountType.TENANT and msp_application_customer_id is None:
            log.error(
                "Failed to send app provision event for platform_customer_id: {}, application_customer_id: {} "
                "operation: {} as MSP application customer id is empty for account_type: {}".format(
                    platform_customer_id, application_customer_id, operation, account_type
                )
            )
            return None

        if application_id is None:
            log.error(
                "Failed to send app provision event for application_customer_id: {}, operation: {} as application "
                "id is empty for account_type: {}".format(
                    application_customer_id, operation, account_type
                )
            )
            return None

        if application_instance_id is None:
            log.error(
                "Failed to send app provision event for application_customer_id: {}, operation: {} as application "
                "instance id is empty for account_type: {}".format(
                    application_customer_id, operation, account_type
                )
            )
            return None

        app_provision_event["id"] = str(uuid.uuid4())
        app_provision_event["time"] = datetime.datetime.now().isoformat()
        app_provision_event["type"] = str(EventType.APP_PROVISION)
        app_provision_event["operation"] = str(operation)
        app_provision_event["status"] = str(operation_status)

        app_provision_event["data"]["event"]["provision_status"] = str(provision_status)
        app_provision_event["data"]["event"]["account_type"] = str(account_type)
        app_provision_event["data"]["event"]["application_id"] = application_id
        app_provision_event["data"]["event"][
            "application_instance_id"
        ] = application_instance_id
        app_provision_event["data"]["event"][
            "platform_customer_id"
        ] = platform_customer_id
        app_provision_event["data"]["event"][
            "application_customer_id"
        ] = application_customer_id
        if msp_application_customer_id is not None:
            app_provision_event["data"]["event"]["msp_id"] = msp_application_customer_id

        app_provision_event["data"] = json.dumps(app_provision_event["data"])

        return app_provision_event
