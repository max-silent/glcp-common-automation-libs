"""
Choose account page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_account_page import CreateAcctPage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import ChooseAccountSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_home_page import TacHomePage
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class ChooseAccount(HeaderedPage):
    """
    Choose account page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize ChooseAccount page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/onboarding/choose-account"

    def open(self):
        """
        Navigate to choose account by url
        :return: current instance of page object
        """
        log.info("Open Choose Account page by navigating to url.")
        self.page.goto(self.url)
        self.pw_utils.wait_for_selector(
            ChooseAccountSelectors.GO_TO_ACCOUNT, timeout_ignore=True, timeout=10000
        )
        if self.page.locator(ChooseAccountSelectors.GO_TO_ACCOUNT).count() < 2:
            self.pw_utils.wait_for_url(
                f"{self.cluster}/home", timeout_ignore=True, timeout=20000
            )
        current_url = self.page.url
        if not current_url == self.url:
            log.error("Unexpected URL")
            self.pw_utils.save_screenshot(self.test_name)
            raise Exception(
                f"Wrong page opened instead of expected 'choose-account': '{current_url}'"
            )
        return self

    def go_to_account_by_index(self, num: int):
        """
        Select account by index.
        :param num: index (starting from 0) of account to choose.
        :return: instance of homepage object
        """
        log.info(f"Go to account with index '{num}'.")
        self.page.locator(ChooseAccountSelectors.GO_TO_ACCOUNT).nth(num).click()
        self.page.wait_for_load_state("domcontentloaded")
        return HomePage(self.page, self.cluster)

    def go_to_account_by_name(self, name: str):
        """
        Select account by name.
        :param name: name of account to choose.
        :return: instance of homepage object
        """
        log.info(f"Go to account with name '{name}'.")
        self._go_to_account_by_name(name)
        return HomePage(self.page, self.cluster)

    def go_to_account_by_name_tac(self, name: str):
        """Select account of TAC user by account name.

        :param name: name of account to choose.
        :return: instance of TAC homepage object.
        """
        log.info(f"TAC: Go to account with name '{name}'.")
        self._go_to_account_by_name(name)
        return TacHomePage(self.page, self.cluster)

    def open_create_account(self):
        """
        Navigate to create account page
        """
        self.page.locator(ChooseAccountSelectors.CREATE_ACCT_BTN).click()
        return CreateAcctPage(self.page, self.cluster)

    def _go_to_account_by_name(self, name: str):
        """Select account of user by account name.

        :param name: name of account to choose.
        """
        self.pw_utils.enter_text_into_element(ChooseAccountSelectors.SEARCH_BOX, name)
        try:
            self.page.wait_for_selector(
                ChooseAccountSelectors.COMPANY_NAME_TEMPLATE.format(name),
                state="visible",
                strict=True,
            )
        except Exception as ex:
            log.error(f"Company name resolving error.")
            self.pw_utils.save_screenshot(self.test_name)
            raise Exception(f"Not resolved company name:\n{ex}")

        self.page.locator(
            ChooseAccountSelectors.GO_TO_ACCOUNT_TEMPLATE.format(name)
        ).click()
        self.page.wait_for_load_state("domcontentloaded")

    def should_have_welcome_title(self, name="Welcome to HPE GreenLake", timeout=20000):
        """
        Verifies Choose Account have Title with {name} present
        param: {name} (optional)
        timeout: int (optional)
        :return: current instance of choose-account page object.
        """
        log.info(f"Verify that title contains '{name}' text.")
        self.page.wait_for_load_state("domcontentloaded")
        expect(
            self.page.locator(ChooseAccountSelectors.WELCOME_HPE_GLE_HEADER)
        ).to_contain_text(name, timeout=timeout)
        return self

    def should_have_create_workspace(self):
        """
        Verifies that the create workspace button exists
        :return: current instance of choose-account page object.
        """
        log.info("Verify that create workspace button exists")
        expect(self.page.locator(ChooseAccountSelectors.CREATE_ACCT_BTN)).to_be_visible()
        return self

    def should_have_welcome_subheader(self, name: str):
        """
        Verifies that the welcome subheader exists
        :return: current instance of choose-account page object.
        """
        log.info(
            f"Verify that the subheader contains "
            f"'Here's a list of workspaces we found associated with {name}' text "
        )
        expect(
            self.page.locator(ChooseAccountSelectors.WELCOME_SUBHEADER)
        ).to_contain_text(f"Here's a list of workspaces we found associated with {name}")
        return self

    def should_count_workspaces(self):
        """
        Verifies that the count workspaces function works
        :return: current instance of choose-account page object.
        """
        log.info("Verify that workspace counter functions")
        num_of_workspace = (
            self.page.locator(ChooseAccountSelectors.ACCOUNTS_COUNT)
            .text_content()
            .split()[0]
        )
        if num_of_workspace == 0:
            self.should_not_have_goto_workspace()
        else:
            self.should_have_goto_workspace()
        return self

    def should_not_have_goto_workspace(self):
        """
        Verifies that no goto workspace cards exist
        :return: current instance of choose-account page object.
        """
        log.info("Verify that goto workspace button does not exist")
        expect(
            self.page.locator(ChooseAccountSelectors.GO_TO_ACCOUNT)
        ).not_to_be_visible()
        return self

    def should_have_goto_workspace(self):
        """
        Verifies that a goto workspace button exists
        :return: current instance of choose-account page object.
        """
        log.info("Verify that goto workspace button exists")
        expect(
            self.page.locator(ChooseAccountSelectors.GO_TO_ACCOUNT).first
        ).to_be_visible()
        return self

    def should_have_back_to_sign_in_option(self):
        """
        User should see back to sign in option at Choose Account page.
        :return: current instance of page object
        """
        expect(
            self.page.locator(ChooseAccountSelectors.BACK_TO_SIGN_IN_BTN)
        ).to_be_visible()
        return self
