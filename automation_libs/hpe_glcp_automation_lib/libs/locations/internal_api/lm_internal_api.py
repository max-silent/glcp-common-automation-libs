"""
Location Management internal apis
"""

import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class LocationManagementInternal(Session):
    """
    LocationManagement Internal API Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Location Management for internal api calls")
        super(LocationManagementInternal, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "location-management-svc.ccs-system.svc.cluster.local"
        self.base_path = "/internal"
        self.api_version_v1 = "/v1"
        self.api_version_v2 = "/v2"
        self.base_url = f"http://{self.host}"

    def _get_path_v1(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version_v1}/{path}"

    def _get_path_v2(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version_v2}/{path}"

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

    def create_lm_location(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        location_request=None,
    ):
        """
        method to create a location in location management using internal api
        platform customer id is in the header of the request
        ccs username is in the header of the request
        :param transaction_id:
        :param platform_customer_id:
        :param username:
        :param location_request:
        :return:
        """
        headers = {
            "CCS-Transaction-ID": transaction_id,
            "CCS-Platform-Customer-Id": platform_customer_id,
            "CCS-Username": username,
            "Content-Type": "application/json",
        }
        self.session.headers.update(headers)

        log.info(
            f"Sending request to create location [platform id:{platform_customer_id}, request:{location_request}"
        )
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/locations"
        log.info(url)
        response = self.post(url=url, json=location_request, ignore_handle_response=True)
        log.info(f"Response of API request[tx:{platform_customer_id}]: {response}")
        return response

    def delete_location(
        self,
        transaction_id=None,
        platform_customer_id=None,
        username=None,
        location_id=None,
    ):
        """
        method to create a location in location management using internal api
        platform customer id is in the header of the request
        ccs username is in the header of the request
        :param transaction_id:
        :param platform_customer_id:
        :param username:
        :param location_id:
        :return:
        """
        headers = {
            "CCS-Transaction-ID": transaction_id,
            "CCS-Platform-Customer-Id": platform_customer_id,
            "CCS-Username": username,
            "Content-Type": "application/json",
        }
        self.session.headers.update(headers)

        log.info(
            f"Sending request to delete location [platform id:{platform_customer_id}, location_id:{location_id}"
        )
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/locations/{location_id}"
        log.info(url)
        response = self.delete(url=url, ignore_handle_response=True)
        log.info(f"Response of API request[tx:{platform_customer_id}]: {response}")
        return response
