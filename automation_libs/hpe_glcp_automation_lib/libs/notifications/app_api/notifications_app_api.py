"""
Notifications Service APP API Library
"""
import logging

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession
from hpe_glcp_automation_lib.libs.commons.utils.logs.logs import Logs

log = logging.getLogger(__name__)


class NotificationServiceAppApiClient(AppSession):
    """
    Notifications Service App API Client
    """

    def __init__(self, host, sso_host, client_id, client_secret, scope):
        """
        Initialize Notifications Service App API class
        :param host: cluster under test App api url
        :param sso_host: sso_host url
        :param client_id: App api client_id
        :param client_secret: App api client secret
        :param scope: scope of the client creds
        """
        log.info("Initializing Audit Trail APP API Client for Api calls")
        super().__init__(host, sso_host, client_id, client_secret, scope)
        self.base_path = "/notifications-svc/app"
        self.api_version = "/v1alpha1"

    _log_response = Logs.log_response

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

    @_log_response
    def create_notification(self, payload):
        url_path = self._get_path("notifications")
        return self.post(url=f"{url_path}", json=payload)
