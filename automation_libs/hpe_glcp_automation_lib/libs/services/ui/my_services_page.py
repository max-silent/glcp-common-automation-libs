"""
Services -  page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_services_navigable_page import (
    SideMenuNavigablePage,
)
from hpe_glcp_automation_lib.libs.services.ui.launched_service import LaunchedService
from hpe_glcp_automation_lib.libs.services.ui.locators import MyServicesSelectors

log = logging.getLogger(__name__)


class MyServices(HeaderedPage, SideMenuNavigablePage):
    """
    MyServices page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Services page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize MyServices page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/services/my-services"

    def wait_for_loaded_list(self, ensure_not_empty=True):
        """Wait for list of Services is not empty and loader spinner is not present on the page.

        :return: current instance of MyServices page object.
        """
        log.info("Playwright: Wait for Services list is loaded.")
        self.pw_utils.wait_for_selector(
            MyServicesSelectors.LOADER_SPINNER, timeout=5000, timeout_ignore=True
        )
        self.page.locator(MyServicesSelectors.LOADER_SPINNER).wait_for(state="hidden")
        if ensure_not_empty:
            self.page.wait_for_selector(
                MyServicesSelectors.LAUNCH_BTN_TEMPLATE.format("")
            )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def choose_region_filtered_out(self, region):
        """Choose the Region for {region}.

        :param region: expected region to match with the region in dropdown.
        :return : current instance of MyServices page object.
        """
        log.info(f"Playwright: Filter out displayed services by region '{region}'.")
        self.pw_utils.select_drop_down_element(
            MyServicesSelectors.REGIONS_DROPDOWN, region, "option"
        )
        return self

    def switch_to_grid_view(self):
        """Switch view of displayed applications to grid.

        :return: current instance of MyServices page object.
        """
        log.info("Playwright: Switch My Services page to grid view.")
        self.page.locator(MyServicesSelectors.GRID_VIEW_BTN).click()
        return self

    def switch_to_list_view(self):
        """Switch view of displayed applications to list.

        :return: current instance of MyServices page object.
        """
        log.info("Playwright: Switch My Services page to list view.")
        self.page.locator(MyServicesSelectors.LIST_VIEW_BTN).click()
        return self

    def click_launch_btn(self, service_name, region=None):
        """Click on launch button for related Service.
        If 'region' not specified - first application matched to 'service_name' will be launched.

        :param service_name: name of service to launch.
        :param region: region of service to launch.
        :return: new instance of LaunchedService page object.
        """
        log.info(
            f"Playwright: Launch service '{service_name}' provisioned at '{region if region else 'Any'}' region."
        )
        button_label_text = service_name
        if region:
            button_label_text += ", " + region.lower().replace(" ", "-")
        self.page.locator(
            MyServicesSelectors.LAUNCH_BTN_TEMPLATE.format(button_label_text)
        ).first.click()
        return LaunchedService(self.page)

    def should_have_service(self, service_name, region=None):
        """Check that specified deployed Service is present at the page.

        :param service_name: name of service to check.
        :param region: region of service to check.
        :return: current instance of MyServices page object.
        """
        log.info(
            f"Playwright: Check service '{service_name}' at '{region if region else 'Any'}' region is displayed."
        )
        button_label_text = service_name
        if region:
            button_label_text += ", " + region.lower().replace(" ", "-")
        expect(
            self.page.locator(
                MyServicesSelectors.LAUNCH_BTN_TEMPLATE.format(button_label_text)
            ).first  # several elements may be resolved if 'region' was not specified
        ).to_be_visible()
        return self

    def should_contain_text_in_title(self, text):
        """Check that expected text is present as part of the heading page title.

        :param text: expected text to be contained in title.
        :return: current instance of MyServices page object.
        """
        log.info(f"Playwright: Check that title contains text '{text}' in Services page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyServicesSelectors.HEADING_PAGE_TITLE)).to_contain_text(
            text
        )
        return self

    def should_have_text_in_title(self, text):
        """Check that expected text matches with the heading page title.

        :param text: expected text to match with the text in title.
        :return: current instance of MyServices page object.
        """
        log.info(f"Playwright: Check that title has text '{text}' in Services page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyServicesSelectors.HEADING_PAGE_TITLE)).to_have_text(
            text
        )
        return self

    def should_be_list_view(self):
        """
        Checks that list view is currently selected
        :return: current instance of MyServices page object
        """
        log.info(f"Playwright: Check that list view is selected in Services page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyServicesSelectors.GRID_VIEW_BTN)).to_be_visible()
        return self

    def should_be_grid_view(self):
        """
        Checks that grid view is currently selected
        :return: current instance of MyServices page object
        """
        log.info(f"Playwright: Check that grid view is selected in Services page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyServicesSelectors.LIST_VIEW_BTN)).to_be_visible()
        return self

    def should_have_region_selected(self, region):
        """
        Checks that region drop down has the specified region selected
        :params region: expected text to show up in region drop down
        :return: current instance of MyServices page object
        """
        log.info(f"Playwright: Check that {region} is selected in Services page.")
        self.pw_utils.save_screenshot(self.test_name)
        if region != "All Regions":
            expect(
                self.page.locator(MyServicesSelectors.REGION_TITLE.format(region))
            ).to_be_visible()
        else:
            expect(self.page.locator(MyServicesSelectors.REGIONS_DROPDOWN)).to_have_value(
                region
            )
        return self
