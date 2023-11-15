"""
Users page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authz.service_centric_ui.locators import (
    UserDetailSelectors,
)
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.headered_page import (
    HeaderedPage,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class UsersDetail(HeaderedPage):
    """
    Users page object model class.
    """

    def __init__(self, page: Page, cluster: str, email: str):
        """
        Initialize Users page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Users page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/identity/users/{email}"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page
        :return: current instance of audit log page object
        """
        log.info("Playwright: wait for table is loaded.")
        self.page.wait_for_selector(
            UserDetailSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def assign_role(self, manager, role):
        """
        Assign a Role to user
        param : manager (text) (required)
        param : role (text) (required)
        returns : self reference
        """
        log.info(f"Playwright: assign '{role}' role for '{manager}'.")
        if not self.table_utils.get_rows_indices_by_text_in_column(
            column_name="Role", column_text=role
        ):
            self.pw_utils.click_selector(UserDetailSelectors.ASSIGN_ROLE_BTN)
            self.pw_utils.click_selector(UserDetailSelectors.USER_APPLICATION_DROPDOWN)
            self.page.wait_for_load_state("domcontentloaded")
            self.page.locator(UserDetailSelectors.APPLICATION_DROP_DOWN).locator(
                "button", has_text=manager
            ).first.click()
            self.pw_utils.click_selector(UserDetailSelectors.INVITE_USERS_ROLES_DROPDOWN)
            self.pw_utils.click_selector(
                UserDetailSelectors.USER_ROLE_OPTION_TEMPLATE.format(role)
            )
            self.page.locator(UserDetailSelectors.ASSIGN_ROLE_BTN).nth(0).click()
            self.pw_utils.click_selector(UserDetailSelectors.CHANGE_ROLE_BUTTON)
            self.shoud_have_notification_assign_role(role)
        else:
            log.info("User role Already exist!")

        return self

    def shoud_have_notification_assign_role(self, name="Observer"):
        """
        Check User Name is available on notification modal
        param : name (text) (required)
        returns :  self reference
        """
        log.info(f"Playwright: check that title has {name} in Notification")
        self.page.wait_for_load_state("domcontentloaded")
        expect(
            self.page.locator(UserDetailSelectors.NOTIFICATION_TOAST_TEXT).locator(
                "strong"
            )
        ).to_contain_text(name)
        return self
