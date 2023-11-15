"""
Authz Internal API
"""

import json
import logging

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class AuthzInternalApi(Session):
    """
    Authz Internal Session class
    """

    def __init__(self, **kwargs):
        log.info("Initializing local-authz for internal api calls")
        super().__init__(**kwargs)

        self.base_url = f"http://authz-svc.ccs-system.svc.cluster.local"

        self.base_path = "/authorization/internal/"
        self.api_version = "v1/"

    def _get_path(self, path, api_version=None):
        api_version = api_version if api_version else self.api_version
        return f"{self.base_path}{api_version}{path}"

    def get_roles_by_user_application(self, workspace, user, appid):
        """
        Get roles assigned to a user for a specific application in the given workspace.
        :param workspace: Workspace ID or customer ID.
        :param user: Username or user ID.
        :param appid: Application ID for which roles are to be retrieved.
        :return: The response from the API call, containing role data.
        """

        path = self._get_path(
            f"customers/{workspace}/users/{user}/application_roles?application_id={appid}"
        )
        url = f"{self.base_url}{path}"

        return self.get(url)

    def update_subject_assignments(self, workspaceId: str, payload):
        """
        Update roles assigned to a subject in the given Basic Organizations workspace.
        :param workspace: Workspace ID or customer ID in the Basic Organizations workspace.
        :param payload: A SubjectRoleUpdates object which contains subject info and updated assignments info.
        :return: Response object
        """
        path = self._get_path(f"Customers/{workspaceId}/assignments")
        return self.put(path, json=payload.dict(), tuple_response=True)

    def get_subject_assignments(
        self, workspaceId: str, subject_id: str, subject_type: str
    ):
        """
        Get roles assigned to a user group in the given Basic Organizations workspace.
        :param workspace: Workspace ID or customer ID.
        :param subject_id: Subject ID for which roles are to be retrieved.
        :param subject_type: Subject type of subject_id (USER or GROUP)
        :return: Response object
        """
        path = self._get_path(
            f"Customers/{workspaceId}/SubjectTypes/{subject_type}/Subjects/{subject_id}/assignments"
        )
        return self.get(path, tuple_response=True)

    def get_assignments_for_user(self, workspace_id, user_id):
        """
        Calls Authz Internal API to get roles assigned to a user in the given workspace.
        :param workspace_id: Workspace ID or customer ID.
        :param user_id: User ID
        :return: The response from the API call, containing assignments
        """
        return self.get(
            self._get_path(f"customers/{workspace_id}/users/{user_id}/role_assignments"),
            tuple_response=True,
        )

    def update_role_assignments_for_user(self, workspace_id, user_id, payload=None):
        """
        Calls Authz Internal API to update roles to a user in the given workspace.
        :param workspace_id: Workspace ID or customer ID.
        :param user_id: User ID
        :payload: role assignment payload
        :return: The response from the API call
        """
        return self.put(
            self._get_path(f"customers/{workspace_id}/users/{user_id}/roles"),
            data=json.dumps(payload),
            tuple_response=True,
        )

    def enforce_get(self, platform_cid, user_name, params):
        """
        Calls Authz Internal API for Get enforcement for user in given workspace
        :param platform_cid: Workspace ID or customer ID.
        :param user_id: Username or user ID.
        :param params: permission and resource being enforced for the user
        :return: The response from the API call, containing enforcement effect
        """
        return self.get(
            self._get_path(f"customers/{platform_cid}/users/{user_name}/enforce"),
            params=params,
            tuple_response=True,
        )

    def enforce_post(self, platform_cid, user_name, payload):
        """
        Calls Authz Internal API for Post enforcement for user in given workspace
        :param platform_cid: Workspace ID or customer ID.
        :param user_id: Username or user ID.
        :param payload: permission and resource being enforced for the user
        :return: The response from the API call, containing enforcement effect
        """
        return self.post(
            self._get_path(f"customers/{platform_cid}/users/{user_name}/enforce"),
            data=json.dumps(payload),
            tuple_response=True,
        )

    def enforce_batch_post(self, platform_cid, user_name, payload):
        """
        Calls Authz Internal API for Post batch enforcement for user in given workspace
        :param platform_cid: Workspace ID or customer ID.
        :param user_id: Username or user ID.
        :param payload: permissions and resources being enforced for the user
        :return: The response from the API call, containing enforcement effect
        """
        return self.post(
            self._get_path(f"customers/{platform_cid}/users/{user_name}/enforce_batch"),
            data=json.dumps(payload),
            tuple_response=True,
        )
