"""
Choose api page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import APISelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class APIPage(HeaderedPage):
    """
    API page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page.
        :param cluster: cluster under.
        """
        log.info("Initialize API page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/api"
        self.client_id = None
        self.client_secret = None
        self.token = None

    def should_client_exist(self, name):
        """Verifies that client exists.
        :param name: name of client.
        :return: current instance of APIPage.
        """
        log.info(f"Checking if client with name {name} exists.")
        expect(self.page.get_by_role("tab", name=f"{name} FormDown")).to_be_visible(
            timeout=10000
        )
        return self

    def create_client(self, application, region, name):
        """
        To create a client with secret for an application.
        :param application: name of application
        :param region: region in which application is deployed
        :param name: name of client
        :return: APIPage.
        """
        log.info(f"Creating Client ID and Secret for {application} in {region}.")
        self.page.locator(APISelectors.CREATE_CREDENTIAL_BTN).click()
        self.page.locator(APISelectors.LIST_APPS).click()
        self.page.get_by_role("option", name=f"{application} ( {region} )").click()
        self.page.locator(APISelectors.CREDENTIAL_NAME).fill(name)
        self.page.locator(APISelectors.CREATE_CREDENTIAL_FORM_BTN).click()
        self.client_id = self.page.locator(APISelectors.CLIENT_ID).get_attribute("value")
        self.client_secret = self.page.locator(APISelectors.CLIENT_SECRET).get_attribute(
            "value"
        )
        self.page.locator(APISelectors.CLOSE_MODAL_BTN).click()
        return self

    def create_access_token(self, name):
        """
        Generate JWT Token.
        :param name: name of client
        :return: APIPage
        """
        log.info(f"Generating Token for {name}.")
        self.page.get_by_role("button", name=f"{name} FormDown").click()
        self.page.locator(APISelectors.API_CLIENT_ACTION_BTN)
        self.page.locator(APISelectors.GENERATE_ACCESS_TOKEN_BTN).click()
        self.page.locator(APISelectors.CLIENT_SECRET_INPUT).fill(self.client_secret)
        self.page.locator(APISelectors.CREATE_ACCESS_TOKEN_BTN).click()
        self.token = self.page.locator(APISelectors.ACCESS_TOKEN).get_attribute("value")
        self.page.locator(APISelectors.GENERATE_TOKEN_CLOSE_MODAL_BTN).click()
        return self

    def delete_client(self, name):
        """
        To delete the client
        :param name: name of the client
        :return: APIPage
        """
        log.info(f"Deleting client {name}.")
        self.page.get_by_role("button", name=f"{name} FormDown").click()
        self.page.locator(APISelectors.API_CLIENT_ACTION_BTN).click()
        self.page.locator(APISelectors.DELETE_CLIENT_BTN).click()
        self.page.locator(APISelectors.DELETE_CLIENT_CREDENTIAL_BTN).click()
        self.client_id = None
        self.client_secret = None
        self.token = None
        return self
