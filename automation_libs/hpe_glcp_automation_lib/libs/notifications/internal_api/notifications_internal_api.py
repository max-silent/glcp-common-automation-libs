"""
Notifications Service internal API Library
"""

import logging

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session
from hpe_glcp_automation_lib.libs.commons.utils.logs.logs import Logs

log = logging.getLogger(__name__)


class NotificationsInternalAPIClient(Session):
    """
    Notifications Service Internal API Client Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Activate Inventory for internal api calls")
        super(NotificationsInternalAPIClient, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "notifications-service.ccs-system.svc.cluster.local"
        self.base_path = "/notifications-svc/internal"
        self.api_version_v1alpha1 = "/v1alpha1"
        self.base_url = f"http://{self.host}"

    _log_response = Logs.log_response

    def _get_path_v1apha1(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version_v1alpha1}/{path}"

    @_log_response
    def create_notification(self, payload):
        """
        create_notification user api to create notification with payload
        :param payload: payload is json format of different parameters required
                        to create notification
                        example:
                        {
                            "ttl": Integer <epoch time format>,
                            "summary": String <summary of notification to be created>,
                            "description": String <description of Notification to be created>,
                            "severity": Integer <severity of notification 1:Critical, 2:Warning,
                                                 3:Ok, 4:Informational>,
                            "target": {
                                "type": String <target type like USERS, ACCOUNTS, PLATFORM, CENTRALS>,
                                "ids": List of Strings <target type ids>,
                            },
                            "channel": List of Strings <target channels like PORTAL, BANNER, EMAIL>
                        }
        """
        url_path = self._get_path_v1apha1("notifications")
        return self.post(url=f"{url_path}", json=payload)
