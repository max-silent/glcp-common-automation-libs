import logging

from hpe_glcp_automation_lib.libs.async_handler_service.internal_api.async_internal_api import (
    AsyncHandlerServiceInternal,
)

log = logging.getLogger(__name__)


class AsyncHandlerServiceInternalApiHelper(AsyncHandlerServiceInternal):
    """
    AsyncHandlerService Internal API Helper Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing AsyncHandler Service Helper for internal api calls")
        super(AsyncHandlerServiceInternalApiHelper, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
