"""
Audit Trail UI API Library
"""
import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class AuditTrail(UISession):
    """
    Audit Trail UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing audit_trail for user api calls")
        super().__init__(host, user, password, pcid)
        self.host = host
        self.pcid = pcid
        self.base_path = "/auditlogs/ui"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

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
    def get_audit_logs(self, query):
        """
        Get audit logs of the Audit Trail service UI API based on query params
        :param query: query params for audit logs
        :return: JSON body of the list of audit logs
        """
        url_path = self._get_path("search")
        return self.get(url=f"{url_path}?{query}", ignore_handle_response=True)

    @_log_response
    def get_applications(self):
        """
        Get list of audit logs applications of the Audit Trail service UI API
        :return: JSON body of the list of applications
        """
        url_path = self._get_path("applications")
        return self.get(url=f"{url_path}", ignore_handle_response=True)

    @_log_response
    def get_categories(self, app_slug):
        """
        Get list of categories of the Audit Trail service UI API
        :param app_slug: app slug for whihc the categories need to be fetched
        :return: JSON body of the list of categories
        """
        url_path = self._get_path(app_slug + "/categories")
        return self.get(url=f"{url_path}", ignore_handle_response=True)

    @_log_response
    def get_audit_detail(self, index, audit_id):
        """
        Get details for audit logs of the Audit Trail service UI API
        :param index: index of the audit log
        :param audit_id: audit id of the audit log
        :return: JSON body of the list of audit logs
        """
        url_path = self._get_path("details")
        return self.get(
            url=f"{url_path}",
            params={"index": index, "audit_id": audit_id},
            ignore_handle_response=True,
        )

    @_log_response
    def post_audit_config(self, payload):
        """
        Set Audit log config details for apps
        :param payload: json formatted payload of different parameters required
        to apply the audit-trail configuration
        https://docs.ccs.arubathena.com/internal/audit-trail/#tag/UI-Api-AuditLogs/operation
        /application_configuration_auditlogs_ui_v1_configs_post
          Example: {"app_id":
            "516232d3-8378-40e5-b3af-20aa0de24781", "app_slug": "APCTFTB", "app_name": "App Catalog FT App B (US East)",
            "app_instance_id": "7747699d-50dd-4762-b095-6ab388401bad", "app_customer_id":
            "5983d2dafacc11ed9873620484f7861a", "app_audit_info": {"app_type": "CLOUD", "categories": ["API Gateway",
            "App Management", "Authorization", "Configuration", "Customer Management", "Saved Filters"],
            "dashboard_columns": {"default": ["Category", "Description", "IP Address", "Time", "Username", "Workspace
            Name"], "fixed": ["Category", "Time", "Description"], "all": ["Category", "Description", "Time",
            "IP Address", "Target", "server_name", "Workspace Name", "Username"]}, "order": {"Category": 0,
            "Description": 1, "Time": 7, "IP Address": 6, "Target": 4, "Username": 2, "server_name": 5, "Workspace
            Name": 3}}, "username": "ccsqa2020@gmail.com"}
        :return: JSON body containing App ID
        """
        url_path = self._get_path("configs")
        return self.post(url=f"{url_path}", json=payload, ignore_handle_response=True)

    @_log_response
    def get_audit_config(self, app_id):
        """
        Get Audit log config details for given application id
        :param app_id: Application ID of the app
        :return: JSON body containing Auditlog config data
                https://docs.ccs.arubathena.com/internal/audit-trail/#tag/UI-Api-AuditLogs/operation
                        /get_configs_auditlogs_ui_v1__app_slug_or_id__configs_get
        """
        url_path = self._get_path(app_id + "/configs")
        return self.get(url=f"{url_path}", ignore_handle_response=True)

    @_log_response
    def put_audit_config(self, payload):
        """
        Update Audit log config
        :param payload: json formatted payload of different parameters required to update the
        existing audit-trail configuration
        https://docs.ccs.arubathena.com/internal/audit-trail/#tag/UI-Api-AuditLogs
        /operation/application_configuration_auditlogs_ui_v1_configs_put
          Example: {"audit_id":
            "l1Tk_YkBJUaBfRzNtq6p", "config": {"app_id": "516232d3-8378-40e5-b3af-20aa0de24781", "app_slug": "APCTFTB",
            "app_name": "App Catalog FT App B (US East)", "app_instance_id": "7747699d-50dd-4762-b095-6ab388401bad",
            "app_customer_id": "5983d2dafacc11ed9873620484f7861a", "app_audit_info": {"app_type": "CLOUD", "categories":
            ["API Gateway", "App Management", "Authorization", "Configuration", "Customer Management"],
            "dashboard_columns": {"default": ["Category", "Description", "IP Address", "Time", "Username", "Workspace
            Name"], "fixed": ["Category", "Time", "Description"], "all": ["Category", "Description", "Time",
            "IP Address", "Target", "server_name", "Workspace Name", "Username"]}, "order": {"Category": 0,
            "Description": 1, "Time": 7, "IP Address": 2, "Target": 3, "Username": 6, "server_name": 4, "Workspace
            Name":
            5}}}}
        :return: JSON body containing App ID
        """
        url_path = self._get_path("configs")
        return self.put(url=f"{url_path}", json=payload, ignore_handle_response=True)

    @_log_response
    def delete_audit_config(self, audit_id, payload):
        """
        Delete Audit log config details
        :param audit_id: audit ID to be deleted
        :param payload: json formatted payload of different parameters required to delte the
                        existing audit-trail configuration
                        https://docs.ccs.arubathena.com/internal/audit-trail/#tag/UI-Api-AuditLogs
                        /operation/application_configuration_auditlogs_ui_v1_configs__audit_id__delete
          Example: {"app_customer_id": "5983d2dafacc11ed9873620484f7861a",
                    "username": "ccsqa2020@gmail.com"}
        :return: JSON body containing deleted audit id
        """
        url_path = self._get_path("configs/" + audit_id)
        return self.delete(url=f"{url_path}", json=payload, ignore_handle_response=True)
