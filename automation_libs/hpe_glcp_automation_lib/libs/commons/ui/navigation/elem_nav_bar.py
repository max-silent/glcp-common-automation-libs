"""
Navigation bar page element
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.locators import NavBarSelectors
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class NavigationBar:
    """
    Navigation bar page element class
    """

    def __init__(self, page: Page):
        """
        Initialize instance of page navigation
        :param page: page
        """
        self.pw_utils = PwrightUtils(page)
        self.page = page

    def navigate_to_home(self):
        """
        Navigate to home page.
        """
        log.info("Navigate to home page.")
        self.page.click(NavBarSelectors.MENU_BTN_HOME)

    def navigate_to_dashboard(self):
        """
        *** NOTE *** This method is deprecated and will be removed, instead please use navigate_to_home().
        Navigate to dashboard home page.
        """
        self.navigate_to_home()

    def navigate_to_services(self):
        """
        Navigate to services page.
        """
        log.info("Navigate to services page.")
        self.page.click(NavBarSelectors.MENU_BTN_SERVICES)

    def navigate_to_applications(self):
        """
        *** NOTE *** This method is deprecated and will be removed, instead please use navigate_to_services().
        Navigate to applications page.
        """
        self.navigate_to_services()

    def navigate_to_devices(self):
        """
        Navigate to devices page.
        """
        log.info("Navigate to devices page.")
        self.page.click(NavBarSelectors.MENU_BTN_DEVICES)

    def navigate_to_customers(self):
        """
        Navigate to customers page (in case of MSP account)
        """
        log.info("Navigate to customers page")
        self.page.click(NavBarSelectors.MENU_BTN_CUSTOMERS)

    def navigate_to_notifications(self):
        """
        Navigate to notifications page
        """
        self.page.click(NavBarSelectors.NOTIFICATIONS_BUTTON)

    def logout(self):
        """
        Logout of the account via header's user menu.
        """
        log.info("Logout from current page.")
        self._open_user_menu()
        self.page.locator(NavBarSelectors.SIGNOUT_MENU_ITEM).click()
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_user_profile(self):
        """
        Navigates to user profile page
        """
        log.info("Navigating to User Profile page")
        self._open_user_menu()
        self.page.locator(NavBarSelectors.ACCOUNT_DETAILS_MENU_ITEM).click()

    def navigate_preferences(self):
        """
        Navigates to user preferences page
        """
        log.info("Navigating to User Preferences page")
        self._open_user_menu()
        self.page.locator(NavBarSelectors.PREFERENCES_MENU_ITEM).click()

    def navigate_support_documentation(self):
        """Navigates to online support documentation page.
        NOTE: navigated page is opened in separate tab. Use <playwright_page> instance, returned by this method,
        according to the following scenario:
            1. Instantiate 'SupportCenter' page-object class: 'support_page = SupportCenter(<playwright_page>)'
            2. Use methods from 'SupportCenter' class for required actions, e.g.: 'support_page.should_have_title()'
            3.Close tab, related to support documentation page: '<playwright_page>.close()'
            4. When browser context closed after test completion - attach recorded video to allure report:
                path = <playwright_page>.video.path()
                allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
        :return: Playwright's Page instance related to the new opened tab.
        """
        log.info("Navigating to Support documentation page")
        self._open_help_menu()
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(NavBarSelectors.DOCUMENTATION_MENU_ITEM).click()
        return new_page_info.value

    def navigate_billing_support(self):
        """Navigates to Billing, Metering and Subscription Page.
        NOTE: navigated page is opened in separate tab. Use <playwright_page> instance, returned by this method,
        according to the following scenario:
            1. Instantiate 'SupportCenter' page-object class: 'support_page = SupportCenter(<playwright_page>)'
            2. Use methods from 'SupportCenter' class for required actions, e.g.: 'support_page.should_have_title()'
            3.Close tab, related to support documentation page: '<playwright_page>.close()'
            4. When browser context closed after test completion - attach recorded video to allure report:
                path = <playwright_page>.video.path()
                allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
        :return: Playwright's Page instance related to the new opened tab.
        """
        log.info("Navigating to Billing, Metering and Subscription Page")
        self._open_help_menu()
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(NavBarSelectors.BILLING_MENU_ITEM).click()
        return new_page_info.value

    def navigate_workspace_user_onboarding_support(self):
        """Navigates to Workspace User Onboarding Support Page.
        NOTE: navigated page is opened in separate tab. Use <playwright_page> instance, returned by this method,
        according to the following scenario:
            1. Instantiate 'SupportCenter' page-object class: 'support_page = SupportCenter(<playwright_page>)'
            2. Use methods from 'SupportCenter' class for required actions, e.g.: 'support_page.should_have_title()'
            3.Close tab, related to support documentation page: '<playwright_page>.close()'
            4. When browser context closed after test completion - attach recorded video to allure report:
                path = <playwright_page>.video.path()
                allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
        :return: Playwright's Page instance related to the new opened tab.
        """
        log.info("Navigating to Workspace User Onboarding Support Page")
        self._open_help_menu()
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(NavBarSelectors.WORKSPACE_MENU_ITEM).click()
        return new_page_info.value

    def navigate_view_cases(self):
        """Navigates to View cases Page.
        NOTE: navigated page is opened in separate tab. Use <playwright_page> instance, returned by this method,
        according to the following scenario:
            1. Instantiate 'SupportCenter' page-object class: 'support_page = SupportCenter(<playwright_page>)'
            2. Use methods from 'SupportCenter' class for required actions, e.g.: 'support_page.should_have_title()'
            3.Close tab, related to support documentation page: '<playwright_page>.close()'
            4. When browser context closed after test completion - attach recorded video to allure report:
                path = <playwright_page>.video.path()
                allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
        :return: Playwright's Page instance related to the new opened tab.
        """
        log.info("Navigating to View cases Page")
        self._open_help_menu()
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(NavBarSelectors.VIEW_CASES_MENU_ITEM).click()
        return new_page_info.value

    def navigate_to_manage(self):
        """
        Navigates to Manage Workspace (Account) page
        """
        log.info("Navigating to Manage Account page")
        self._open_workspace_menu()
        self.page.locator(NavBarSelectors.MENU_ITEM_MANAGE_ACC).click()

    def navigate_to_manage_users(self):
        """
        Navigates to Manage Users page
        """
        log.info("Navigating to Manage Users page")
        self._open_workspace_menu()
        self.page.locator(NavBarSelectors.MENU_ITEM_MANAGE_USERS).click()

    def navigate_to_roles_permissions(self):
        """
        Navigates to Roles & Permissions page
        """
        log.info("Navigating to Roles & Permissions page")
        self._open_workspace_menu()
        self.page.locator(NavBarSelectors.MENU_ITEM_ROLES_PERMISSIONS).click()

    def navigate_to_switch_workspace(self):
        """
        Navigates to Switch Workspace page
        """
        log.info("Navigating to Switch Workspace page")
        self._open_workspace_menu()
        self.page.locator(NavBarSelectors.MENU_ITEM_SWITCH_WORKSPACE).click()

    def click_on_brand_logo(self):
        """
        Click on brand logo to return to home page
        """
        self.page.locator(NavBarSelectors.BRAND_LOGO).click()

    def click_on_tabs_in_help_and_support_menu(self, text):
        """
        Clicking buttons under help menu
        """
        self._open_help_menu()
        self.page.locator(NavBarSelectors.HELP_MENU_SUB_BUTTONS.format(text)).click()
        return self

    def click_on_contextual_help_menu(self):
        """
        Clicking on contextual help menu button
        :return: self reference.
        """
        log.info("Playwright: click on contextual help menu button.")
        self.page.locator(NavBarSelectors.CONTEXTUAL_HELP_BTN).click()
        return self

    def should_have_contextual_help_button(self):
        """
        Check that contextual help menu button is displayed.
        :return: self reference.
        """
        log.info("Playwright: verifying visibility of contextual help menu button")
        self.page.wait_for_load_state()
        expect(self.page.locator(NavBarSelectors.CONTEXTUAL_HELP_BTN)).to_be_visible()
        return self

    def should_have_user_icon_visible(self):
        """
        Verify that user icon shown on the top menu bar
        :return: self reference
        """
        expect(self.page.locator(NavBarSelectors.USER_MENU_BTN)).to_be_visible()
        return self

    def should_have_home_menu_button(self):
        """
        Checking the top navigation bar for Home menu button
        """
        log.info(f"Verifying Home Menu button on the navigation bar")
        self.page.wait_for_load_state()
        expect(self.page.locator(NavBarSelectors.MENU_BTN_HOME)).to_be_visible()
        return self

    def should_have_email_address_on_menu_item(self, email):
        """
        Verify top right the loggedin user email address
        :param: email: (required)
        :return: self reference
        """
        log.info(f"Verifying User Email {email} in user menu")
        self._open_user_menu()
        expect(self.page.locator(NavBarSelectors.MENU_ITEM_EMAIL_ADDRESS)).to_have_text(
            email
        )
        return self

    def should_not_have_devices_tab(self):
        """
        Check devices tab is not visible on NavBar for MSP user
        :return: self
        """
        log.info(f"Verifying Device Tab is Hidden")
        expect(self.page.locator(NavBarSelectors.MENU_BTN_DEVICES)).not_to_be_visible()
        return self

    def should_have_services_tab(self):
        """
        Verify the Services tab  on the navigation bar
        :return: self reference
        """
        log.info(f"Verifying Services Tab")
        expect(self.page.locator(NavBarSelectors.MENU_BTN_SERVICES)).to_be_visible()
        return self

    def should_have_displayed_account(self, account_name):
        """
        Verify that particular account is loaded in the navigation bar
        :param account_name: text to be displayed at workspace menu.
        :return: NavigationBar page object.
        """
        log.info("Playwright: check account name displayed at home page.")
        expect(self.page.locator(NavBarSelectors.WORKSPACE_MENU_TEXT)).to_have_text(
            account_name
        )
        return self

    def should_have_help_menu_options(self, text):
        """
        Verify the Help Menu on the navigation page
        :return: self reference
        """
        self._open_help_menu()
        modified_text = text.lower().replace(" ", "-")
        expect(
            self.page.locator(
                NavBarSelectors.HELP_MENU_ITEM_TEMPLATE.format(modified_text)
            )
        ).to_be_visible()
        return self

    def should_have_support_menu_options(self, text):
        """
        Verify the Support menu on the navigation page
        :return: self reference
        """
        modified_text = text.lower().replace(" ", "-")
        expect(
            self.page.locator(
                NavBarSelectors.SUPPORT_MENU_ITEM_TEMPLATE.format(modified_text)
            )
        ).to_be_visible()
        return self

    def should_have_user_menu_item(self, text):
        """
        Verify the User Menu on the navigation page
        :return: self reference
        """
        modified_text = text.lower().replace(" ", "-")
        expect(
            self.page.locator(NavBarSelectors.USER_MENU_ITEM.format(modified_text))
        ).to_be_visible()
        return self

    def should_have_help_menu_headings(self):
        """
        Checking help menu headings
        """
        self._open_help_menu()
        expect(
            self.page.locator(NavBarSelectors.HELP_MENU_HELP_TITLE)
            and self.page.locator(NavBarSelectors.HELP_MENU_SUPPORT_TITLE)
        ).to_be_visible()
        return self

    def should_have_app_menu_services_heading(self):
        """
        Checking app menu service headings
        """
        self._open_apps_menu()
        expect(
            self.page.locator(NavBarSelectors.APP_MENU_SERVICES_HEADER)
            and self.page.locator(NavBarSelectors.APP_MENU_GREENLAKE_ADMIN_HEADER)
            and self.page.locator(NavBarSelectors.APP_MENU_RESOURCES_HEADER)
        ).to_be_visible()
        return self

    def should_have_workspace_options(self):
        """
        Checking if page has workspace option
        """
        expect(
            self.page.locator(NavBarSelectors.MENU_ITEM_MANAGE_ACC)
            and self.page.locator(NavBarSelectors.MENU_ITEM_MANAGE_USERS)
            and self.page.locator(NavBarSelectors.MENU_ITEM_ROLES_PERMISSIONS)
            and self.page.locator(NavBarSelectors.MENU_ITEM_SWITCH_WORKSPACE)
        ).to_be_visible()
        return self

    def should_have_tabs_in_help_and_support_menu(self, text):
        """
        Checking buttons under help and support menu
        """
        self._open_help_menu()
        expect(
            self.page.locator(NavBarSelectors.HELP_MENU_SUB_BUTTONS.format(text))
        ).to_be_visible()
        return self

    def should_have_options_under_app_menu_services(self, text):
        """
        Checking the options under app menu services
        """
        self._open_apps_menu()
        modified_text = text.lower().replace(" ", "-")
        expect(
            self.page.locator(
                NavBarSelectors.APP_MENU_SERVICES_ITEM_TEMPLATE.format(modified_text)
            )
        ).to_be_visible()
        return self

    def should_have_options_under_app_menu_administrator(self, text):
        """
        Checking the options under app menu administrator
        """
        self._open_apps_menu()
        modified_text = text.lower().replace(" ", "-")
        expect(
            self.page.locator(
                NavBarSelectors.APP_MENU_ADMINISTRATION_ITEM_TEMPLATE.format(
                    modified_text
                )
            )
        ).to_be_visible()
        return self

    def should_have_options_under_app_menu_resources(self, text):
        """
        Checking the options under app menu resources
        """
        self._open_apps_menu()
        modified_text = text.lower().replace(" ", "-")
        expect(
            self.page.locator(
                NavBarSelectors.APP_MENU_RESOURCES_ITEM_TEMPLATE.format(modified_text)
            )
        ).to_be_visible()
        return self

    def _open_apps_menu(self):
        """
        Open app menu
        """
        self.page.locator(NavBarSelectors.APPS_MENU_BTN).click()

    def _open_workspace_menu(self):
        """
        Open the workspace page
        """
        if self.page.locator(NavBarSelectors.WORKSPACE_MENU_POPUP).is_hidden():
            self.page.click(NavBarSelectors.WORKSPACE_MENU_BTN)

    def _open_help_menu(self):
        """
        Open the help menu page
        """
        if self.page.locator(NavBarSelectors.HELP_MENU_POPUP).is_hidden():
            self.pw_utils.click_selector(NavBarSelectors.HELP_MENU_BUTTON)

    def _open_user_menu(self):
        """
        Open the usermenu page
        """
        if self.page.locator(NavBarSelectors.USER_MENU_POPUP).is_hidden():
            self.page.click(NavBarSelectors.USER_MENU_BTN)
