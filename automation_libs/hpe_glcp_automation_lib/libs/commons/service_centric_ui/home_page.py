"""
Homepage page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.service_centric_ui.switch_account_page import (
    SwitchAccount,
)
from hpe_glcp_automation_lib.libs.adi.service_centric_ui.dev_inventory_page import (
    DevicesInventory,
)
from hpe_glcp_automation_lib.libs.app_prov.service_centric_ui.service_page import (
    ServicesPage,
)
from hpe_glcp_automation_lib.libs.authz.service_centric_ui.users_page import Users
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.headered_page import (
    HeaderedPage,
)
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.locators import (
    HomePageSelectors,
)
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.private_cloud_buisness_entrprise_page import (
    PrivateCloudBusinessEnterprise,
)
from hpe_glcp_automation_lib.libs.locations.service_centric_ui.create_location_page import (
    CreateLocationPage,
)

log = logging.getLogger(__name__)


class HomePage(HeaderedPage):
    """
    Homepage page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize homepage page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize HomePage page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/home"

    def wait_for_loaded_state(self):
        """
        Wait till page is loaded and loading spinner is not present.
        :return: current instance of Homepage page object.
        """
        log.info("Playwright: wait for home page is loaded.")
        super().wait_for_loaded_state()
        self.page.locator(HomePageSelectors.LOADER_SPINNER).wait_for(state="hidden")
        return self

    def should_have_displayed_account(self, account_name):
        """
        Verify that home page successfully loaded for particular account.
        :return: current instance of Homepage page object.
        """
        log.info("Playwright: check account name displayed at home page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(HomePageSelectors.ACCT_NAME)).to_have_text(account_name)
        return self

    def open_switch_acct(self):
        """
        Verify that switch account loaded successfully loaded for particular account.
        :return: SwitchAccount Page
        """
        self.page.locator(HomePageSelectors.SWITCH_ACCOUNT_BUTTON).click()
        return SwitchAccount(self.page, self.cluster)

    def open_return_msp_account(self):
        """
        Navigates to MSP Account homepage
        return:current instance of homepage object
        """
        self.page.locator(HomePageSelectors.RETURN_TO_MSP_ACCT_BTN).click()
        return self

    def click_service_arrow_link(self, service_name):
        """
        verify “Click on Specified Arrow Link which matches {Param}”
        service_name: param (optional) to compare text
        :return:self reference
        """
        log.info(f"Playwright: Clicking on {service_name} Arrow")
        self.page.locator("span", has_text=service_name).first.click()
        return self

    def click_on_private_cloud(self):
        """
        Click on the private cloud tab
        :return: self reference
        """
        log.info("Playwright: Click on Private Cloud tab")
        self.page.locator(HomePageSelectors.PRIVATE_CLOUD_TAB).click()
        return self

    def click_quickaction_add_users_or_assign_roles_link(self):
        """
        Click on the Add Users/ Assign Roles link from Quick Actions section under Home page
        :return: Users page
        """
        log.info("Playwright: Click on Quickaction add_users_or_assign_roles_link")
        self.page.locator(HomePageSelectors.ADD_USER_OR_ASSIGN_ROLES_LINK_PATH).click()
        return Users(self.page, self.cluster)

    def click_quickaction_add_service_subscription_link(self):
        """
        Clicks on Add Service Subscriptions link under Quick Actions on Home page
        :return: ServicesPage page
        """
        log.info(f"Playwright: Click on Add Service Subscriptions link")
        self.page.locator(HomePageSelectors.ADD_SERVICE_SUBSCRIPTIONS_LINK).first.click()
        self.page.wait_for_load_state()
        return ServicesPage(page=self.page, cluster=self.cluster)

    def click_quickaction_add_device_link(self):
        """
        Click on the "Add device" link under “Quick_actions”
        :return: DevicesInventory page
        """
        log.info(f"Playwright: Clicking on Quick Action Add device link")
        self.page.wait_for_load_state()
        self.page.locator(HomePageSelectors.ADD_DEVICE_LINK).click()
        return DevicesInventory(self.page, self.cluster)

    def click_quickaction_click_location_link(self):
        """
        verify “create_location link” under “Quick_actions”
        :return: LocationPage
        """
        log.info(f"Playwright: Clicking Quick Action Create Location link.")
        self.page.wait_for_load_state()
        self.page.wait_for_selector(HomePageSelectors.CREATE_LOCATION_LINK).click()
        return CreateLocationPage(self.page, self.cluster)

    def click_recent_services_launch(self, text):
        """
        verify launch button under recent services is clickable
        :param: text: (required)
        :return: self reference
        """
        log.info(f"Playwright: Clicking on launch button  for {text} ")
        self.page.locator(HomePageSelectors.SERVICE_TITLE.format(text)).click()
        return self

    def click_on_private_cloud_business_edition_arrow(self):
        """
        Click on the private Cloud business edition arrow
        :return: Private Cloud business page
        """
        log.info(f"Playwright: click on private_cloud_business_edition_arrow")
        self.page.wait_for_selector(
            HomePageSelectors.PRIVATE_CLOUD_BUSINESS_EDITION_ARROW
        )
        self.pw_utils.click_selector(
            HomePageSelectors.PRIVATE_CLOUD_BUSINESS_EDITION_ARROW
        )
        return PrivateCloudBusinessEnterprise(self.page, self.cluster)

    def click_on_recommended_tab(self):
        """
        Clicks on Recommended tab under Featured Services on Home page
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on Recommended tab")
        self.page.locator(HomePageSelectors.RECOMMENDED_TAB).click()
        return self

    def click_on_compute_tab(self):
        """
        Clicks on Compute tab under Featured Services on Home page
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on Compute tab")
        self.page.locator(HomePageSelectors.COMPUTE_TAB).click()
        return self

    def click_on_networking_tab(self):
        """
        Clicks on Networking tab under Featured Services on Home page
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on Networking tab")
        self.page.locator(HomePageSelectors.NETWORKING_TAB).click()
        return self

    def click_on_workloads_tab(self):
        """
        Clicks on Workloads tab under Featured Services on Home page
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on Workloads tab")
        self.page.locator(HomePageSelectors.WORKLOADS_TAB).click()
        return self

    def click_on_management_and_governance_tab(self):
        """
        Clicks on Management & Governance tab under Featured Services on Home page
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on Management & Governance tab")
        self.page.locator(HomePageSelectors.MANAGEMENT_AND_GOVERNANCE).click()
        return self

    def should_have_region_of_featured_services(self, text):
        """
        Verify region of featured services on Home page
        text: param (required) to compare text
        :return: self reference.
        """
        expect(
            self.page.locator(HomePageSelectors.REGION_FEATURED_SERVICES)
        ).to_have_text(text)
        return self

    def should_have_home_page_title(self, text="GreenLake"):
        """
        User should be able to see the HPE Green Lake Badge title in the Homepage
        :param: text: (optional)
        :return: self reference
        """
        self.page.wait_for_load_state()
        expect(
            self.page.locator(HomePageSelectors.GREEN_LAKE_BADGE_TITLE)
        ).to_contain_text(text)
        return self

    def should_have_recent_services_empty(
        self,
        text="You haven't launched any services yet. View the services catalog to get started.",
    ):
        """
        verify “Recent Services in home page where it will be empty”
        text: param (optional) to compare text
        :return:self reference
        """
        self.page.wait_for_load_state()
        expect(
            self.page.locator(HomePageSelectors.RECENT_SERVICE_EMPTY_TEXT, has_text=text)
        )
        return self

    def should_have_recent_services_title(self, text="Recent Services"):
        """
        verify 'Recent Services' title in home page
        param: text (optional)
        :return: self reference
        """
        expect(self.page.locator(HomePageSelectors.RECENT_SERVICES_TITLE)).to_have_text(
            text
        )
        return self
