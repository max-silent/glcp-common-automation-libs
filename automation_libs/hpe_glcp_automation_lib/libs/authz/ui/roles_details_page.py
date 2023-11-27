"""
Roles Details page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authz.ui.locators import RolesSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class RolesDetails(HeaderedPage):
    """
    Roles Details page object model class.
    """

    def __init__(self, page: Page, cluster: str, app_id: str, slug_id: str):
        log.info("Initialize Roles view page object")
        super().__init__(page, cluster)
        self.url = (
            f"{cluster}/manage-account/identity/roles/roleviewedit/{app_id}/{slug_id}"
        )

    def edit_custom_role_permission(self, resource_name, permission_type, action):
        """
        Edit permission in the custom role.
        :param resource_name: resource name for adding permissions
        :param permission_type: type of permission ( EDIT/ VIEW / DELETE )
        :param action: add or remove the permission (ADD / REMOVE)
        :return: current instance of roles details page object.
        """
        log.info(
            f"Playwright: Edit custom role permission : '{resource_name}' in edit permission page."
        )
        self.page.locator(RolesSelectors.EDIT_CUSTOM_ROLE_PERMISSION_BUTTON).click()
        self.page.locator(RolesSelectors.ADD_PERMISSIONS_BTN).click()
        self.page.wait_for_selector(RolesSelectors.PERMISSION_DIALOG_TITLE)
        self.page.locator(
            RolesSelectors.RESOURCE_NAME_TEMPLATE.format(resource_name)
        ).click()
        if action == "ADD":
            self.add_permission_to_custom_role(permission_type)
        if action == "REMOVE":
            self.remove_permission_from_custom_role(permission_type)
        self.page.locator(RolesSelectors.ADD_PERMISSION_BUTTON).click()
        self.page.locator(RolesSelectors.SAVE_PERMISSION_BUTTON).click()
        return self

    def add_permission_to_custom_role(self, permission_type):
        """
        add  permission in the custom role.
        :param permission_type: type of permission ( Edit/ View / Delete )
        :return: current instance of roles details page object.
        """
        log.info(
            f"Playwright: Add  '{permission_type}' permission to custom role in edit permission page."
        )
        if self.page.locator(
            RolesSelectors.PERMISSION_CHECKBOX_TICKED.format(permission_type)
        ).is_hidden():
            self.page.locator(
                RolesSelectors.RESOURCE_OPT_TEMPLATE.format(permission_type)
            ).click()
        return self

    def remove_permission_from_custom_role(self, permission_type):
        """
        remove  permission in the custom role.
        :param permission_type: type of permission ( Edit/ View / Delete )
        :return: current instance of roles details page object.
        """
        log.info(
            f"Playwright: Remove  '{permission_type}' permission from custom role in edit permission page."
        )
        if self.page.locator(
            RolesSelectors.PERMISSION_CHECKBOX_TICKED.format(permission_type)
        ).is_visible():
            self.page.locator(
                RolesSelectors.RESOURCE_OPT_TEMPLATE.format(permission_type)
            ).click()
        return self
