"""
Users page object model
"""
import logging

from automation.libs_local.authz.service_centric_ui.user_detail_page import UsersDetail
from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authz.ui.locators import UsersSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class Users(HeaderedPage):
    """
    Users page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Users page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Users page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/identity/users"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of users page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(
            UsersSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text, ensure_not_empty=True):
        """
        Enter text to search field.
        :param search_text: search_text.
        :param ensure_not_empty: defines either it's required to wait for non-empty table or not.
        :return: current instance of users page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' in users")
        self.pw_utils.enter_text_into_element(UsersSelectors.SEARCH_FIELD, search_text)
        if ensure_not_empty:
            self.wait_for_loaded_table()
        else:
            self.wait_for_loaded_state()
        return self

    def navigate_to_identity_and_access(self):
        """
        Return to the previous page.
        """
        log.info("Playwright: navigate back to identity and access page from users.")
        self.page.locator(UsersSelectors.BACK_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def navigate_to_user_detail(self, username):
        """Navigated to User Detail Page

        :param: username (required)
        return: User Detail Page
        """
        self.page.locator(UsersSelectors.TABLE_ROWS, has_text=username).first.click()
        return UsersDetail(self.page, self.cluster, username)

    def invite_user(self, user_email, role: str = "Observer"):
        """
        Invites the user in the users page

        :param user_email: user email which is to be invited
        :param role: user role to be assigned
        :return: current instance of users page object.
        """
        log.info(f"Playwright: Invite {user_email} with {role} role")
        self.page.locator(UsersSelectors.INVITE_USERS_BUTTON).click()
        self.page.locator(UsersSelectors.INVITE_USERS_EMAIL_FIELD).fill(user_email)
        self.page.locator(UsersSelectors.INVITE_USERS_ROLES_DROPDOWN).click()
        self.page.locator(UsersSelectors.INVITE_USERS_ROLE_TEMPLATE.format(role)).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(UsersSelectors.INVITE_USERS_SEND_INVITE_BTN).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def delete_user(self, user_email):
        """
        Deletes the user from the users page

        :param user_email: user email which is to be deleted
        :return: current instance of users page object
        """
        log.info(f"Playwright: Delete {user_email} user.")
        self.search_for_text(user_email)
        self.page.locator(
            UsersSelectors.TABLE_ACTION_BTN_TEMPLATE.format(user_email)
        ).click()
        self.page.locator(UsersSelectors.DELETE_BTN).click()
        self.page.locator(UsersSelectors.DELETE_CHECK_BTN).click()
        self.page.locator(UsersSelectors.DELETE_CONFIRM_BTN).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def assign_role(
        self,
        user_email,
        app_name,
        role_name,
        access_rule=None,
        limit_resource_access=False,
        rrp_name=None,
    ):
        """
        Assign role to users with application access

        :param user_email: assign role to user_email
        :param app_name: application name
        :param role_name: role name
        :param access_rule: access rule
        :param limit_resource_access: boolean
        :param rrp_name: resource restriction policy name
        :return: current instance of users page object
        """
        log.info(f"Playwright: Assign {role_name} role to {user_email}.")
        self.search_for_text(user_email)
        self.page.get_by_text(user_email).first.is_enabled()
        self.page.get_by_text(user_email).first.click()
        self.page.locator(UsersSelectors.ASSIGN_ROLE_BUTTON).click()
        self.pw_utils.select_drop_down_element(
            UsersSelectors.APPLICATIONS_SELECT_DROPDOWN,
            app_name,
            "option",
            exact_match=True,
        )
        self.page.locator(UsersSelectors.ROLES_DROPDOWN).click()
        self.page.locator(
            UsersSelectors.ROLES_DROPDOWN_OPT_TEMPLATE.format(role_name)
        ).click()

        if access_rule:
            self.pw_utils.select_drop_down_element(
                UsersSelectors.ACCESS_RULE_DROPDOWN,
                access_rule,
                "option",
            )

        if limit_resource_access:
            self.page.locator(UsersSelectors.RESOURCE_POLICY_TOGGLE).click()
            self.page.locator(UsersSelectors.RESOURCE_POLICY_DROPDOWN).click()
            if self.pw_utils.wait_for_selector(
                UsersSelectors.CLEAR_ALL_POLICY_BTN,
                state="visible",
                timeout_ignore=True,
            ):
                self.page.locator(UsersSelectors.CLEAR_ALL_POLICY_BTN).click()
            self.page.locator(
                UsersSelectors.RESOURCE_POLICY_OPT_TEMPLATE.format(rrp_name)
            ).click()
            self.page.locator(UsersSelectors.RESOURCE_POLICY_DROPDOWN).click()
        self.page.locator(UsersSelectors.ASSIGN_ROLE_BUTTON).last.click()
        self.page.locator(UsersSelectors.CHANGE_ROLE_BUTTON).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def unassign_role(self, user_email, app_name):
        """
        Unassign role to users with application access

        :param user_email: user email
        :param app_name: application name with which role is assigned
        :return: current instance of users page object
        """
        log.info(f"Playwright: Unassign {app_name} role for {user_email}.")
        self.search_for_text(user_email)
        self.page.get_by_text(user_email).first.is_enabled()
        self.page.get_by_text(user_email).first.click()
        self.page.wait_for_selector(
            UsersSelectors.TABLE_ACTION_BTN_TEMPLATE.format(app_name)
        )
        self.page.locator(
            UsersSelectors.TABLE_ACTION_BTN_TEMPLATE.format(app_name)
        ).first.click()
        self.page.locator(UsersSelectors.REMOVE_ROLE_OPT).click()
        self.page.locator(UsersSelectors.REMOVE_ROLE_BTN).click()
        self.page.wait_for_selector(UsersSelectors.NOTIFICATION_OK_CLOSE_BTN)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(UsersSelectors.NOTIFICATION_OK_CLOSE_BTN).click()
        return self

    def should_have_search_field(self):
        """
        Check that search field with expected placeholder is present on the page.
        :return: current instance of users page object.
        """
        log.info(f"Playwright: check search field is present at users.")
        search_field_locator = self.page.locator(UsersSelectors.SEARCH_FIELD)
        self.pw_utils.save_screenshot(self.test_name)
        expect(search_field_locator).to_be_visible()
        expect(search_field_locator).to_have_attribute("placeholder", "Search Users")
        return self

    def should_contain_text_in_table(self, text):
        """
        Check table contains row with expected text.
        :param text: the text to be displayed in table.
        :return: current instance of users page object.
        """
        log.info(f"Playwright: check that row with text '{text}' is present in table.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(UsersSelectors.TABLE_ROWS, has_text=text).first
        ).to_be_visible()
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of users page object.
        """
        log.info(
            f"Playwright: check that row with text '{value}' in column '{column_name}' is present in table."
        )
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(
            column_name, value
        )
        if not matching_rows_indices:
            raise ValueError(
                f"Not found rows with '{value}' value at '{column_name}' column."
            )
        expect(
            self.page.locator(
                UsersSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0])
            )
        ).to_be_visible()

        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of users page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(self.page.locator(UsersSelectors.TABLE_ROWS)).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def should_contain_text_in_title(self, text):
        """
        Check that expected text is present as part of the heading page title.
        :param text: expected text to be contained in title.
        :return: current instance of users page object.
        """
        log.info(f"Playwright: check that title contains text '{text}' in users page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(UsersSelectors.HEADING_PAGE_TITLE)).to_contain_text(text)
        return self

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of users page object.
        """
        log.info(f"Playwright: check that title has matched text '{text}' in users page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(UsersSelectors.HEADING_PAGE_TITLE)).to_have_text(text)
        return self

    def should_user_status_verified(self, user_email):
        """
        check if status of the invited user is shown as verified

        :param user_email: user email which was invited
        """
        self.search_for_text(user_email)
        selector = UsersSelectors.USER_STATUS_TEMPLATE.format(user_email, "VERIFIED")
        expect(self.page.locator(selector)).to_be_visible()
        return self

    def should_user_status_unverified(self, user_email):
        """
        check if status of the invited user is shown as unverified

        :param user_email: user email which was invited
        """
        self.search_for_text(user_email)
        selector = UsersSelectors.USER_STATUS_TEMPLATE.format(user_email, "UNVERIFIED")
        expect(self.page.locator(selector)).to_be_visible()
        return self

    def should_user_exists(self, user_email):
        """
        check if user exists in the table after invited

        :param user_email: user email which was invited
        """
        self.search_for_text(user_email)
        return self.page.get_by_text(user_email).first.is_enabled()