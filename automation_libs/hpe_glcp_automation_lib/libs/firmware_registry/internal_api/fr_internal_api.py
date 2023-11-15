import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class InternalAPIClient(Session):
    """
    Firmware Registry Internal API Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Firmware Registry for Internal Api calls")
        super(InternalAPIClient, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "firmware-registry-svc.ccs-system.svc.cluster.local"
        self.base_path = "/firmware-registry/internal"
        self.api_version = "/v1"
        self.base_url = f"http://{self.host}"

    def _get_path(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version}/{path}"

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

    @_log_response
    def get_all_firmwares_mode_oem(self, **params):
        """
        Search the firmwares by mode/oem/build/version
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_platform_id_from_name(self, **params):
        """
        Search the firmwares by platform name
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/platform/name"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_platform_id_from_part(self, **params):
        """
        Search the firmwares by part number
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/part/partnumber"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_all_firmwares_platform_oem(self, **params):
        """
        Search the firmwares by part/oem/build/version
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/platform/oem"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_current_firmware_part_oem(self, **params):
        """
        Search the firmwares by part/oem
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware/current"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_current_firmware_part_oem_version_build(self, **params):
        """
        Search the firmwares by part/oem/build/version
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware/current/version_build"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_all_firmwares_checksum_oem(self, **params):
        """
        Search the firmwares by checksum/oem
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware/checksum/oem"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_latest_firmwares(self, **params):
        """
        Search the latest firmware by part/oem
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware/latest"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_mandatory_firmwares(self, **params):
        """
        Get the mandatory firmware by part/oem
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/mandatory_upgrade_firmware"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_all_firmwares_bridge(self, **params):
        """
        Get all the firmwares through activate bridge
        :params params: Kwargs of the search query parameters
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware/bridge"),
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def get_all_firmwares_mnp(self, part_number):
        """
        Get the latest mnp firmware for partnumber
        :part_number: Part number
        :return: API Response obj
        """
        return self.get(
            self._get_path("search/all/firmware/mnp"),
            params={"part_number": part_number},
            ignore_handle_response=True,
        )
