"""
Audit-Tail NBAPI

"""
import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger()


class AuditTrailNBApiClient(AppSession):
    """
    Audit Trail NB API Client
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize Audit Trail class

        :param host: cluster under test NB api url
        :param sso_host: sso_host url
        :param client_id: App api client_id
        :param client_secret: App api client secret
        """
        log.info("Initializing Audit Trail NB API Client")
        super().__init__(host, sso_host, client_id, client_secret, scope="")
        self.base_url = f"https://{host}"
        self.base_path = "auditlogs"
        self.api_version = "v1beta1"

    def _get_path(self, path):
        log.info(f"_get_path: {self.base_url}/{self.base_path}/{self.api_version}/{path}")
        return f"{self.base_url}/{self.base_path}/{self.api_version}/{path}"

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
    def get_audit_logs(self, query_params=None):
        """
        Get the Audit Logs based on the search params(search API)
        :param query_params: Kwargs of the search query parameters defined by API spec(Optional). Following are the
        params
            app_cid: application customer id(optional)
            filter: the filter query combinations as per the api spec below(optional)
            select: the select query parameter for retrieving custom attributes in the response(optional)
            all: universal search param(optional)
            limit: items to return at one time (max 2000). Default value : 50(optional)
            offset: Specifies the zero-based resource offset to start the response from. Default 0(optional)
        :return: JSON response object
        API spec https://github.com/glcp/audit-trail/blob/mainline/api/v1beta1/audit-trail.yaml
        """
        return self.get(
            self._get_path(f"search"), params=query_params, ignore_handle_response=True
        )

    @_log_response
    def get_audit_log_details(self, audit_id, query_params=None):
        """
        Get the additional Audit Log details for the provided audit log id
        :param audit_id: Audit Log id(required)
        :param query_params: Kwargs of the query parameters defined by API spec(Optional). Following are the
        params
            application-customer-id: application customer id(optional)
        :return: JSON response object
        API Spec https://github.com/glcp/audit-trail/blob/mainline/api/v1beta1/audit-trail.yaml
        """
        return self.get(
            self._get_path(f"details/{audit_id}"),
            params=query_params,
            ignore_handle_response=True,
        )
