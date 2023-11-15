"""
Authz App API
"""
import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class AuthzAppApi(AppSession):
    """
    Authz App API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        :param host: CCS App API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        """
        super(AuthzAppApi, self).__init__(host, sso_host, client_id, client_secret)
        log.info("Initializing authz for app api calls")
        self.base_url = "https://" + host
        self.base_path = "/authorization/app"
        self.api_version = "/v1"

    def _log_response(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            log.debug(f"{' '.join(func.__name__.title().split('_'))} API Request")
            res = func(*args, **kwargs)
            msg = (
                f"{' '.join(func.__name__.title().split('_'))} API Response"
                + "\n\n"
                + pprint.pformat(res)
                + "\n"
            )
            if res.json() is not None:
                msg += pprint.pformat(res.json()) + "\n"
            log.debug(msg)
            return res

        return decorated_func

    @_log_response
    def get_app_instance_metadata(self, application_instance_id):
        """
        Get the details of the app instance from Authz
        :param app_instance_id: Application Instance ID
        :return: Response object
        """
        return self.get(
            f"{self.base_path}{self.api_version}/application_instances/{application_instance_id}",
            ignore_handle_response=True,
        )

    @_log_response
    def onboard_app(self, app_instance_id, payload):
        """
        Onboard an app instance in Authz
        :param app_instance_id: Application Instance ID
        :payload: Details of the app to onboard -- see `payload.py`
        :return: Response object
        """
        return self.post(
            f"{self.base_path}{self.api_version}/application_instances/{app_instance_id}/onboard",
            json=payload,
            ignore_handle_response=True,
        )

    @_log_response
    def upgrade_app(self, app_instance_id, payload):
        """
        Upgrade an app instance in Authz
        :param app_instance_id: Application Instance ID
        :payload: Details of the app to upgrade -- see `payload.py`
        :return: Response object
        """
        return self.post(
            f"{self.base_path}{self.api_version}/application_instances/{app_instance_id}/upgrade",
            json=payload,
            ignore_handle_response=True,
        )

    def process_organization_events(self, orgs_event, headers):
        """
        Delete User/Group Assignments and Casbin Cache entries
        :param orgs_event: Details of the organization related event
        :return: Response object
        """
        return self.post(
            f"{self.base_path}{self.api_version}/events",
            json=orgs_event,
            headers=headers,
            tuple_response=True,
        )
