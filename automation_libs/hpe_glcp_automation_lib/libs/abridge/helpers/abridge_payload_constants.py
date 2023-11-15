"""
Payloads templates for Activate Bridge Api
"""
import logging
from logging import DEBUG

log = logging.getLogger(__name__)


class BridgePayload:
    log_level = DEBUG

    def bridge_login(self):
        bridge_login = {"credential_0": "", "credential_1": ""}
        return bridge_login

    def inventory_query_data(self):
        inventory_query_payload = {"devices": [""]}
        return inventory_query_payload

    def create_folder(self):
        create_default_folder_payload = {
            "folder": {"folderName": "FT_create_folder_7W25LJ2_test"}
        }
        return create_default_folder_payload

    def get_folder_by_query(self):
        get_folder_by_query_payload = {"folders": [""]}
        return get_folder_by_query_payload

    def get_all_rule_by_folder(self):
        get_all_rule_by_folder_payload = {"folders": [""]}
        return get_all_rule_by_folder_payload

    def delete_created_folder(self):
        delete_created_folder = {"folders": [""]}
        return delete_created_folder
