"""
CCS Manager User API
"""
import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class CCSManagerUserApi(UISession):
    """
    CCS Manager API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing ui_doorway for user api calls")
        super().__init__(host, user, password, pcid)

        self.base_path = "/ui-doorway/ui"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

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

    def get_customers(self, params=None):
        """
        Get the list of customers from GLCP based on the query params passed
        :return: JSON object of customer details
        """
        return self.get(
            url=self._get_path(f"cm/customers"),
            ignore_handle_response=True,
            params=params,
        )

    def get_customers_provisions(self, params=None):
        """
        Get the list of applications provisioned for a customer
        :return: JSON object of customer details
        """
        return self.get(
            url=self._get_path(f"cm/customers/provisions"),
            ignore_handle_response=True,
            params=params,
        )

    def get_customers_detail(self, params):
        """
        Get the details of a customer
        :return: JSON object of customer details
        """
        return self.get(
            url=self._get_path(f"cm/customers/detail"),
            ignore_handle_response=True,
            params=params,
        )

    def get_customers_roles(self, params):
        """
        Get the roles of a customer
        :return: JSON object of customer roles
        """
        return self.get(
            url=self._get_path(f"cm/customers/roles"),
            ignore_handle_response=True,
            params=params,
        )

    def get_customers_profile_programs(self, pcid):
        """
        Get the list of customer profile programs
        :return: JSON object of customer profile programs
        """
        return self.get(
            url=self._get_path(f"cm/customers/profile/programs/{pcid}"),
            ignore_handle_response=True,
        )

    def get_customers_aliases(self, params):
        """
        Get the list of customer aliases
        :return: JSON object of customer aliases
        """
        return self.get(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            params=params,
        )

    def update_customers_contact(self, payload):
        """
        API method to update the customers profile contact
        :return: Successful message after update
        """
        return self.put(
            url=self._get_path(f"cm/customers/profile/contact"),
            ignore_handle_response=True,
            json=payload,
        )

    def update_customers_preferences(self, payload):
        """
        API method to update the customers multi factor auth
        :return: Successful message after update
        """
        return self.put(
            url=self._get_path(f"cm/customers/profile/preferences"),
            ignore_handle_response=True,
            json=payload,
        )

    def update_customers_programs(self, payload):
        """
        API method to update the customers profile programs
        :return: Successful message after update
        """
        return self.put(
            url=self._get_path(f"cm/customers/profile/programs"),
            ignore_handle_response=True,
            json=payload,
        )

    def create_customer_aliases(self, payload):
        """
        Create a alias for a customer
        :return: JSON object of customer aliases
        """
        return self.post(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            json=payload,
        )

    def update_customers_aliases(self, payload):
        """
        API method to update the customers aliases
        :return: Successful message after update
        """
        return self.put(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            json=payload,
        )

    def delete_customers_aliases(self, payload):
        """
        API method to delete the customers aliases
        :return: Successful message after update
        """
        return self.delete(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            json=payload,
        )

    def get_subscriptions(self, params=None):
        """
        Get the list of subscriptions based on the query params passed
        :return: JSON object of subscription details
        """
        return self.get(
            url=self._get_path(f"cm/subscriptions"),
            ignore_handle_response=True,
            params=params,
        )

    def get_license_tiers(self, params):
        """
        Get the list of license tiers based on the device type passed
        :return: JSON object of subscription tier details
        """
        return self.get(
            url=self._get_path(f"license/tiers"),
            ignore_handle_response=True,
            params=params,
        )

    def delete_subscriptions(self, payload):
        """
        API method to delete a subscription
        :return: JSON object of subscription details
        """
        return self.delete(
            url=self._get_path(f"cm/subscriptions"),
            ignore_handle_response=True,
            json=payload,
        )

    def generate_subscriptions(self, payload):
        """
        API method to create a subscription
        :return: JSON object of subscription details
        """
        return self.post(
            url=self._get_path(f"cm/subscriptions/eval"),
            ignore_handle_response=True,
            json=payload,
        )

    def modify_subscriptions(self, payload):
        """
        API method to modify or extend a subscription
        :return: JSON object of subscription details
        """
        return self.post(
            url=self._get_path(f"cm/subscriptions/modify"),
            ignore_handle_response=True,
            json=payload,
        )

    def transfer_subscriptions(self, payload):
        """
        API method to transfer a subscription
        :return: JSON object of subscription details
        """
        return self.put(
            url=self._get_path(f"cm/subscriptions/transfer"),
            ignore_handle_response=True,
            json=payload,
        )

    def get_users(self, params=None):
        """
        Get the list of users from GLCP based on query params passed

        limit: Maximum number of entries to be retrieved.
        offset: Starting position passed to the service for pagination
        email: Filter by username(email address)
        platform_customer_id: Filter by a CCS platform ID
        application_customer_id: Filter by application customer ID
        application_id: Filter by application ID. Across all application instances.
        application_instance_id: Filter by application instance ID
        user_status: Filter by one or more user status
        user_type: Filter by one or more user type
        domain: Filter by users of a particular email domain
        first_name: Filter by user's first name
        last_name: Filter by user's last name
        provision_status: Application Provision Status Enum list
        include_unverified: Append a list of all the unverified users to the list too(platform_customer_id to be given)

        :return: JSON object of users
        """
        return self.get(
            url=self._get_path(f"cm/users"), ignore_handle_response=True, params=params
        )

    def create_user_re_invite(self, payload):
        """
        API to invite a user to a platform account

        :payload: {
            "email": "string",
            "customer_id": "string",
            "customer_username": "string"
            }
        :return: Success message
        """
        return self.post(
            url=self._get_path(f"cm/users/re-invite"),
            ignore_handle_response=True,
            json=payload,
        )

    def delete_users(self, payload):
        """
        API to delete a user from a platform account.

        :payload:
        {
            "username": "string",
            "customer_id": "string",
            "delete_across_customers": false
        }
        :return: Success message
        """
        return self.delete(
            url=self._get_path(f"cm/users"), ignore_handle_response=True, json=payload
        )

    def create_invite_users(self, payload):
        """
        Invite user to a platform customer account and assign role.

        :payload : {
            "roles": [
                {
                "role": {
                    "slug": "string",
                    "application_id": "string",
                    "name": "string"
                },
                "access_rules": {
                    "msp": true,
                    "tenants": [
                    "ALL"
                    ]
                }
                }
            ],
            "user_names": [
                "string"
            ],
            "platform_customer_id": "string",
            "customer_username": "string",
            "contact_information": "user@example.com"
        }

        :return: Success message
        """
        return self.post(
            url=self._get_path(f"cm/users/invite"),
            ignore_handle_response=True,
            json=payload,
        )

    def update_user_roles(self, payload):
        """
        API method to update the customers roles.
        : payload :
        {
            "platform_customer_id": "string",
            "username": "string",
            "roles": {
                "add": [
                {
                    "role": {
                    "slug": "string",
                    "application_id": "string",
                    "name": "string"
                    },
                    "access_rules": {
                    "msp": true,
                    "tenants": [
                        "ALL"
                    ]
                    },
                    "scope_resource_instances": [
                    {
                        "matcher": "/my-app/foo/*",
                        "name": "string",
                        "application_cid": "string",
                        "application_instance_id": "string"
                    }
                    ],
                    "resource_restriction_policies": [
                    "string"
                    ]
                }
                ],
                "delete": [
                {
                    "slug": "string",
                    "application_id": "string",
                    "name": "string"
                }
                ],
                "update": [
                {
                    "role": {
                    "slug": "string",
                    "application_id": "string",
                    "name": "string"
                    },
                    "access_rules": {
                    "msp": true,
                    "tenants": [
                        "ALL"
                    ]
                    },
                    "scope_resource_instances": {
                    "add": [
                        {
                        "matcher": "/my-app/foo/*",
                        "name": "string",
                        "application_cid": "string",
                        "application_instance_id": "string"
                        }
                    ],
                    "delete": [
                        {
                        "matcher": "/my-app/foo/*",
                        "name": "string",
                        "application_cid": "string",
                        "application_instance_id": "string"
                        }
                    ]
                    }
                }
                ],
                "overwrite": [
                {
                    "role": {
                    "slug": "string",
                    "application_id": "string",
                    "name": "string"
                    },
                    "access_rules": {
                    "msp": true,
                    "tenants": [
                        "ALL"
                    ]
                    },
                    "scope_resource_instances": [
                    {
                        "matcher": "/my-app/foo/*",
                        "name": "string",
                        "application_cid": "string",
                        "application_instance_id": "string"
                    }
                    ],
                    "resource_restriction_policies": [
                    "string"
                    ]
                }
                ]
            }
        }

        :return: Successful message after update.
        """
        return self.put(
            url=self._get_path(f"cm/users/roles"),
            ignore_handle_response=True,
            json=payload,
        )

    def get_user_roles_assignments(self, params=None):
        """
        API to get user roles assignments

        :return: JSON object of user role assignments.
        """
        return self.get(
            url=self._get_path(f"cm/users/role-assignments"),
            ignore_handle_response=True,
            params=params,
        )

    def get_access(self, params=None):
        """
        API to manage access

        :return:
        {
            "effect": "DENY",
            "showCCSManagerFeature": False,
        }
        """
        return self.get(
            url=self._get_path(f"cm/access"), ignore_handle_response=True, params=params
        )

    def get_devices(self, params=None):
        """
        Get Device List of customer

        params:

        limit: Maximum number of entries that should be returned during the ADI API call during retrieval.
        offset: Starting position passed to the ADI service for retrival of devices
        platform_customer_id: Filter devices based on customer
        search_string: search feature for device search
        display_device_types: Filter for device based on device types
        application_ids: Filter for device based on application assigned
        archive_visibility: Filter for device based on archive status
        serial_number: For fetching device details
        part_number: For fetching device details
        device_type: For fetching device details
        unassigned_only: Filter Unassigned devices - boolean

        :return: JSON object of Devce list.
        """
        return self.get(
            url=self._get_path(f"cm/devices"), ignore_handle_response=True, params=params
        )

    def create_devices(self, payload):
        """
        Add AS devices
        :payload:
        {
            "devices": [
                {
                "location_id": "string",
                "location_name": "string",
                "contact_id": "string",
                "contact_name": "string",
                "serial_number": "VG2007087934",
                "entitlement_id": "AN0011AMS10356",
                "part_number": "874460-S01",
                "app_category": "COMPUTE",
                "tag_change_request": {
                    "create_tags": []
                }
                }
            ],
            "platform_customer_id": "string"
        }
        :return: Successfull response.
        """
        return self.post(
            url=self._get_path(f"cm/devices"), ignore_handle_response=True, json=payload
        )

    def update_devices(self, payload):
        """
        Assign the location/contact to list of devices of a customer account
        :payload:
        {
            "platform_customer_id": "pcid_123"
            "devices": [
                {
                    "serial_number": "CNJHK2RABC",
                    "device_type": "AP",
                    "part_number": "AP-555",
                    "archive": true
                },
                {
                    "serial_number": "CNJHK2RABC",
                    "mac_address": "aa:bb:cc:dd:ee:ff",
                    "part_number": "AP-555",
                    "device_type": "AP",
                    "archive": false,
                    "location_id": "string",
                    "location_name": "string",
                    "contact_id": "string",
                    "contact_name": "string"
                }
            ]
        }
        :return: Successful message after update.
        """
        return self.patch(
            url=self._get_path(f"cm/devices"), ignore_handle_response=True, json=payload
        )

    def get_stats(self, params=None):
        """
        Get Device Stats Information for location

        :return:
        {
            "total_customers": 2,
            "standalone_customers": 2,
            "msp_customers": 2,
            "tenant_customers": 2,
            "total_users": 2,
            "total_orders": 0,
            "total_subscriptions": 0
        }
        """
        return self.get(
            url=self._get_path(f"cm/stats"), ignore_handle_response=True, params=params
        )

    def create_stats(self, payload=None):
        """
        Get Device Stats Information for location
        :payload:
        {
            "platform_customer_id": ""
            "devices": [
                {
                "serial_number": "",
                "mac_address": "",
                "part_number": ""
                }
            ],
            "filter": {
                "assigned_contact": "true",
                "assigned_location": "true"
            }
        }
        returns:
            {
                "count": 1,
                "app_category": [
                    {
                    "NETWORK": 0
                    },
                    {
                    "STORAGE": 0
                    },
                    {
                    "COMPUTE": 0
                    }
                ],
            }

        payload:
            {
                "platform_customer_id": ""
                "filter": {
                    "location_id": ""
                },
                "group_by": [
                    "app_category"
                ]
            }
        return:
            {
                "app_category": [
                    {
                    "NETWORK": 10
                    },
                    {
                    "STORAGE": 6
                    },
                    {
                    "COMPUTE": 4
                    }
                ],
                "count": 20
        }
        """
        return self.post(
            url=self._get_path(f"cm/stats"), ignore_handle_response=True, json=payload
        )

    def get_ld_flags(self):
        """
        API method to get all ld flags on the cluster

        :return: JSON object of ld flags
        """
        return self.get(url=self._get_path(f"get-ld-flags"), ignore_handle_response=True)

    def get_activate_orders(self, params=None):
        """
        Get list of orders for given platform customer

        params:
        platform_customer_id: str
        page: int
        limit: int

        :return: JSON object of customer details
        """
        return self.get(
            url=self._get_path(f"cm/activate/orders"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_devices(self, params):
        """
        API method to get list of activate devices

        params:

        folder_name: str
        folder_id: str
        mac_address: str
        device_name: str
        serial_number: str
        part_number: str
        device_model: str
        search_string: str
        external_device_type: str
        limit: Pagination Limit
        page: Page Number
        platform_customer_id: str

        :return: JSON object of activate device details
        """
        return self.get(
            url=self._get_path(f"cm/activate/devices"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_devices_summary(self, params):
        """
        API method to get mac address list of activate devices

        params:

        action: str
        mode: str
        platform_customer_id: str

        :return: JSON object of activate device mac details
        """
        return self.get(
            url=self._get_path(f"cm/activate/devices/mac"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_device_details(self, serial_number, params=None):
        """
        API method to get list of activate device details

        params:

        serial_number: str
        mac_address: str
        devices_history_limit: int
        devices_history_page: int
        orders_limit: int
        orders_page: int
        platform_customer_id: str

        :return: JSON object of activate device details
        """
        return self.get(
            url=self._get_path(f"cm/activate/devices/{serial_number}"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_folders(self, params):
        """
        API method to get list of activate folders

        params:

        platform_customer_id: str
        customer_id: str
        folder_name: str
        folder_id: str
        search_name: str
        limit: Pagination Limit
        page: Page Number

        :return: JSON object of activate folders
        """
        return self.get(
            url=self._get_path(f"cm/activate/folders"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_rules(self, params):
        """
        API method to get activate rules

        params:

        platform_customer_id: str
        search_string: str
        folder_ids: str
        limit: Pagination Limit
        page: Page Number

        :return: JSON object of activate folder rules
        """
        return self.get(
            url=self._get_path(f"cm/activate/rules"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_folder_rules(self, folder_id, rule_name, params):
        """
        API method to get activate folder rules

        params:

        folder_id: str
        rule_name: str

        :return: JSON object of activate folder rules
        """
        return self.get(
            url=self._get_path(f"cm/activate/folders/{folder_id}/rules/{rule_name}"),
            ignore_handle_response=True,
            params=params,
        )

    def edit_activate_device_details(self, payload):
        """
        API method to edit any activate device details

        payload:
        {
            "device_update_request": [
                {
                    "mac": "string",
                    "device_name": "string",
                    "device_full_name": "string",
                    "device_description": "string",
                    "folder_id": "string",
                    "folder_name": "string",
                    "mode": "string"
                }
            ],
            "platform_customer_id": "string"
        }
        :return: JSON object of activate device details
        """
        return self.put(
            url=self._get_path(f"cm/activate/devices"),
            ignore_handle_response=True,
            json=payload,
        )

    def move_activate_device_to_folder(self, payload):
        """
        API method to move activate device to folder

        payload:
        {
            "folder_id": 0,
            "folder_name": "string",
            "devices": [
                {
                    "device_type": "AP",
                    "serial_number": "string",
                    "mac_address": "string",
                    "part_number": "string"
                }
            ],
            "platform_customer_id": "string"
        }
        :return: JSON object of activate device
        """
        return self.post(
            url=self._get_path(f"cm/activate/devices/folder"),
            ignore_handle_response=True,
            json=payload,
        )

    def move_activate_device_to_customer(self, payload):
        """
        API method to move activate device to customer

        payload:
        {
                "folder_id": 0,
                "folder_name": "string",
                "devices": [
                    {
                        "device_type": "AP",
                        "serial_number": "string",
                        "mac_address": "string",
                        "part_number": "string"
                    }
                ],
                "platform_customer_id": "string"

        }
        :return: JSON object of activate device
        """
        return self.post(
            url=self._get_path(f"cm/activate/devices/customer"),
            ignore_handle_response=True,
            json=payload,
        )

    def add_activate_exception_devices(self, payload):
        """
        API method to add activate exception devices

        payload:
        {
          "serial_numbers": [
            "string"
          ],
          "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.post(
            url=self._get_path(f"cm/activate/devices/exception"),
            ignore_handle_response=True,
            json=payload,
        )

    def create_activate_folder(self, payload):
        """
        API method to add activate folder

        payload:
        {
          "folder_name": "string",
          "parent_folder_id": "string",
          "description": "string",
          "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.post(
            url=self._get_path(f"cm/activate/folders"),
            ignore_handle_response=True,
            json=payload,
        )

    def modify_activate_folder(self, folder_id, payload):
        """
        API method to update activate folder

        folder_id: folder id
        payload:
        {
          "folder_name": "string",
          "parent_folder_id": "string",
          "description": "string",
          "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.put(
            url=self._get_path(f"cm/activate/folders/{folder_id}"),
            ignore_handle_response=True,
            json=payload,
        )

    def delete_activate_folder(self, folder_id, payload):
        """
        API method to delete activate folder.

        payload:
        {
          "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.delete(
            url=self._get_path(f"cm/activate/folders/{folder_id}"),
            ignore_handle_response=True,
            json=payload,
        )

    def create_activate_folder_rule(self, payload):
        """
        API method to create the folder rule

        payload:
        {
          "rule_id": "string",
          "rule_name": "string",
          "folder_id": "string",
          "folder_name": "string",
          "rule_type": "provision",
          "sub_type": "iap",
          "move_to_folder_id": "string",
          "move_to_folder_name": "string",
          "reference_rule_id": "string",
          "reference_rule_name": "string",
          "amp_ip": "string",
          "shared_secret": "string",
          "organization": "string",
          "controller": "string",
          "persist_controller_ip": true,
          "ap_group": "string",
          "value": "string",
          "enabled": true,
          "backup_controller": "string",
          "backup_controller_ip": "string",
          "vpn_mac": "string",
          "vpn_ip": "string",
          "backup_vpn_mac": "string",
          "country_code": "string",
          "config_group": "string",
          "config_node_path": "string",
          "redundancy_level": "string",
          "controller2": "string",
          "primary_ctrl_ip2": "string",
          "backup_controller2": "string",
          "vpn_mac2": "string",
          "vpn_ip2": "string",
          "backup_vpn_mac2": "string",
          "platform_customer_id": "string"
        }

        :return: JSON object of activate folder rules
        """
        return self.post(
            url=self._get_path(f"cm/activate/rules"),
            ignore_handle_response=True,
            json=payload,
        )

    def update_activate_folder_rule(self, rule_id, payload):
        """
        API method to update the folder rule

        payload:
        {
          "rule_id": "string",
          "rule_name": "string",
          "folder_id": "string",
          "folder_name": "string",
          "rule_type": "provision",
          "sub_type": "iap",
          "move_to_folder_id": "string",
          "move_to_folder_name": "string",
          "reference_rule_id": "string",
          "reference_rule_name": "string",
          "amp_ip": "string",
          "shared_secret": "string",
          "organization": "string",
          "controller": "string",
          "persist_controller_ip": true,
          "ap_group": "string",
          "value": "string",
          "enabled": true,
          "backup_controller": "string",
          "backup_controller_ip": "string",
          "vpn_mac": "string",
          "vpn_ip": "string",
          "backup_vpn_mac": "string",
          "country_code": "string",
          "config_group": "string",
          "config_node_path": "string",
          "redundancy_level": "string",
          "controller2": "string",
          "primary_ctrl_ip2": "string",
          "backup_controller2": "string",
          "vpn_mac2": "string",
          "vpn_ip2": "string",
          "backup_vpn_mac2": "string",
          "platform_customer_id": "string"
        }

        :return: Successful message.
        """
        return self.put(
            url=self._get_path(f"cm/activate/rules/{rule_id}"),
            ignore_handle_response=True,
            json=payload,
        )

    def delete_activate_folder_rule(self, rule_id, payload):
        """
        API method to delete a activate folder for a platform customer

        rule_id : rule id
        payload:
        {
          "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.delete(
            url=self._get_path(f"cm/activate/rules/{rule_id}"),
            ignore_handle_response=True,
            json=payload,
        )

    def create_activate_alias(self, payload):
        """
        API method to add a customer alias of a customer.

        payload:
        {
            "alias": "string",
            "type": "string",
            "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.post(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            json=payload,
        )

    def update_activate_alias(self, payload):
        """
        API method to update an alias name of a customer.

        alias : alias name
        payload:
        {
            "alias": "string",
            "type": "string",
            "platform_customer_id": "string"
        }
        :return: Successful message.
        """
        return self.put(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            json=payload,
        )

    def delete_activate_alias(self, payload):
        """
        API method to delete a activate alias of a customer.

        rule_id : rule id
        payload:
        {
            "platform_customer_id": "string",
            "alias" : "string"
        }
        :return: Successful message.
        """
        return self.delete(
            url=self._get_path(f"cm/customers/aliases"),
            ignore_handle_response=True,
            json=payload,
        )

    def get_activate_order_detail(self, order_number, params=None):
        """
        API method to dget order detail.

        :order_number : order_number
        :return: JSON object of activate order.
        """
        return self.get(
            url=self._get_path(f"cm/subscriptions/orders/detail/{order_number}"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_inventory_csv(self, params=None):
        """
        API method to get activate inventory csv.

        params:
        :platform_customer_id: str
        :return: Exported data.
        """
        return self.get(
            url=self._get_path(f"cm/activate/export/inventory-csv"),
            ignore_handle_response=True,
            params=params,
        )

    def get_activate_export_allow_list_cli(self, params=None):
        """
        API method to get export allowlist cli

        params:
        :platform_customer_id: str
        :new_format: bool
        :return: Exported data.
        """
        return self.get(
            url=self._get_path(f"cm/activate/export/allowlist-cli"),
            ignore_handle_response=True,
            params=params,
        )

    def create_activate_export_allow_list_cli(self, params, payload):
        """
        API method to export allowlist cli

        params:
        platform_customer_id: str
        limit: int
        offset: int
        new_format: bool

        payload:
        {
          "device_filter_request": [
            {
              "mac_address": "string",
              "serial_number": "string"
            }
          ]
        }

        :return: Successful message.
        """
        return self.post(
            url=self._get_path(f"cm/activate/export/allowlist-cli"),
            ignore_handle_response=True,
            json=payload,
            params=params,
        )

    def get_activate_export_allow_list_csv(self, params):
        """
        API method to export allowlist csv.

        params:
        :platform_customer_id: str
        :return: Exported data.
        """
        return self.get(
            url=self._get_path(f"cm/activate/export/allowlist-csv"),
            ignore_handle_response=True,
            params=params,
        )

    def get_notification(
        self,
    ):
        """
        API method get the notifications.

        params:
        :channel: Filter notifications based on channel
        limit: Number of entries per page
        next: Fetch notifications for next
        read: Filter notifications based on read flag
        dismissed: Filter notifications based on dismissed flag
        sort: Sort notifications based on param
        state: Filter notifications based on state
        from_date: Filter notifications based on fromDate
        to_date: Filter notifications based on toDate
        status: Filter notifications based on status
        search: Filter notifications based on search
        :return: JSON object of notification.
        """
        return self.get(
            url=f"/notifications-svc/ui/v1alpha1/notifications",
            ignore_handle_response=True,
        )

    def get_notification_details(self, notification_id):
        """
        API to get a details about notification.

        params:
        :notification_id: notification id
        :return: JSON object of notification.
        """
        return self.get(
            url=f"/notifications-svc/ui/v1alpha1/notifications/{notification_id}",
            ignore_handle_response=True,
        )

    def get_audit_logs(self, params: dict = None):
        """
        Get all the entries of a audit logs

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of auditlogs api
        """

        return self.get(
            url=self._get_path("cm/auditlogs"),
            ignore_handle_response=True,
            params=params,
        )

    def get_audit_logs_search_graphs(self, params: dict = None):
        """
        Get all the entries of a auditlogs-search-graphs

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of auditlogs-search-graphs api
        """

        return self.get(
            url=self._get_path("cm/auditlogs/search-graphs"),
            ignore_handle_response=True,
            params=params,
        )

    def get_subscription_orders_with_subscription(self, subscription_key):
        """
        API call to get subscription orders based on subscription key

        :subscription_key: subscription key of the subscription which
        :returns:
        [
            {
                "obj_key": "string",
                "reason": "Creation",
                "quote": "string",
                "entitlements": [
                    {
                        "line_item": "string",
                        "licenses": [
                            {
                                "subscription_key": "string",
                                "device_serial_number": "string",
                                "qty": "string",
                                "available_qty": "string",
                                "capacity": "string",
                                "appointments": {
                                    "term": "string",
                                    "subscription_start": "string",
                                    "subscription_end": "string",
                                    "delayed_activation": "string"
                                }
                            }
                        ],
                        "product": {
                            "sku": "string",
                            "description": "string"
                        }
                    }
                ],
                "activate": {
                    "sono": "string",
                    "sold_to": "string",
                    "sold_to_name": "string",
                    "sold_to_email": "string",
                    "ship_to": "string",
                    "ship_to_name": "string",
                    "ship_to_email": "string",
                    "end_user": "string",
                    "end_user_name": "string",
                    "end_user_email": "string",
                    "reseller": "string",
                    "reseller_name": "string",
                    "reseller_email": "string",
                    "po": "string",
                    "order_class": "string",
                    "party": {
                        "id": "string",
                        "country_id": "string",
                        "global_id": "string"
                    }
                }
            }
        ]
        """
        return self.get(
            url=self._get_path(
                f"cm/subscriptions/orders/subscription-key/{subscription_key}"
            ),
            ignore_handle_response=True,
        )

    def get_subscription_orders(self, purchase_order):
        """
        API call to get subscription orders based on purchase order id

        :purchase_order: purchase order number
        :returns:
        [
            {
                "obj_key": "string",
                "reason": "Creation",
                "quote": "string",
                "entitlements": [
                    {
                        "line_item": "string",
                        "licenses": [
                            {
                                "subscription_key": "string",
                                "device_serial_number": "string",
                                "qty": "string",
                                "available_qty": "string",
                                "capacity": "string",
                                "appointments": {
                                    "term": "string",
                                    "subscription_start": "string",
                                    "subscription_end": "string",
                                    "delayed_activation": "string"
                                }
                            }
                        ],
                        "product": {
                            "sku": "string",
                            "description": "string"
                        }
                    }
                ],
                "activate": {
                    "sono": "string",
                    "sold_to": "string",
                    "sold_to_name": "string",
                    "sold_to_email": "string",
                    "ship_to": "string",
                    "ship_to_name": "string",
                    "ship_to_email": "string",
                    "end_user": "string",
                    "end_user_name": "string",
                    "end_user_email": "string",
                    "reseller": "string",
                    "reseller_name": "string",
                    "reseller_email": "string",
                    "po": "string",
                    "order_class": "string",
                    "party": {
                        "id": "string",
                        "country_id": "string",
                        "global_id": "string"
                    }
                }
            }
        ]
        """
        return self.get(
            url=self._get_path(f"cm/subscriptions/orders/detail/{purchase_order}"),
            ignore_handle_response=True,
        )

    def update_subscription_orders(self, payload):
        """
        Update subscription order

        :payload:
        {
        "subscription_keys":[subscription_key],
        "end_user_name":"string"
        }

        Returns:
        {"message": "string"}
        """
        return self.put(
            url=self._get_path(f"cm/subscriptions/orders"),
            ignore_handle_response=True,
            json=payload,
        )

    def get_app_role_assignments(self, params: dict = None):
        """
        Get all the entries of app roleassignments

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of app_role_assignments api
        """

        return self.get(
            url=self._get_path("cm/applications/role-assignments"),
            ignore_handle_response=True,
            params=params,
        )

    def get_applications(self, params: dict = None):
        """
        Get all the entries of applications

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of applications api
        """

        return self.get(
            url=self._get_path("cm/applications"),
            ignore_handle_response=True,
            params=params,
        )

    def get_application_details(self, application_id: str):
        """
        Get the application details

        :param application_id: uuid string of an application
        :return: response object of application details api
        """

        return self.get(
            url=self._get_path(f"cm/applications/{application_id}"),
            ignore_handle_response=True,
        )

    def get_app_instances(self, params: dict = None):
        """
        Get all the entries of app instances

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of app instances api
        """

        return self.get(
            url=self._get_path("cm/app-instances"),
            ignore_handle_response=True,
            params=params,
        )

    def get_app_instance_details(self, app_instance_id: str):
        """
        Get the app instance details

        :param app_instance_id: uuid string of an app instance
        :return: response object of app instance details api
        """

        return self.get(
            url=self._get_path(f"cm/app-instances/{app_instance_id}"),
            ignore_handle_response=True,
        )

    def get_customer_rrp(self, params: dict = None):
        """
        Get all Customer Resource Restriction Policies of a platform customer

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of resource_restrictions api
        """

        return self.get(
            url=self._get_path("cm/resource_restrictions"),
            ignore_handle_response=True,
            params=params,
        )

    def get_rrp_details(self, rrp_id: str):
        """
        Gets all info on a resource restriction policy identified by resource restriction policy id

        :param rrp_id: uuid string of an rrp
        :return: response object of resource-restrictions-detail api
        """

        return self.get(
            url=self._get_path(f"cm/resource_restrictions/detail/{rrp_id}"),
            ignore_handle_response=True,
        )

    def get_user_rrp(self, params: dict = None):
        """
        Get all users of a customer account who are assigned given resource restriction policy

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of resource-restrictions-users api
        """

        return self.get(
            url=self._get_path("cm/resource_restrictions/users"),
            ignore_handle_response=True,
            params=params,
        )

    def get_tenants(self, params: dict = None):
        """
        Get all Tenants of a MSP Customer

        :param params: (optional) Dictionary to be sent in the query string
        :return: response object of tenants api
        """

        return self.get(
            url=self._get_path("cm/tenants"),
            ignore_handle_response=True,
            params=params,
        )

    def delete_tenant(self, payload: dict):
        """
        API to delete a tenant account

        :param payload: Dictionary should contains customer_id and username
        :return: response object of tenant api
        """
        return self.delete(
            url=self._get_path("cm/tenants"), ignore_handle_response=True, json=payload
        )

    def update_tenant(self, username: str, payload: dict):
        """
        API to update tenant account details

        :param username: Username/ Email address of the user who is performing the tenent
        update operation
        :param payload: Dictionary with update params
        :return: response object of tenant api
        """
        return self.put(
            url=self._get_path(f"cm/tenants/{username}"),
            ignore_handle_response=True,
            json=payload,
        )

    def get_ip_access_rule(self, params: dict = None):
        """
        Get IP Access Rules for Platform Customer

        :param params: (optional) Dictionary with query params
        :return: response object of ip_access_rule api
        """
        return self.get(
            url=self._get_path("cm/ip-access-rule"),
            ignore_handle_response=True,
            params=params,
        )

    def toggle_ip_access_rule(self, params: dict = None):
        """
        Enable/Disable IP Access Rules for Platform Customer

        :param params: (optional) Dictionary with query params
        :return: response object of toggle_ip_access_rule api
        """
        return self.put(
            url=self._get_path("cm/ip-access-rule/toggle"),
            ignore_handle_response=True,
            params=params,
        )
