"""
Role details page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authz.ui.locators import RoleDetailsSelectors
from hpe_glcp_automation_lib.libs.authz.ui.user_data import RoleDetailsData
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class RoleDetails(HeaderedPage):
    """
    Roles details page object model class.
    """

    def __init__(self, page: Page, cluster: str, app_id: str, role_id: str):
        """
        Initialize Roles page object.
        :param page: page.
        :param cluster: cluster url.
        :param app_id: application uuid.
        :param role_id: role uuid/slug.
        """
        log.info("Initialize Roles page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = (
            f"{cluster}/manage-account/identity/roles/roleviewedit/{app_id}/{role_id}"
        )

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of roles page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.page.wait_for_selector(
            RoleDetailsSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.wait_for_loaded_state()
        return self

    def navigate_to_roles_and_permissions(self):
        """
        Return to the previous page.
        """
        log.info(f"Playwright: navigate back to identity and access page from roles.")
        self.page.locator(RoleDetailsSelectors.BACK_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def edit_role_details(self, role_data: RoleDetailsData = RoleDetailsData):
        """
        Edit custom role details.
        :param role_data: role data for editing the role (name and description)
        :return: current instance of role details page object.
        """
        log.info("Playwright: edit role details")
        self.pw_utils.click_selector(RoleDetailsSelectors.EDIT_BTN)
        self.page.locator(RoleDetailsSelectors.EDIT_NAME_INPUT_BOX).fill(role_data.role)
        self.page.locator(RoleDetailsSelectors.EDIT_DESC_INPUT_BOX).fill(
            role_data.description
        )
        self.pw_utils.click_selector(RoleDetailsSelectors.EDIT_ROLES_SAVE_BTN)
        self.pw_utils.save_screenshot(self.test_name)
        return self
