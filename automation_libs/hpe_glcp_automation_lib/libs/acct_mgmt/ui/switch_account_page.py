"""
This file holds methods to switch account

"""
import logging
import re

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import SwitchAccountSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class SwitchAccount(HeaderedPage):
    """
    SwitchAccount page object
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Switch Account page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/switch-account"

    def search_account(self, account: str):
        """
        Searches the specified account

        :param account: name of the account
        :return: self
        """
        log.info(f"Playwright: search for text: '{account}' in customer records")
        self.pw_utils.enter_text_into_element(
            SwitchAccountSelectors.SEARCH_ACCOUNT_FIELD, account
        )
        self.wait_for_loaded_state()
        return self

    def filterby(self, _type: str = "All"):
        """
        Filter the account list for the given type

        :param _type: "Standard", "MSP", "All"
        :return: self
        """
        log.info(f"Playwright: filter by account type: '{_type}' in customer reecords")
        if (
            _type
            != self.page.locator(
                SwitchAccountSelectors.ACCOUNT_TYPE_DROPDOWN
            ).input_value()
        ):
            self.page.locator(SwitchAccountSelectors.ACCOUNT_TYPE_DROPDOWN).click()
            self.page.locator(
                SwitchAccountSelectors.DROPDOWN_OPTS_TEMPLATE.format(_type)
            ).click()
            self.wait_for_loaded_state()
        return self

    def sortby(self, _type: str = "Recent"):
        """
        Sort the account list for the given type

        :param _type: "Recent", "Alphabetical"
        :return: self
        """
        log.info(f"Playwright: sort by account type: '{_type}' in customer reecords")
        if (
            _type
            != self.page.locator(SwitchAccountSelectors.SORT_BY_DROPDOWN).input_value()
        ):
            self.page.locator(SwitchAccountSelectors.SORT_BY_DROPDOWN).click()
            self.page.locator(
                SwitchAccountSelectors.DROPDOWN_OPTS_TEMPLATE.format(_type)
            ).click()
            self.wait_for_loaded_state()
        return self

    def open_create_new_workspace(self):
        """
        Clicks the create new workspace button
        """
        self.page.locator(SwitchAccountSelectors.CREATE_NEW_ACCOUNT_BTN).click()
        # Note: instance of CreateAcctPage page object cannot be returned due to the circular import

    def launch_workspace(self, name: str = None):
        """
        Clicks the launch button of a workspace with a given name in the recent workspace div
        :param name: the name of the workspace which will be launched
        """
        if name:
            self.search_account(name)
        self.page.locator(SwitchAccountSelectors.RECENT_ACCOUNT_LAUNCH).click()
        # Note: instance of HomePage page object cannot be returned due to the circular import

    def should_have_sort_by_selected(self, text: str):
        """
        Verifies what is selected in the sort by dropdown
        :param text: Matches what is selected in the sort by dropdown with this
        Possible Values: "Recent", "Alphabetical"
        :return current instance.
        """
        expect(self.page.locator(SwitchAccountSelectors.SORT_BY_DROPDOWN)).to_have_value(
            text
        )
        return self

    def should_have_account_in_recent(self, account_name):
        """
        Check the account name listed in the recent first

        :param account_name: account_name
        :return: current instance
        """
        log.info(
            f"Playwright: check that account_name listed in the recent"
            f"with '{account_name}'"
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(SwitchAccountSelectors.RECENT_ACCOUNT_NAME)
        ).to_have_text(account_name)
        return self

    def should_have_accounts_count_in_recent(self, count):
        """
        Check count of account cards listed in the recent.
        :param count: (int) expected count of displayed cards.
        :return: current instance.
        """
        log.info(
            f"Playwright: check that account cards count in the recent is '{count}'."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(SwitchAccountSelectors.RECENT_ACCOUNT_CARDS)
        ).to_have_count(count)
        return self

    def should_have_counter_value(self, count):
        """
        Check  accounts counter value.
        :param count: (Union[int, str]) expected count at accounts counter.
        :return: current instance
        """
        log.info(f"Playwright: check that accounts counter has value '{count}'.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(SwitchAccountSelectors.RECENT_ACCOUNTS_COUNTER)
        ).to_contain_text(
            re.compile(f"^{count}\\s")
        )  # expected value at the beginning of the string, before space.
        return self

    def should_have_launch_button(self):
        """
        Verifies that there is a launch button in the workspaces div
        :return current instance.
        """
        expect(
            self.page.locator(SwitchAccountSelectors.RECENT_ACCOUNT_LAUNCH)
        ).to_be_visible()
        return self

    def should_have_create_new_workspace_btn(self):
        """
        Checking the presence of create new workspace button
        """
        log.info("Playwright: Checking the presence of new workspace_btn")
        expect(
            self.page.locator(SwitchAccountSelectors.CREATE_NEW_ACCOUNT_BTN)
        ).to_be_visible()
        return self
