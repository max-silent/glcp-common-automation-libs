import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_services_navigable_page import (
    SideMenuNavigablePage,
)
from hpe_glcp_automation_lib.libs.services.ui.locators import ServiceCatalogSelectors
from hpe_glcp_automation_lib.libs.services.ui.service_details_page import ServiceDetails

log = logging.getLogger()


class ServiceCatalog(HeaderedPage, SideMenuNavigablePage):
    """
    Service Catalog Page Object Model
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with Service Catalog Page
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Playwright: Initialize Service Catalog page.")
        super().__init__(page, cluster)
        self.url = f"{cluster}/services/service-catalog"

    def wait_for_loaded_list(self):
        """
         Wait for list of services is not empty and loader spinner is not present on the page.
        :return: current instance of Service Catalog page object.
        """
        log.info("Playwright: wait for services list is loaded.")
        self.page.locator(ServiceCatalogSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_selector(
            ServiceCatalogSelectors.SERVICES_CARDS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_service(self, service_name: str):
        """
         Open the service details page
        :param service_name: name of the service
        :return: instance of Service Details page object
        """
        self.wait_for_loaded_list()
        log.info(f"Playwright: Opens details for '{service_name}' service.")
        service_locator = ServiceCatalogSelectors.SERVICES_OPEN_LINK_TEMPLATE.format(
            service_name
        )
        self.page.locator(service_locator).click()
        return ServiceDetails(self.page, self.cluster, service_name)

    def select_region(self, region: str):
        """
        Select region to filter services on page
        :param region: name of the region
        :return: instance of Service Catalog page object
        """
        log.info(f"Playwright: Select region {region} to filter service catalog.")
        self.pw_utils.select_drop_down_element(
            ServiceCatalogSelectors.SELECT_REGION_DROPDOWN, region, "option"
        )
        return self

    def should_have_services_title(self):
        """
        Verify the presence of the title 'Services' text.
        :return: self reference.
        """
        log.info(f"Verifying the presence of the title 'Services'.")
        self.page.wait_for_load_state("domcontentloaded")
        expect(
            self.page.locator(ServiceCatalogSelectors.SERVICES_PAGE_HEADING)
        ).to_be_visible()
        return self

    def should_have_service(self, service_name: str):
        """
         Check for the service existence
        :param service_name: name of the service
        :return: current instance of Service Catalog page object
        """
        self.wait_for_loaded_list()
        log.info(
            f"Playwright: check the service existence with name '{service_name}' in Service Catalog page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(
                ServiceCatalogSelectors.SERVICES_OPEN_LINK_TEMPLATE.format(service_name)
            )
        ).to_be_visible()
        return self

    def should_contain_text_in_title(self, text):
        """
        Check that expected text is present as part of the heading page title.
        :param text: expected text to be contained in title.
        :return: current instance of ServiceCatalog page object.
        """
        log.info(
            f"Playwright: check that title contains text '{text}' in ServiceCatalog page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(ServiceCatalogSelectors.HEADING_PAGE_TITLE)
        ).to_contain_text(text)
        return self

    def should_only_contain_specified_services(self, qualifier):
        """
        Checks that all available services contain a specified qualifier.
        :param qualifier: expected text to be contained in each card
        :return: current instance of ServiceCatalog page object
        """
        log.info(
            f"Playwright: check that all services contain matching keyword: '{qualifier}'."
        )
        self.pw_utils.save_screenshot(self.test_name)
        for card in self.page.locator(ServiceCatalogSelectors.SERVICES_CARDS).all():
            expect(card).to_contain_text(qualifier)
        return self
