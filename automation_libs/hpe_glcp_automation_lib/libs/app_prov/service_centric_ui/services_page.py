"""
Services -  page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.app_catalog.service_centric_ui.service_catalog_page import (
    ServiceCatalog,
)
from hpe_glcp_automation_lib.libs.app_prov.service_centric_ui.locators import (
    ServicePageLocators,
)
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.headered_page import (
    HeaderedPage,
)
from hpe_glcp_automation_lib.libs.sm.service_centric_ui.service_subscriptions import (
    DeviceSubscriptions,
)

log = logging.getLogger(__name__)


class ServicesPage(HeaderedPage):
    """
    ServicesPage page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Services page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize ServicesPage page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/services/my-services"

    def choose_region_filtered_out(self, region):
        """
        Choose the Region for {region}
        :param region: expected region to match with the region in dropdown.
        :return : self reference
        """
        log.info("Corresponding Region should be filtered out")
        self.pw_utils.click_selector(ServicePageLocators.ALL_REGION)
        self.page.locator(ServicePageLocators.CHOOSE_REGION.format(region)).click()
        return self

    def click_launch_btn(self):
        """
        Click on launch button for related Service
        :return : self reference
        """
        log.info("Services that are already provisioned and launchable")
        self.wait_for_loaded_state()
        self.pw_utils.click_selector(ServicePageLocators.LAUNCH_BTN)
        return self

    def click_on_catalog_in_services_tab(self):
        """
        Navigate to service-catalog page
        :return: ServiceCatalog page
        """
        log.info(f"Playwright: click on catalog tab")
        self.page.locator(ServicePageLocators.SERVICE_CATALOG).click()
        return ServiceCatalog(self.page, self.cluster)

    def click_on_subscriptions_tab(self):
        """click on subscription in service tab it navigates to Service subscription page"""
        self.page.locator(ServicePageLocators.SUBSCRIPTION_TAB).click()
        return DeviceSubscriptions(self.page, self.cluster)

    def should_have_my_services_tab_in_services_tab(self, text="My Services"):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return : self reference
        """
        log.info(f"Playwright: check that title has my services text in Services page.")
        expect(self.page.locator(ServicePageLocators.MY_SERVICES_TAB)).to_contain_text(
            text
        )
        return self

    def should_have_catalog_tab_in_services_tab(self, text="Catalog"):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return : self reference
        """
        log.info(f"Playwright: check that title has catalog text in Services page.")
        expect(self.page.locator(ServicePageLocators.SERVICE_CATALOG)).to_contain_text(
            text
        )
        return self

    def should_have_subscription_tab(self, text="Subscriptions"):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return : self reference
        """
        log.info(f"Playwright: check that title has catalog text in Services page.")
        expect(self.page.locator(ServicePageLocators.SUBSCRIPTION_TAB)).to_contain_text(
            text
        )
        return self

    def should_contain_text_in_title(self, text="Services"):
        """
        Check that expected text is present as part of the heading page title.
        :param text: expected text to be contained in title.
        :return: current instance of service page object.
        """
        log.info(f"Playwright: check that title contains text '{text}' in service page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(ServicePageLocators.ADD_SERVICE_SUBSCRIPTIONS_HEADING)
        ).to_contain_text(text)
        return self
