"""
My Applications page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.app_prov.ui.locators import (
    AppNavigationSelectors,
    MyApplicationsSelectors,
)
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class MyApplications(HeaderedPage):
    """
    My Applications page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize My Applications page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize My Applications page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/applications/my-apps"

    def wait_for_loaded_list(self):
        """
        Wait for list of applications is not empty and loader spinner is not present on the page.
        :return: current instance of My Applications page object.
        """
        log.info("Playwright: wait for applications list is loaded.")
        self.page.wait_for_selector(
            MyApplicationsSelectors.APPLICATION_TILE, state="visible", strict=False
        )
        self.page.locator(MyApplicationsSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_available_applications(self):
        """
        Navigate to Available Application page.
        Cannot add return because it creates a circular imports
        """
        log.info("Playwright: navigate to Available Applications page")
        self.page.wait_for_selector(AppNavigationSelectors.AVAILABLE_APPS_BTN).click()

    def open_installed_application(self, app_uuid: str):
        """
        Open an installed application
        :param app_uuid: application uuid
        :return: current instance of My Applications page object
        """
        log.info(
            f"Playwright: open the application with uuid '{app_uuid}' in My Applications page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(
            MyApplicationsSelectors.APPLICATION_CARD_TEMPLATE.format(app_uuid)
        ).click()
        return self

    def should_contain_text_in_title(self, text):
        """
        Check that expected text is present as part of the heading page title.
        :param text: expected text to be contained in title.
        :return: current instance of My Applications page object.
        """
        log.info(
            f"Playwright: check that title contains text '{text}' in My Applications page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(MyApplicationsSelectors.HEADING_PAGE_TITLE)
        ).to_contain_text(text)
        return self

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of My Applications page object.
        """
        log.info(
            f"Playwright: check that title has text '{text}' in My Applications page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(MyApplicationsSelectors.HEADING_PAGE_TITLE)
        ).to_have_text(text)
        return self

    def should_have_appplication(self, app_uuid: str):
        """
         Check for the application existence
        :param app_uuid: application uuid
        :return: current instance of My Applications page object
        """
        log.info(
            f"Playwright: check the application existence with uuid '{app_uuid}' in My Applications page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(
                MyApplicationsSelectors.APPLICATION_CARD_TEMPLATE.format(app_uuid)
            )
        ).to_be_enabled()
        return self

    def should_have_my_services_link(self, name="My Services"):
        """
            Verify the link My Services
        :param name: (required) for the Service name
        :return: current instance of My Applications page object.
        """
        log.info(f"Before click on My Services")
        expect(self.page.locator(MyApplicationsSelectors.MYSERVICES_BTN)).to_have_text(
            name
        )
        return self

    def should_have_subscriptions_link(self, name="Subscriptions"):
        """
        Verify the link Subscriptions
         :param name: (required) for the Subscription name
        :return: current instance of My Applications page object.
        """
        log.info(f"Before click on Subscriptions")
        expect(self.page.locator(MyApplicationsSelectors.SUBCRIPTIONS_BTN)).to_have_text(
            name
        )
        return self

    def should_have_catalog_link(self, name="Catalog"):
        """
        Verify the link Catalog
         :param name: (required) for the Catalog name
        :return: current instance of My Applications page object.
        """
        log.info(f"Before click on Catalog")
        expect(self.page.locator(MyApplicationsSelectors.CATALOG_BTN)).to_have_text(name)
        return self
