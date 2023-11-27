"""
Homepage page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.switch_account_page import SwitchAccount
from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory
from hpe_glcp_automation_lib.libs.authz.ui.users_page import Users
from hpe_glcp_automation_lib.libs.commons.ui.locators import HomePageSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.locations.ui.create_location_page import (
    CreateLocationPage,
)
from hpe_glcp_automation_lib.libs.services.ui.launched_service import LaunchedService
from hpe_glcp_automation_lib.libs.services.ui.my_services_page import MyServices
from hpe_glcp_automation_lib.libs.services.ui.service_catalog_page import ServiceCatalog
from hpe_glcp_automation_lib.libs.services.ui.service_details_page import ServiceDetails

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

    def open_return_msp_account(self):
        """
        Navigates to MSP Account homepage
        return:current instance of homepage object
        """
        self.page.locator(HomePageSelectors.RETURN_TO_MSP_ACCT_BTN).click()
        return self

    def open_service_details(self, service_name):
        """
        Click on Service plate with corresponding service name under 'Featured Services' section.
        service_name: Name of service to open
        :return: instance of ServiceDetails page object.
        """
        log.info(f"Playwright: Clicking on {service_name} Featured Service Plate")
        self.page.locator(
            HomePageSelectors.SERVICE_PLATE_TEMPLATE.format(service_name)
        ).click()
        return ServiceDetails(
            page=self.page, cluster=self.cluster, service_name=service_name
        )

    def launch_recent_service_by_name(self, service_name, region=None):
        """
        Launch Service by name from 'recent services' area
        :param: service_name: Name of the service
        :param: region: Region to launch service for
        :return: self reference
        """
        log.info(
            f"Playwright: Launch {service_name} from 'Recent Services' for {region} region"
        )
        self.page.locator(
            HomePageSelectors.LAUNCH_RECENT_SERVICE_TEMPLATE.format(service_name)
        ).click()

        if self.page.locator(HomePageSelectors.LAUNCH_POPUP_REGION_DROPDOWN).is_visible():
            if region:
                self.pw_utils.select_drop_down_element(
                    HomePageSelectors.LAUNCH_POPUP_REGION_DROPDOWN,
                    region,
                    element_role="option",
                )
            else:
                self.pw_utils.select_drop_down_element_by_index(
                    HomePageSelectors.LAUNCH_POPUP_REGION_DROPDOWN,
                    HomePageSelectors.LAUNCH_POPUP_REGION_DROPDOWN_LIST_ITEM,
                    1,
                )
            self.page.locator(HomePageSelectors.LAUNCH_POPUP_LAUNCH_BTN).click()
            self.page.locator(HomePageSelectors.LAUNCH_POPUP_LAUNCH_BTN).wait_for(
                state="hidden"
            )
        elif region:
            raise ValueError("Regions list for selection is not available.")
        return LaunchedService(self.page)

    def launch_first_recent_service(self):
        """
        Launches first service with the first region under Recent Services on Home page
        :return: instance of LaunchedService page object.
        """
        log.info("Playwright: Launch First service for first region from Recent Services")
        self.page.locator(HomePageSelectors.RECENT_SERVICES_LAUNCH).first.click()
        self.pw_utils.select_drop_down_element_by_index(
            HomePageSelectors.LAUNCH_POPUP_REGION_DROPDOWN,
            HomePageSelectors.LAUNCH_POPUP_REGION_DROPDOWN_LIST_ITEM,
            1,
        )
        self.page.locator(HomePageSelectors.LAUNCH_POPUP_LAUNCH_BTN).click()
        self.page.locator(HomePageSelectors.LAUNCH_POPUP_LAUNCH_BTN).wait_for(
            state="hidden"
        )
        return LaunchedService(self.page)

    def click_on_recommended_tab(self):
        """
        Clicks on Recommended tab under Featured Services on Home page
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on Recommended tab")
        self.page.locator(HomePageSelectors.RECOMMENDED_TAB).click()
        return self

    def click_on_private_cloud_tab(self):
        """
        Click on the private cloud tab
        :return: self reference
        """
        log.info("Playwright: Click on Private Cloud tab")
        self.page.locator(HomePageSelectors.PRIVATE_CLOUD_TAB).click()
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

    def click_on_featured_services_tab(self, service):
        """
        Clicks on a given tab under Featured Services on Home page
        :param: service: name of the tab under featured services
        :return: current instance of Homepage page object.
        """
        log.info(f"Playwright: Click on {service} tab")
        service = service.upper().replace(" ", "_")
        self.page.locator(
            HomePageSelectors.FEATURED_SERVICE_TAB_TEMPLATE.format(service)
        ).click()
        return self

    def click_on_view_catalog(self):
        """
        Clicks on "View Catalog" link under "Featured Services" section on Home page
        :return: CatalogPage
        """
        log.info(f"Playwright: Clicking 'View Catalog' link.")
        self.page.locator(HomePageSelectors.VIEW_CATALOG_LINK).click()
        return ServiceCatalog(page=self.page, cluster=self.cluster)

    def click_quick_action_add_users_or_assign_roles_link(self):
        """
        Click on the "Add Users/ Assign Roles" link from "Quick Actions" section under Home page
        :return: Users page instance
        """
        log.info("Playwright: Click on 'Quick Action: Add Users/ Assign Roles' link")
        self.page.locator(HomePageSelectors.ADD_USER_OR_ASSIGN_ROLES_LINK_PATH).click()
        return Users(self.page, self.cluster)

    def click_quick_action_add_service_subscriptions_link(self):
        """
        Clicks on "Add Service Subscriptions" link under "Quick Actions" section on Home page
        :return: MyServices page instance
        """
        log.info(f"Playwright: Click on 'Quick Action: Add Service Subscriptions' link")
        self.page.locator(HomePageSelectors.ADD_SERVICE_SUBSCRIPTIONS_LINK).click()
        return MyServices(page=self.page, cluster=self.cluster)

    def click_quick_action_add_device_link(self):
        """
        Clicks on "Add Device" link under "Quick Actions" section on Home page
        :return: DevicesInventory page instance
        """
        log.info(f"Playwright: Clicking on 'Quick Action: Add Device' link")
        self.page.locator(HomePageSelectors.ADD_DEVICE_LINK).click()
        return DevicesInventory(self.page, self.cluster)

    def click_quick_action_create_location_link(self):
        """
        Clicks on "Create Location" link under "Quick Actions" section on Home page
        :return: LocationPage instance
        """
        log.info(f"Playwright: Clicking 'Quick Action: Create Location' link.")
        self.page.wait_for_selector(HomePageSelectors.CREATE_LOCATION_LINK).click()
        return CreateLocationPage(self.page, self.cluster)

    def click_quick_action_manage_workspace_link(self):
        """
        Click on "Manage Workspace" link from Quick Actions section under Home page
        """
        log.info("Playwright: Click on 'Quick Action: Manage Workspace Link")
        self.page.locator(HomePageSelectors.MANAGE_WORKSPACE_LINK).click()
        # Note: instance of ManageAccount page object cannot be returned due to the circular import

    def click_quick_switch_workspace_link(self):
        """
        Click on "Switch Workspace" link from Quick Actions section under Home page
        :return: SwitchAccount instance
        """
        log.info("Playwright: Click on 'Quick Action: Switch Workspace Link")
        self.page.locator(HomePageSelectors.SWITCH_WORKSPACE_LINK).click()
        return SwitchAccount(self.page, self.cluster)

    def click_on_dismiss_link(self):
        """
        Clicks on dismiss link
        :return: self reference
        """
        self.page.locator(HomePageSelectors.DISMISS_LINK).click()
        return self

    def click_my_services_link(self):
        """
        Clicking on my services link
        """
        self.page.locator(HomePageSelectors.MY_SERVICES_LINK).click()
        return MyServices(self.page, self.cluster)

    def switch_recent_services_to_list_view(self):
        """
        Click on switch recent services view to show list view if grid view.
        :return: Home page instance
        """
        if (self.page.locator(HomePageSelectors.LIST_VIEW_BTN)).is_visible():
            self.page.locator(HomePageSelectors.LIST_VIEW_BTN).click()
        return self

    def switch_recent_services_to_grid_view(self):
        """
        Click on switch recent services view to show grid view if list view.
        :return: Home page instance
        """
        if (self.page.locator(HomePageSelectors.GRID_VIEW_BTN)).is_visible():
            self.page.locator(HomePageSelectors.GRID_VIEW_BTN).click()
        return self

    def should_have_recent_services_empty(self):
        """
        verify “Recent Services in home page where it will be empty”
        :return:self reference
        """
        expect(
            self.page.locator(HomePageSelectors.EMPTY_RECENT_SERVICE_PLACEHOLDER)
        ).to_be_visible()
        return self

    def should_have_recent_services_title(self):
        """
        verify 'Recent Services' title in home page
        :return: self reference
        """
        expect(self.page.locator(HomePageSelectors.RECENT_SERVICES_TITLE)).to_be_visible()
        return self

    def should_have_quick_action_card(self):
        """Verify existence of quick actions card.

        :return: self reference
        """
        log.info("Playwright: checking the presence of Quick actions card")
        expect(self.page.locator(HomePageSelectors.QUICK_ACTIONS_CARD)).to_be_visible()
        return self

    def should_have_link_in_quick_actions(self, text):
        """Verify link in quick actions card.

        :return: self reference.
        """
        log.info(f"Playwright: checking link with text '{text}' in quick actions card.")
        expect(
            self.page.locator(HomePageSelectors.QUICK_ACTION_LINK_TEMPLATE.format(text))
        ).to_be_visible()
        return self

    def should_have_recommended_tab(self):
        """
        Checking if page has recommended tab
        :return: Home page instance
        """
        expect(self.page.locator(HomePageSelectors.RECOMMENDED_TAB)).to_be_visible()
        return self

    def should_have_private_cloud_tab(self):
        """
        Checking if page has private cloud tab
        :return: Home page instance
        """
        expect(self.page.locator(HomePageSelectors.PRIVATE_CLOUD_TAB)).to_be_visible()
        return self

    def should_have_networking_tab(self):
        """
        Checking if page has networking tab
        :return: Home page instance
        """
        expect(self.page.locator(HomePageSelectors.NETWORKING_TAB)).to_be_visible()
        return self

    def should_have_workloads_tab(self):
        """
        Checking if page has workloads tab
        :return: Home page instance
        """
        expect(self.page.locator(HomePageSelectors.WORKLOADS_TAB)).to_be_visible()
        return self

    def should_have_management_and_governance_tab(self):
        """
        Checking if page has management and governance tab
        :return: Home page instance
        """
        expect(
            self.page.locator(HomePageSelectors.MANAGEMENT_AND_GOVERNANCE)
        ).to_be_visible()
        return self

    def should_not_have_quick_action_create_location_link(self):
        """
        expects the create location link in quick actions to not be visible
        :return: current instance of Homepage page object
        """
        expect(
            self.page.locator(HomePageSelectors.CREATE_LOCATION_LINK)
        ).not_to_be_visible()
        return self

    def should_have_developer_portal_tile_under_learn_more(self):
        """
        Checking the developer tile under learn more
        :return: current instance of Homepage page object
        """
        expect(
            self.page.locator(HomePageSelectors.LEARN_MORE_DEVELOPER_CARD)
        ).to_be_visible()
        return self

    def should_have_whats_new_tile_under_learn_more(self):
        """
        Checking the what's new in hpe tile under learn more
        :return: current instance of Homepage page object
        """
        expect(
            self.page.locator(HomePageSelectors.LEARN_MORE_WHATS_NEW_CARD)
        ).to_be_visible()
        return self

    def should_have_test_drive_tile_under_learn_more(self):
        """
        Checking the test drive tile under learn more
        :return: current instance of Homepage page object
        """
        expect(
            self.page.locator(HomePageSelectors.LEARN_MORE_TEST_DRIVE_CARD)
        ).to_be_visible()
        return self

    def should_have_my_services_link(self):
        """
        Checking the presence of My services link
        :return: current instance of Homepage page object
        """
        expect(self.page.locator(HomePageSelectors.MY_SERVICES_LINK)).to_be_visible()
        return self

    def should_have_catalog_link(self):
        """
        Checking the presence of catalog link
        :return: current instance of Homepage page object
        """
        expect(self.page.locator(HomePageSelectors.VIEW_CATALOG_LINK)).to_be_visible()
        return self

    def should_have_service(self, service_name):
        """
        Checking service under featured services in home page
        :param service_name: Service name
        :return: current instance of Homepage page object
        """
        log.info(
            f"Playwright: Check that service '{service_name}' is present under "
            f"featured services."
        )
        expect(
            self.page.locator(
                HomePageSelectors.SERVICE_PLATE_TEMPLATE.format(service_name)
            )
        ).to_be_visible()
        return self

    def should_have_app_in_recent_services(self, service_name):
        """
        Verify app in 'Recent Services' in home page
        :param service_name: Service name
        :return: current instance of Homepage page object
        """
        expect(
            self.page.locator(
                HomePageSelectors.RECENT_SERVICES_APP_DIV_TEMPLATE.format(service_name)
            )
        ).to_be_visible()
        return self

    def should_have_category_in_featured_services(self, category):
        """
        Verifies that a card with the given category is present in featured services
        :param category: The given category that is to be verified
        :return: current instance of Homepage page object
        """
        expect(
            self.page.locator(
                HomePageSelectors.FEATURED_SERVICE_CARD_SUBHEADER_TEMPLATE.format(
                    category
                )
            ).first
        ).to_be_visible()
        return self

    def should_have_recent_services_view_switch_state(self, list_view=True):
        """
        Validates visibility for view type button under 'Recent Services' section.
        :param list_view: (Bool) with possible values as 'Grid' or 'List'
        :return: current instance of Homepage page object
        """
        log.info(
            f"Playwright: Verifying {list_view} button visibility from 'Recent Services' "
        )
        if list_view:
            expect(self.page.locator(HomePageSelectors.LIST_VIEW_BTN)).to_be_visible()
        else:
            expect(self.page.locator(HomePageSelectors.GRID_VIEW_BTN)).to_be_visible()
        return self
