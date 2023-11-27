"""
API  page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import ApiPageSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class APIpage(HeaderedPage):
    """
    API  page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize API page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/api"
        self.client_id = None
        self.client_secret = None
        self.token = None

    def expand_client_panel(self, name):
        """Expand panel with specified client name.

        :param name: name of client.
        :return: current instance of APIPage page object.
        """
        client_pane_locator = self.page.locator(
            ApiPageSelectors.CLIENT_BTN_TEMPLATE.format(name)
        )
        if client_pane_locator.get_attribute("aria-expanded") == "false":
            log.info(f"Playwright: Expand panel of '{name}' client.")
            client_pane_locator.click()
        return self

    def create_client(self, application, region=None, name=None):
        """Create a client with secret for an application.

        :param application: name of application.
        :param region: region in which application is deployed.
        :param name: name of client.
        :return: current instance of APIPage page object.
        """
        log.info(f"Creating Client ID and Secret for {application} in '{region}' region.")
        list_item_text = f"{application}"
        if region:
            list_item_text += f" ( {region} )"
        self.page.locator(ApiPageSelectors.CREATE_CREDENTIAL_BTN).click()
        self.pw_utils.select_drop_down_element(
            drop_menu_selector=ApiPageSelectors.SERVICE_MANAGER_DROPDOWN,
            element=list_item_text,
            element_role="option",
            exact_match=True,
        )
        self.page.locator(ApiPageSelectors.CREDENTIAL_NAME).fill(name)
        self.page.locator(ApiPageSelectors.CREATE_CREDENTIAL_FORM_BTN).click()
        self.client_id = self.page.locator(ApiPageSelectors.CLIENT_ID).get_attribute(
            "value"
        )
        self.client_secret = self.page.locator(
            ApiPageSelectors.CLIENT_SECRET
        ).get_attribute("value")
        self.page.locator(ApiPageSelectors.CLOSE_MODAL_BTN).click()
        self.wait_for_loaded_state()
        return self

    def delete_client(self, name):
        """Delete API-client with specified name.

        :param name: name of the client.
        :return: current instance of APIPage page object.
        """
        log.info(f"Deleting client '{name}'.")
        self.expand_client_panel(name)
        self.page.locator(ApiPageSelectors.API_CLIENT_ACTION_BTN).click()
        self.page.locator(ApiPageSelectors.DELETE_CLIENT_BTN).click()
        self.page.locator(ApiPageSelectors.DELETE_CLIENT_CREDENTIAL_BTN).click()
        self.wait_for_loaded_state()
        self.client_id = None
        self.client_secret = None
        self.token = None
        return self

    def create_access_token(self, name):
        """Generate JWT Token.

        :param name: name of client.
        :return: current instance of APIPage page object.
        """
        self.expand_client_panel(name)
        log.info(f"Generating Token for '{name}' client.")
        self.page.locator(ApiPageSelectors.GENERATE_ACCESS_TOKEN_BTN).click()
        self.page.locator(ApiPageSelectors.CLIENT_SECRET_INPUT).fill(self.client_secret)
        self.page.locator(ApiPageSelectors.CREATE_ACCESS_TOKEN_BTN).click()
        self.token = self.page.locator(ApiPageSelectors.ACCESS_TOKEN).get_attribute(
            "value"
        )
        self.page.locator(ApiPageSelectors.CLOSE_MODAL_BTN).click()
        return self

    def should_client_exist(self, name):
        """Verify that client exists.

        :param name: name of client.
        :return: current instance of APIPage.
        """
        log.info(f"Playwright: checking if client with name '{name}' exists.")
        expect(
            self.page.locator(ApiPageSelectors.CLIENT_BTN_TEMPLATE.format(name))
        ).to_be_visible()
        return self

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of API  page object.
        """
        log.info("Playwright: check that title has matched text in API  page.")
        expect(self.page.locator(ApiPageSelectors.PAGE_TITLE)).to_be_visible()
        return self
