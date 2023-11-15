"""
Notifications Service UI API Client
"""
import logging

from hpe_glcp_automation_lib.libs.notifications.user_api.notifications_ui_api import (
    Notifications,
)

log = logging.getLogger(__name__)


class NotificationsUIAPIHelper(Notifications):
    """
    Notifications Service UI API Helper Class
    """

    def __init__(self, host, user, password, pcid):
        log.info("Initializing Notifications Service UI API Helper for UI Api calls")
        super().__init__(host, user, password, pcid)
