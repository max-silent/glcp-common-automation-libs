"""
Metric Collector Service internal API Library
"""

import logging

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session
from hpe_glcp_automation_lib.libs.commons.utils.logs.logs import Logs

log = logging.getLogger(__name__)


class MetricCollectorInternalAPIClient(Session):
    """
    Metric Collector Service Internal API Client Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Metric Collector for internal api calls")
        super(MetricCollectorInternalAPIClient, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "metric-collector-svc.ccs-system.svc.cluster.local"
        self.base_path = "/metric-collector/internal"
        self.api_version_v1alpha1 = "/v1"
        self.base_url = f"http://{self.host}"

    _log_response = Logs.log_response

    def _get_health_path(self, path):
        return f"{self.base_url}/{path}"

    def _get_path_v1(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version_v1alpha1}/{path}"

    @_log_response
    def get_healthz(self):
        """
        Metric collector healthz api to find the health of the service
        """
        url_path = self._get_health_path("healthz")
        log.info(f"Running healthz - URL: {url_path}")
        return self.get(
            url=f"{url_path}",
            ignore_handle_response=True,
        )

    @_log_response
    def get_readyz(self):
        """
        Metric collector readyz api to find the readiness of the service
        """
        url_path = self._get_health_path("readyz")
        log.info(f"Running readyz - URL: {url_path}")
        return self.get(
            url=f"{url_path}",
            ignore_handle_response=True,
        )

    @_log_response
    def run_invoke(self, headers):
        """
        Metric collector invoke api to trigger file upload to s3 based on headers inputs like service and filename
        """
        url_path = self._get_path_v1("invoke")
        log.info(f"Running invoke - URL: {url_path}")
        return self.post(
            url=f"{url_path}",
            headers=headers,
            ignore_handle_response=True,
        )

    @_log_response
    def get_invoke_status(self, headers):
        """
        Metric collector api to get invoke status to check if the service invoked is in ready state
        """
        url_path = self._get_path_v1("invoke/status")
        log.info(f"Running invoke status - URL: {url_path}")
        return self.get(
            url=f"{url_path}",
            headers=headers,
            ignore_handle_response=True,
        )

    @_log_response
    def list_files(self, params):
        """
        Metric collector list api to get the list of files from s3 based on folder name
        """
        url_path = self._get_path_v1("files/list")
        log.info(f"Running list - URL: {url_path}")
        return self.get(
            url=f"{url_path}",
            params=params,
            ignore_handle_response=True,
        )

    @_log_response
    def delete_files(self, headers):
        """
        Metric collector delete api to delete the files from s3 based on folder name
        """
        url_path = self._get_path_v1("delete")
        log.info(f"Running delete - URL: {url_path}")
        return self.delete(
            url=f"{url_path}",
            headers=headers,
            ignore_handle_response=True,
        )
