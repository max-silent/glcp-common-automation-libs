"""
Users page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authz.ui.locators import UserDetailSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class UsersDetail(HeaderedPage):
    """
    User Detail page object model class.
    """

    def __init__(self, page: Page, cluster: str, email: str):
        """
        Initialize User Detail page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize User Detail page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/identity/users/{email}"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty
        :return: current instance of user details page object
        """
        log.info("Playwright: wait for table is loaded.")
        self.page.wait_for_selector(
            UserDetailSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def assign_role(
        self,
        app_name,
        role_name,
        access_rule=None,
        limit_resource_access=False,
        rrp_name=None,
    ):
        """
        Assign role to users with application access

        :param app_name: application name
        :param role_name: role name
        :param access_rule: access rule
        :param limit_resource_access: boolean
        :param rrp_name: resource restriction policy name
        :return: current instance of users detail page object
        """
        log.info(f"Playwright: Assign {role_name} role.")
        self.page.locator(UserDetailSelectors.ASSIGN_ROLE_BTN).click()
        self.pw_utils.select_drop_down_element(
            UserDetailSelectors.USER_APPLICATION_DROPDOWN,
            app_name,
            "option",
            exact_match=True,
        )
        self.page.locator(UserDetailSelectors.USER_ROLES_DROPDOWN).click()
        self.page.get_by_role("searchbox").type(role_name, delay=100)
        self.page.locator(
            UserDetailSelectors.USER_ROLE_OPTION_TEMPLATE.format(role_name)
        ).click()
        if access_rule:
            self.pw_utils.select_drop_down_element(
                UserDetailSelectors.ACCESS_RULE_DROPDOWN,
                access_rule,
                "option",
            )
        if limit_resource_access:
            self.page.locator(UserDetailSelectors.RESOURCE_POLICY_TOGGLE).click()
            self.page.locator(UserDetailSelectors.RESOURCE_POLICY_DROPDOWN).click()
            self.page.locator(
                UserDetailSelectors.RESOURCE_POLICY_OPT_TEMPLATE.format(rrp_name)
            ).click()
            self.page.locator(UserDetailSelectors.RESOURCE_POLICY_DROPDOWN).click()
        self.page.locator(UserDetailSelectors.POPUP_ASSIGN_ROLE_BUTTON).click()
        self.page.locator(UserDetailSelectors.CHANGE_ROLE_BUTTON).click()
        self.page.wait_for_selector(UserDetailSelectors.ASSIGNED_ROLE_NOTIFICATION)
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def remove_role(self, role, app_name, resource_access=None):
        """
        Remove Role for User
        param : role (text) (required)
        param : app_name (text) (required)
        param : resource_access (text) (optional)
        returns : self reference
        """
        log.info(f"Playwright: remove '{role}' role.")
        params = {"Role": role, "Application": app_name}
        if resource_access:
            params["Resource Access"] = resource_access
        self.wait_for_loaded_table()
        matched_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(
            params
        )
        if not matched_rows_indices:
            raise ValueError(f"Missed role with specified details: '{params}'.")
        self.page.locator(UserDetailSelectors.ROLE_ACTIONS_BTN).nth(
            matched_rows_indices[0] - 1
        ).click()  # index of nth() starts from 0.
        self.page.locator(UserDetailSelectors.REMOVE_ROLE_OPT).click()
        self.page.locator(UserDetailSelectors.REMOVE_ROLE_BTN).click()
        self.page.wait_for_selector(UserDetailSelectors.REMOVED_ROLE_NOTIFICATION)
        return self

    def should_not_have_role_actions(self):
        """
        Check absence of role actions buttons.
        :return: current instance of users detail page object.
        """
        log.info("Playwright: check the absence of role actions buttons.")
        expect(
            self.page.locator(UserDetailSelectors.ROLE_ACTIONS_BTN)
        ).not_to_be_visible()
        return self

    def should_have_role_actions(self, role, app_name, action, resource_access=None):
        """
        Check the presence of role actions button
        param : role (text) (required)
        param : app_name (text) (required)
        param : action (text) (required)
        param : resource_access (text) (optional)
        returns : self reference
        """
        log.info(f"Playwright: check the presence of '{action}' action button.")
        role_details = {"Role": role, "Application": app_name}
        if resource_access:
            role_details["Resource Access"] = resource_access
        self.wait_for_loaded_table()
        row_index = self.table_utils.get_rows_indices_by_values_in_columns(role_details)
        if row_index:
            self.page.locator(UserDetailSelectors.ROLE_ACTIONS_BTN).nth(
                row_index[0] - 1
            ).click()
        expect(
            self.page.locator(UserDetailSelectors.ROLE_ACTION_BTN_TEMPLATE.format(action))
        ).to_be_visible()
        return self

    def should_not_have_user_actions(self):
        """
        Check absence of user actions button.
        :return: current instance of users detail page object.
        """
        log.info("Playwright: check the absence of actions button in user detail page")
        expect(
            self.page.locator(UserDetailSelectors.USER_ACTIONS_BUTTON)
        ).not_to_be_visible()
        return self

    def should_have_user_actions(self):
        """
        Checking the presence of actions button
        :return: current instance of users detail page object.
        """
        log.info("Playwright: check the presence of actions button in user detail page")
        expect(self.page.locator(UserDetailSelectors.USER_ACTIONS_BUTTON)).to_be_visible()
        return self

    def should_not_have_assign_role_button(self):
        """
        Check absence of assign role button.
        :return: current instance of users detail page object.
        """
        log.info("Playwright: Checking the absence of assign role button")
        expect(
            self.page.locator(UserDetailSelectors.ASSIGN_ROLE_BUTTON)
        ).not_to_be_visible()
        return self

    def should_have_assign_role_btn(self):
        """
        Checking the presence of assign role button
        :return: current instance of users detail page object.
        """
        log.info("Playwright: Checking the presence of assign role button")
        expect(self.page.locator(UserDetailSelectors.ASSIGN_ROLE_BTN)).to_be_visible()
        return self

    def should_have_notification_assign_role(self, name):
        """
        Check Username is available on notification modal
        param : name (text) (required)
        returns :  self reference
        """
        log.info(f"Playwright: check that title has {name} in Notification")
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(UserDetailSelectors.NOTIFICATION_OK)).to_contain_text(
            name
        )
        return self

    def should_have_role(self, application_name, role):
        """
        checking the role presence
        param: application_name
        param: role
        """
        log.info(f"Playwright: Checking {application_name} for {role}")
        expect(
            self.page.locator(
                UserDetailSelectors.CHECK_ROLE.format(application_name, role)
            )
        ).to_be_visible()
        return self

    def should_have_action_dropdown(self):
        """
        Checks for action dropdown ellipsis icon in user detail page
        returns :  self reference
        """
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(UserDetailSelectors.ACTION_DROPDOWN)).to_be_visible()
        return self
