"""
Workspace details page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import WorkspaceDetailSelectors
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.manage_mfa_page import ManageMFA
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class WorkspaceDetails(HeaderedPage):
    """
    workspace details page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize workspace details page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/account-details"

    def edit_workspace_details(self, workspace_data: CreateUserData = CreateUserData):
        """
        Edits workspace account details

        :param workspace_data: account data for workspace details update,
            e.g. workspace_name, address,Email etc.
        :return: current instance of workspace details page object.
        """
        log.info("Updating workspace details")
        self.page.locator(WorkspaceDetailSelectors.EDIT_DETAILS_BTN).click()
        self.wait_for_loaded_state()
        self.page.locator(WorkspaceDetailSelectors.COUNTRY).click()
        self.page.locator(WorkspaceDetailSelectors.INPUT_COUNTRY_SEARCH).type(
            workspace_data.country, delay=100
        )
        self.page.get_by_text(workspace_data.country, exact=True).click()
        self.page.locator(WorkspaceDetailSelectors.STREET_ADDRESS_1).fill(
            workspace_data.street_address
        )
        self.page.locator(WorkspaceDetailSelectors.STREET_ADDRESS_2).fill(
            workspace_data.street_address2
        )
        self.page.locator(WorkspaceDetailSelectors.CITY).fill(workspace_data.city_name)
        self.page.locator(WorkspaceDetailSelectors.STATE_OR_REGION).fill(
            workspace_data.state_or_province
        )
        self.page.locator(WorkspaceDetailSelectors.ZIP).fill(workspace_data.postal_code)
        self.page.locator(WorkspaceDetailSelectors.EMAIL_DETAILS).fill(
            workspace_data.email
        )
        self.page.locator(WorkspaceDetailSelectors.PHONE_DETAILS).fill(
            workspace_data.phone_number
        )
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(WorkspaceDetailSelectors.SAVE_CHANGES_BTN).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.wait_for_selector(WorkspaceDetailSelectors.UPDATE_MSG_POPUP)
        expect(self.page.locator(WorkspaceDetailSelectors.UPDATE_MSG)).to_be_visible()
        log.info("Workspace has been updated successfully.")
        self.page.locator(WorkspaceDetailSelectors.UPDATE_MSG_CLOSE_BTN).click()
        return self

    def edit_workspace_name(self, workspace_name):
        """
        Edits workspace name
        :param workspace_name
        :return: current instance of workspace details page object.
        """
        self.page.locator(WorkspaceDetailSelectors.EDIT_DETAILS_BTN).click()
        self.page.locator(WorkspaceDetailSelectors.WORKSPACE_NAME).fill(workspace_name)
        self.page.locator(WorkspaceDetailSelectors.SAVE_CHANGES_BTN).click()
        return self

    def open_security_details(self):
        """
        Open Security Tab
        :return: instance of the manage_mfa page object.
        """
        log.info("Playwright: open Security tab of workspace details.")
        self.pw_utils.click_selector(WorkspaceDetailSelectors.SECURITY_BTN)
        return ManageMFA(self.page, self.cluster)

    def go_back_to_manage_workspace(self):
        """
        Navigate back to manage account page
        """
        log.info(f"Playwright: Navigating to manage account page")
        self.page.click(WorkspaceDetailSelectors.BACK_TO_MANAGE_BUTTON)
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of workspace details page object.
        """
        log.info(
            "Playwright: check that title has matched text in Workspace Details page."
        )
        expect(self.page.locator(WorkspaceDetailSelectors.PAGE_TITLE)).to_be_visible()
        return self
