import logging

from hpe_glcp_automation_lib.libs.firmware_registry.internal_api.fr_internal_api import (
    InternalAPIClient,
)

log = logging.getLogger(__name__)


class InternalApiHelper(InternalAPIClient):
    """
    Firmware Registry Internal API Helper Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Firmware Registry Helper for Internal Api calls")
        super(InternalApiHelper, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )

    def invoke_get_platform_id_from_name(self, name, limit=None, offset=None):
        """
        Search the firmwares by platform name
        :param name: Platform name
        :param limit: Limit for the pagination
        :param offset: Offset for the pagination
        :return: JSON response
        """
        params = dict(name=name)
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self.get_platform_id_from_name(**params)
