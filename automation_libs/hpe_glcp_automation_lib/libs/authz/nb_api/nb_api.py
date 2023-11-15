"""
Authz NB API
"""
import logging
import pprint
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.unified_api.unified_api import UnifiedSession

log = logging.getLogger(__name__)


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


class NBAPISession(UnifiedSession):
    """
    Authz NB API Session Class.
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        :param app_api_host: CCS Unified API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        """
        log.info("Initializing unified api session for NB API calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/authorization"
        self.api_version = "/v1alpha1"
        self.nbapi_base_url = f"{self.base_url}{self.base_path}{self.api_version}"

    @_log_response
    def get_roles(self, application_id: str, **kwargs):
        """
        Get roles per application
        """

        url = f"{self.nbapi_base_url}/applications/{application_id}/roles"
        response = self.get(url=url, tuple_response=True, **kwargs)
        return response

    @_log_response
    def get_role(self, application_id: str, role_id: str, **kwargs):
        """
        Get role by id
        """

        url = f"{self.nbapi_base_url}/applications/{application_id}/roles/{role_id}"
        response = self.get(url=url, tuple_response=True, **kwargs)
        return response

    @_log_response
    def delete_role(self, application_id: str, role_id: str, **kwargs):
        """
        Delete role by id
        """

        url = f"{self.nbapi_base_url}/applications/{application_id}/roles/{role_id}"
        response = self.delete(url=url, tuple_response=True, **kwargs)
        return response

    @_log_response
    def get_role_assignments_per_user_id(self, subject_grn: str, **kwargs) -> tuple:
        """
        Get role assignments by subject grn.

        :param subject_grn: The subject's Global Resource Name (GRN).
        :type subject_grn: str
        Example: "grn:glp/organizations/0000-0000-0000-0000/workspaces/456/users/789"

        :return: A tuple containing the HTTP status code and API response.
        :rtype: tuple
        """

        url = f"{self.nbapi_base_url}/assignments?subject-id={subject_grn}"
        return self.get(url=url, tuple_response=True, **kwargs)

    @_log_response
    def assign_role_to_user(
        self, application_id: str, request_data: dict, **kwargs
    ) -> tuple:
        """
        Assign a role to a subject.

        :param application_id: The ID of the application.
        :type application_id: str
        Example: "00000000-0000-0000-0000-000000000000"

        :param request_data: The data specifying the role assignment.
        :type request_data: dict
        Example: {
            "roleId": "ccs.observer",
            "subjectId": "grn:glp/organizations/0000-0000-0000-0000/workspaces/456/users/789",
        }

        :return: A tuple containing the HTTP status code and API response.
        :rtype: tuple
        """

        url = f"{self.nbapi_base_url}/applications/{application_id}/assignments"
        return self.post(url=url, json=request_data, tuple_response=True, **kwargs)

    @_log_response
    def delete_user_role_assignment(
        self, application_id: str, role_id: str, subject_grn: str, **kwargs
    ) -> tuple:
        """
        Delete a role assignment for a subject.

        :param application_id: The ID of the application.
        :type application_id: str
        Example: "00000000-0000-0000-0000-000000000000"

        :param role_id: The ID of the role.
        :type role_id: str
        Example: "ccs.account-admin"

        :param subject_grn: The subject's Global Resource Name (GRN).
        :type subject_grn: str
        Example: "grn:glp/organizations/0000-0000-0000-0000/workspaces/456/users/789"

        :return: A tuple containing the HTTP status code and API response.
        :rtype: tuple
        """

        url = (
            f"{self.nbapi_base_url}/applications/{application_id}/roles/"
            f"{role_id}/assignments?subject-id={subject_grn}"
        )
        return self.delete(url=url, tuple_response=True, **kwargs)
