"""
Audit Trail APP API Client
"""
import logging
import pprint

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class AuditTrailAppApiClient(AppSession):
    """
    Audit Trail App API Client
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize Audit Trail class

        :param host: cluster under test App api url
        :param sso_host: sso_host url
        :param client_id: App api client_id
        :param client_secret: App api client secret
        """
        log.info("Initializing Audit Trail APP API Client for Api calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/auditlogs/app"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

    def _log_response(func):
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
    def publish(self, payload):
        """
        Publish Audit Log
        :param payload: Audit Log payload
        :return: Response JSON
        """
        return self.post(
            self._get_path("publish"),
            data=payload,
            ignore_handle_response=True,
        )

    def get_app_specific_audit_log_configurations(self, params=None):
        """
        Retrieve application specific audit log configurations
        Params: params
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/configs"
            log.debug(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.debug(f"response of application specific audit log configurations: {res}")
            return res
        except:
            log.error(
                "\nException in while getting application specific audit log configurations \n"
            )
