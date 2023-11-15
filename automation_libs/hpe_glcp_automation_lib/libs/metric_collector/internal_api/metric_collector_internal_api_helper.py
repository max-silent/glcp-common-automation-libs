"""
Metric Collector Service Internal API Helper
"""
import logging

from hpe_glcp_automation_lib.libs.metric_collector.internal_api.metric_collector_internal_api import (
    MetricCollectorInternalAPIClient,
)

log = logging.getLogger(__name__)


class MetricCollectorInternalApiHelper(MetricCollectorInternalAPIClient):
    """
    Metric Collector Service Internal API Helper Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Metric Collector Service Helper for internal api calls")
        super(MetricCollectorInternalApiHelper, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
