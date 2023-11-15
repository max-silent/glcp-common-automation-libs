"""
Payloads templates for ADI Internal Api
"""
import logging

log = logging.getLogger(__name__)


class AdiInternalInputPayload:
    """
    Preparing payloads for API method call.
    """

    def get_ccs_device_history_event_payload(
        self, event_id, serial_number, part_number, mac_address, source_ip, folder_id
    ):
        data = (
            '{"device_histories":[{"serial_number":"serial_to_replace",'
            '"mac_address_to_replace":"13:00:00:99:18:52","part_number":"part_to_replace",'
            '"device_model":"STRARCUS101","date":"1685577600000","source_ip":"source_ip_to_replace",'
            '"geo":"","folder_id":"folder_id_to_replace"}]}'.replace(
                "serial_to_replace", serial_number
            )
            .replace("part_to_replace", part_number)
            .replace("mac_address_to_replace", mac_address)
            .replace("source_ip_to_replace", source_ip)
            .replace("folder_id_to_replace", folder_id)
        )

        payload = {
            "specversion": "1.0.0",
            "id": event_id,
            "source": "CCS",
            "type": "CCS_DEVICE_HISTORY_EVENT",
            "topic": "app.account-management.users.CCS",
            "time": "2023-08-14T13:41:59.562452",
            "data": data,
        }

        return payload.copy()
