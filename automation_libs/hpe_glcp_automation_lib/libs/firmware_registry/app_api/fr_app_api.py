"""
Firmware Registry APP API calls
"""
import logging
import pprint

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class AppAPIClient(AppSession):
    """
    FirmwareRegistry App API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize ActivateInventory class
        :param host: cluster under test App api url
        :param sso_host: sso_host url
        :param client_id: App api client_id
        :param client_secret: App api client secret
        """
        log.info("Initializing Firmware Registry APP API Client for Api calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/firmware-registry/nb"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

    def _log_response(func):
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

    @_log_response
    def upload_firmware(self, firmware_payload):
        """
        Upload the Firmware
        :param firmware_payload: Firmware metadata
        :return: Response JSON
        """
        return self.post(
            self._get_path("firmware"),
            json=firmware_payload,
            ignore_handle_response=True,
        )

    @_log_response
    def update_firmware(self, firmware_id, payload):
        """
        Update the Firmware metadata
        :param firmware_id: ID of the firmware to be updated
        :param payload: Firmware metadata to be updated
        :return: Response JSON
        """
        return self.put(
            self._get_path(f"firmware/{firmware_id}"),
            json=payload,
            ignore_handle_response=True,
        )

    @_log_response
    def delete_firmware(self, firmware_id):
        """
        Delete the Firmware
        :param firmware_id: ID of the firmware to be deleted
        :return: Response JSON
        """
        return self.delete(
            self._get_path(f"firmware/{firmware_id}"), ignore_handle_response=True
        )

    @_log_response
    def get_firmwares(self, **params):
        """
        Search for the firmware
        :param params: Kwargs of the search query parameters
        :return: Response JSON
        """
        return self.get(
            self._get_path(f"search"), params=params, ignore_handle_response=True
        )

    @_log_response
    def search_firmwares(self, cbuild, **kwargs):
        """
        Cbuild search for the firmware
        :param cbuild: Cbuild value for the query
        :param kwargs: Kwargs of the search query parameters
        :return: Response JSON
        """
        return self.get(
            self._get_path(f"search/all/firmware/cbuild"),
            params={"cbuild": cbuild, **kwargs},
            ignore_handle_response=True,
        )

    @_log_response
    def get_firmware_operation_status(self, task_id):
        """
        Get the operational status of the task
        :param task_id: Task ID of the task (upload/update/delete)
        :return: Response JSON
        """
        return self.get(self._get_path(f"status/{task_id}"), ignore_handle_response=True)
