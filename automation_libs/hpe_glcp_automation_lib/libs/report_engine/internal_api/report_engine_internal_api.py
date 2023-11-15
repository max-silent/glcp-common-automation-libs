"""
Report Engine Internal API Library
"""
import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class ReportEngine(Session):
    """
    Report Engine Internal API Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing report_engine for internal api calls")
        super().__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.app_host = "http://report-engine-svc.ccs-system.svc.cluster.local:80"
        self.app_base_path = "/report-engine/app"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.host}{self.base_path}{self.api_version}/{path}"

    def _get_app_path(self, path):
        return f"{self.app_host}{self.app_base_path}{self.api_version}/{path}"

    def _log_response(func):
        @wraps(func)
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
    def health_check_status(self):
        """
        Get status of the Report Engine service health check status
        :return: JSON object of the status
        """
        # http://report-engine-svc.ccs-system.svc.cluster.local:80/report-engine/internal/v1/healthcheck
        return self.get(url=self._get_path("healthcheck"), ignore_handle_response=True)

    @_log_response
    def query_execute(self, payload):
        """
        Post API to get the data based on SQL query
        :param payload: SQL query
        :return: JSON object of api metadata
        """
        # http://report-engine-svc.ccs-system.svc.cluster.local:80/report-engine/internal/v1/query/execute
        # url = "https://report-engine-svc/report-engine/app/v1/query/execute"
        return self.post(
            url=self._get_app_path("query/execute"),
            json=payload,
            ignore_handle_response=True,
        )

    @_log_response
    def query_execute_async(self, payload):
        """
        Post API to get the data based on SQL query and upload the data to S3
        :param payload: SQL query including S3, emailID and kafka topic details
        :return: JSON object of api metadata
        """
        # http://report-engine-svc.ccs-system.svc.cluster.local:80/report-engine/internal/v1/query/execute-async
        # url = "https://report-engine-svc/report-engine/app/v1/query/execute-async"
        return self.post(
            url=self._get_app_path("query/execute-async"),
            json=payload,
            ignore_handle_response=True,
        )

    @_log_response
    def query_validate(self, payload):
        """
        Post API to get the data based on SQL query
        :param payload: SQL query
        :return: JSON object of api metadata
        """
        # http://report-engine-svc.ccs-system.svc.cluster.local:80/report-engine/internal/v1/query/validate
        # url = "https://report-engine-svc/report-engine/app/v1/query/validate"
        log.info(f"payload is {payload}")
        return self.post(
            url=self._get_app_path("query/validate"),
            json=payload,
            ignore_handle_response=True,
        )
