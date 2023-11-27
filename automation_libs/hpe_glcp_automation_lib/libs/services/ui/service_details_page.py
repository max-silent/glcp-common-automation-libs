"""
Service Details Page model.
"""
import logging
import re

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.services.ui.locators import ServiceDetailsSelectors

log = logging.getLogger()


class ServiceDetails(HeaderedPage):
    """
    Service Details page object model
    """

    def __init__(self, page: Page, cluster: str, service_name: str):
        """Initialize 'ServiceDetails' with page and cluster.

        :param page: Page
        :param cluster: cluster under test url
        :param service_name: name of the service
        """
        log.info(f"Initialize ServiceDetails page-object for '{service_name}'.")
        super().__init__(page, cluster)
        self.url = (
            f"{cluster}/services/service-catalog/{service_name.lower().replace(' ', '-')}"
        )
        self.service_name = service_name

    def click_on_tab(self, text):
        """Click on tab with specified text.

        :return: current instance of ServiceDetails page object.
        """
        tab_locator = self.page.locator(ServiceDetailsSelectors.TAB_TEMPLATE.format(text))
        if tab_locator.get_attribute("aria-selected") == "false":
            log.info(f"Playwright: Click at '{text}' tab.")
            tab_locator.click()
        return self

    def click_on_provision_btn(self):
        """Click on provision button of Service-details page.

        :return: current instance of ServiceDetails page object.
        """
        log.info(f"Playwright: Click at Provision button")
        self.page.locator(ServiceDetailsSelectors.PROVISION_BTN).click()
        return self

    def go_back_to_service_catalog(self):
        """
        Navigate back to service catalog page.
        """
        log.info(f"Playwright: Clicking on back to service catalog page button")
        self.page.locator(ServiceDetailsSelectors.BACK_TO_SERVICE_CATALOG).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def deploy_service_using_provision_btn(self, region=None):
        """Deploy service using 'Provision' button.
        Deploys at given region if specified or at first available region otherwise.

        :param region: region to deploy at.
        return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Provisioning '{self.service_name}' to {region if region else 'first available'} region."
        )
        self.click_on_provision_btn()
        self._process_deployment(region)
        return self

    def deploy_service(self, region=None):
        """Deploy service using 'Add Region' button.
        Deploys at given region if specified or at first available region otherwise.

        :param region: region to deploy at.
        :return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Deploying '{self.service_name}' to {region if region else 'first available'} region."
        )
        self.click_on_tab("Regions")
        self.page.locator(ServiceDetailsSelectors.ADD_REGION_BTN).click()
        self._process_deployment(region)
        return self

    def deploy_service_to_all_regions(self):
        """Deploy Service to all available Regions.

        :return: current instance of ServiceDetails page object.
        """
        log.info(f"Playwright: Deploying service to all available Regions.")
        add_region_button = self.page.locator(ServiceDetailsSelectors.ADD_REGION_BTN)
        while add_region_button.is_visible():
            self.deploy_service()
        return self

    def remove_service(self, region=None):
        """Remove deployed service from given region if specified or from first displayed region otherwise.

        :param region: region to remove from.
        :return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Removing {self.service_name} from {region if region else 'first displayed'} region."
        )
        region = region.lower().replace(" ", "-") if region else ""

        first_item = self.page.locator(
            ServiceDetailsSelectors.INSTALLED_APP_REGION_NAME_TEMPLATE.format(region, "")
        ).first
        # Wait for text is loaded to the element
        expect(first_item).to_contain_text(re.compile(r"\w+"), timeout=5000)
        service_region_tag = first_item.text_content()

        self.page.locator(
            ServiceDetailsSelectors.INSTALLED_APP_ACTION_BTN_TEMPLATE.format(region)
        ).first.click()
        self.page.locator(
            ServiceDetailsSelectors.APP_ACTION_TEMPLATE.format("Remove Region")
        ).click()
        self.page.locator(ServiceDetailsSelectors.REMOVE_REGION).click()
        self.pw_utils.wait_for_selector(
            ServiceDetailsSelectors.LOADER_SPINNER, timeout_ignore=True, timeout=10000
        )
        self.page.locator(ServiceDetailsSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.locator(
            ServiceDetailsSelectors.INSTALLED_APP_REGION_NAME_TEMPLATE.format(
                region, service_region_tag
            )
        ).wait_for(state="hidden", timeout=90000)
        return self

    def remove_service_from_all_regions(self):
        """Remove deployed service from all regions.

        :return self: current instance of ServiceDetails page object.
        """
        log.info(f"Playwright: Removing service from all deployed regions.")
        installed_apps = self.page.locator(
            ServiceDetailsSelectors.INSTALLED_APP_REGION_ITEMS
        )
        items_count = installed_apps.count()
        if items_count == 0:
            log.warning("There is no any displayed item of region-deployed service.")
        while items_count > 0:
            self.remove_service()
            after_removal_count = installed_apps.count()
            if after_removal_count == items_count:
                raise ValueError(
                    f"Displayed services count was not changed after removal: remained {items_count}."
                )
            items_count = after_removal_count
        return self

    def should_not_have_unavailable_regions_error(self):
        """Check that message about already added all available regions for this service is not displayed.
        Applicable to 'Regions' tab of service details page.

        :return: current instance of ServiceDetails page object.
        """
        log.info(
            "Playwright: Checking that there is no message about lack of available regions for service."
        )
        expect(
            self.page.locator(ServiceDetailsSelectors.UNAVAILABLE_REGIONS_ERROR)
        ).not_to_be_visible()
        return self

    def should_have_provision_button(self):
        """
        Check for the presence of the provision button.
        :return: current instance of ServiceDetails page object.
        """
        log.info("Playwright: Check that provision button is displayed.")
        expect(self.page.locator(ServiceDetailsSelectors.PROVISION_BTN)).to_be_visible()
        return self

    def should_not_have_provision_button(self):
        """Check that provision button is not displayed.
        :return: current instance of ServiceDetails page object.
        """
        log.info("Playwright: Check that provision button is displayed.")
        expect(self.page.locator(ServiceDetailsSelectors.PROVISION_BTN)).to_be_hidden()
        return self

    def should_have_service(self, region):
        """Check Service exists at specified region.

        :param region: region.
        :return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Check that '{self.service_name}' service in '{region}' region is present."
        )
        region = region.lower().replace(" ", "-")
        expect(
            self.page.locator(
                ServiceDetailsSelectors.INSTALLED_APP_REGION_TEMPLATE.format(region)
            )
        ).to_be_visible()
        return self

    def should_have_launch_button(self):
        """Verify that launch button is present on the page.

        :return: current instance of ServiceDetails page object.
        """
        log.info(f"Playwright: Check that launch button is displayed.")
        expect(self.page.locator(ServiceDetailsSelectors.LAUNCH_BTN)).to_be_visible()
        return self

    def should_have_overview_tab_content(self):
        """Check that element with overview content is present at the page.

        return: current instance of ServiceDetails page object.
        """
        log.info(
            "Playwright: Check that area with overview content is present at the page."
        )
        expect(self.page.locator(ServiceDetailsSelectors.OVERVIEW_AREA)).to_be_visible()
        return self

    def should_have_title(self):
        """Check that heading title is displayed.

        return: current instance of ServiceDetails page object.
        """
        log.info("Playwright: Check that heading title is present at the page.")
        expect(
            self.page.locator(ServiceDetailsSelectors.HEADING_PAGE_TITLE)
        ).to_be_visible()
        return self

    def should_have_region_available(self, region: str):
        """Verify the region in the available region for the service

        param: region to verify
        return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Should have the {region} region in available region at the {self.service_name} page."
        )
        expect(
            self.page.locator(
                ServiceDetailsSelectors.AVAILABLE_REGION_TEMPLATE.format(region)
            )
        ).to_be_visible()
        return self

    def should_have_documentation_link(self):
        """Check the documentation link for the service

        return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Check that documentation link is present at the {self.service_name} page."
        )
        expect(
            self.page.locator(ServiceDetailsSelectors.DOCUMENTATION_LINK)
        ).to_be_visible()
        return self

    def should_have_terms_of_service(self):
        """Check the terms of service link for the service

        return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Check that terms of service link is present at the {self.service_name} page."
        )
        expect(
            self.page.locator(ServiceDetailsSelectors.TERMS_OF_SERVICE_LINK)
        ).to_be_visible()
        return self

    def _process_deployment(self, region):
        """Process 'Provision Service Manager' dialog and wait until service deployment completed.
        Deploys at given region if specified 'region' is not 'None' or at first available region otherwise.

        :param region: region to deploy at.
        return: current instance of ServiceDetails page object.
        """
        if region:
            self.pw_utils.select_drop_down_element(
                ServiceDetailsSelectors.REGION_DROPDOWN, region, "option"
            )
        else:
            self.page.locator(ServiceDetailsSelectors.REGION_DROPDOWN).click()
            self.page.locator(ServiceDetailsSelectors.REGION_DROPDOWN_ITEM).click()
        self.page.locator(ServiceDetailsSelectors.TERMS_CONDITION_CHECKBOX).click()
        self.page.locator(ServiceDetailsSelectors.DEPLOY_BTN).click()
        self.pw_utils.wait_for_selector(
            ServiceDetailsSelectors.LOADER_SPINNER, timeout_ignore=True, timeout=10000
        )
        self.page.locator(ServiceDetailsSelectors.LOADER_SPINNER).wait_for(
            state="hidden", timeout=90000
        )

    def should_not_have_remove_region(self):
        """Check the remove region not to be visible for the service

        return: current instance of ServiceDetails page object.
        """
        log.info(
            f"Playwright: Check that remove region is not present at the {self.service_name} page."
        )
        self.page.locator(
            ServiceDetailsSelectors.INSTALLED_APP_ACTION_BTN_TEMPLATE.format("")
        ).first.click()
        expect(
            self.page.locator(
                ServiceDetailsSelectors.APP_ACTION_TEMPLATE.format("Remove Region")
            )
        ).not_to_be_visible()
        return self
