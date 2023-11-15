"""
Notifications Service Internal API Helper
"""
import logging

from hpe_glcp_automation_lib.libs.notifications.internal_api.notifications_internal_api import (
    NotificationsInternalAPIClient,
)

log = logging.getLogger(__name__)


class NotificationsInternalApiHelper(NotificationsInternalAPIClient):
    """
    Notifications Service Internal API Helper Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Notifications Service Helper for internal api calls")
        super(NotificationsInternalApiHelper, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
