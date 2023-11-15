"""
Async Handler Service Internal API's
"""
import inspect
import logging
import pprint
import uuid
from functools import wraps

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class AsyncHandlerServiceInternal(Session):
    """
    AsyncHandlerService Internal API Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing Async Handler Service for internal api calls")
        super(AsyncHandlerServiceInternal, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.host = "async-handler-service-svc.ccs-system.svc.cluster.local"
        self.base_path = "/async-handler/internal"
        self.api_version_v1 = "/v1"
        self.base_url = f"http://{self.host}"

    def _get_path_v1(self, path):
        return f"{self.base_path}{self.api_version_v1}/{path}"

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
        Get status of the Async Handler Service health check status
        :return: API Response obj
        """
        return self.get(url=self._get_path_v1("status"), ignore_handle_response=True)

    @_log_response
    def create_async_response(self, platform_customer_id, user_name, data):
        """
        Create async operation resource in Async-Handler-Service with Initial values and save the data in db

        :param platform_customer_id: Platform Customer Id
        :param user_name: Username
        :param data: Payload of the async request
        :return: API Response obj
        """

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Username": user_name,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        log.info("Session : {}".format(self.session.headers))
        return self.post(
            url=self._get_path_v1("async-operations"),
            json=data,
            ignore_handle_response=True,
        )

    @_log_response
    def get_async_response(self, task_id):
        """
        Get async operation resource in Async-handler-Service will get the values of the Async-Operation with or while
        polling on the identifier

        :param task_id: Identifier
        :return: API Response obj
        """

        self.session.headers.update(
            {
                "Accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        log.info("Session : {}".format(self.session.headers))
        return self.get(
            url=self._get_path_v1(f"async-operations/{task_id}"),
            ignore_handle_response=True,
        )

    @_log_response
    def patch_async_response(self, platform_customer_id, user_name, data, task_id):
        """
        Patch async operation resource in Async-Handler-Service with the values sent by client, and save in db

        :param platform_customer_id: Platform Customer Id
        :param user_name: Username
        :param task_id: Identifier
        :param data: Payload of the Patch Operation to be sent to modify
        :return: API Response obj
        """

        self.session.headers.update(
            {
                "CCS-Platform-Customer-Id": platform_customer_id,
                "CCS-Username": user_name,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        log.info("Session : {}".format(self.session.headers))
        return self.patch(
            url=self._get_path_v1(f"async-operations/{task_id}"),
            json=data,
            ignore_handle_response=True,
        )

    @_log_response
    def delete_async_response(self, task_id):
        """
        Delete async operation resource in Async-Handler-Service will delete the resource in db of the identifier

        :param task_id: Identifier
        :return: API Response obj
        """

        self.session.headers.update(
            {
                "Accept": "application/json",
                "CCS-Transaction-Id": f"{inspect.currentframe().f_code.co_name}_{uuid.uuid1().hex}",
            }
        )

        log.info("Session : {}".format(self.session.headers))
        return self.delete(
            url=self._get_path_v1(f"async-operations/{task_id}"),
            ignore_handle_response=True,
        )
