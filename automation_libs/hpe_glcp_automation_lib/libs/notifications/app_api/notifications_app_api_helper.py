"""
    Notifications Service App API Helper
"""
import logging

from hpe_glcp_automation_lib.libs.notifications.app_api.notifications_app_api import (
    NotificationServiceAppApiClient,
)

log = logging.getLogger(__name__)


class NotificationsAppAPIHelper(NotificationServiceAppApiClient):
    """
    Notifications Service APP API Helper Class
    """

    def __init__(self, host, sso_host, client_id, client_secret, scope):
        log.info("Initializing Notifications Service Helper for APP Api calls")
        super().__init__(host, sso_host, client_id, client_secret, scope)
