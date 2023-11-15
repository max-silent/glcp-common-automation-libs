"""
Notification UI API Library
"""
import logging

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession
from hpe_glcp_automation_lib.libs.commons.utils.logs.logs import Logs

log = logging.getLogger(__name__)


class Notifications(UISession):
    """
    Notification UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID
        """
        log.info("Initializing notification for user api calls")
        super().__init__(host, user, password, pcid)
        self.host = host
        self.pcid = pcid
        self.base_path = "/notifications-svc/ui"
        self.api_version = "/v1alpha1"

    _log_response = Logs.log_response

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

    @_log_response
    def get_session(self):
        """
        call the session api
        """
        return self.session.post(
            url=self._get_path("/session"),
            headers=self.session.session.headers,
            json=self.session.session.token_json,
        )

    @_log_response
    def get_status(self):
        """
        Get status of the Audit Trail service UI API
        :return: JSON object of the status
        """
        return self.get(self._get_path("status"), ignore_handle_response=True)

    @_log_response
    def get_notification_portal(self, query):
        """
        user api to get notifications from portal with query
        :param query: search param example : channel, limit etc.,.
        """
        url_path = self._get_path("notifications")
        return self.get(url=f"{url_path}?{query}", ignore_handle_response=True)

    @_log_response
    def update_timeline(self):
        """
        update-timeline user api to update user-timeline for
        latest notifications to display in portal
        """
        url_path = self._get_path("notifications/update-timeline")
        return self.post(url=f"{url_path}", ignore_handle_response=True)

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
        url_path = self._get_path("notifications")
        return self.post(url=f"{url_path}", json=payload)

    @_log_response
    def get_notification_by_id(self, notification_id):
        url_path = self._get_path("notifications/" + notification_id)
        return self.get(url=f"{url_path}", ignore_handle_response=True)
