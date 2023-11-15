import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.app_prov.service_centric_ui.locators import (
    ServiceDetailsSelectors,
)
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage

log = logging.getLogger()


class ServiceDetails(HeaderedPage):
    """
    Service Detail page object model
    """

    def __init__(self, page: Page, cluster: str, service_name: str):
        """
         Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        :service_name: name of the service
        """
        log.info("Initialize ServiceDetails  page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/services/service-catalog/{service_name}"
        self.service_name = service_name

    def click_on_tab(self, text):
        """
        Click on tab with specified text.
        :return: self
        """
        self.page.locator(ServiceDetailsSelectors.TAB_TEMPLATE.format(text)).click()
        return self

    def remove_service(self, region):
        """
        To remove service for given region
        :param region: region
        :return: ServiceDetails page object
        """
        log.info(f"Removing {self.service_name} from region {region}.")
        region = region.lower().replace(" ", "-")
        self.page.locator(ServiceDetailsSelectors.EllipsisIcon.format(region)).click()
        self.page.locator(ServiceDetailsSelectors.REMOVE_BUTTON).click()
        self.page.locator(ServiceDetailsSelectors.REMOVE_REGION).click()
        self.page.locator(ServiceDetailsSelectors.LOADER_SPINNER).wait_for(state="hidden")
        log.info(f"{self.service_name} from region {region} removed.")
        return self

    def deploy_service(self, region):
        """
        Deploy service in give region.
        :param region: region
        :return: ServiceDetails page object
        """

        log.info(f"Deploying {self.service_name} in region {region}.")
        self.click_on_region_tab()
        self.page.locator(ServiceDetailsSelectors.ADD_REGION).click()
        self.page.locator(ServiceDetailsSelectors.SELECT_REGION).click()
        self.page.get_by_role("option", name=region).click()
        self.page.locator(ServiceDetailsSelectors.TERMS_CONDITION_CHECKBOX).click()
        self.page.locator(ServiceDetailsSelectors.DEPLOY_BTN).click()
        self.page.locator(ServiceDetailsSelectors.LOADER_SPINNER).wait_for(state="hidden")
        log.info(f"{self.service_name} in region {region} deployed.")
        return self

    def click_on_provision_btn(self):
        """
        clicks on provision button on Service-catalog page
        :param: text: (required)
        :return: self reference.
        """
        log.info(f"click on PROVISION button")
        self.page.locator(ServiceDetailsSelectors.PROVISION_BTN).first.click()
        return self

    def check_region_provision_eligiblity(self):
        region_element = self.page.locator(
            ServiceDetailsSelectors.REGION_VALUE
        ).get_attribute("value")
        region = region_element if region_element else ""
        if region == "O":
            return True
        return False

    def click_on_region_tab(self):
        """
        Click on Region tab and verify provision button if region is 'O'.
        :return: self
        """
        if (
            "Regions"
            not in self.page.locator(ServiceDetailsSelectors.ACTIVE_TAB).text_content()
        ):
            self.page.locator(ServiceDetailsSelectors.SERVICE_DETAILS_TAB).click()
        else:
            log.info("Region tab not available!")
        return self

    def should_have_provision_button(self):
        """
        Check for the presence of the provision button.
        :return: self reference
        """
        self.page.wait_for_load_state("domcontentloaded")
        log.info("Playwright: Checking the presence of the provision button.")
        expect(self.page.locator(ServiceDetailsSelectors.PROVISION_BTN)).to_be_visible()
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
            self.page.locator(ServiceDetailsSelectors.HEADING_PAGE_TITLE)
        ).to_have_text(text)
        return self

    def should_have_service(self, region):
        """
        Check Service exists
        :param region: region
        :return: ServiceDetails page object
        """
        log.info(f"Finding {self.service_name} in region {region}.")
        region = region.lower().replace(" ", "-")
        expect(
            self.page.locator(
                ServiceDetailsSelectors.INSTALLED_SERVICE_REGION_TEMPLATE.format(region)
            )
        ).to_be_visible()
        return self
