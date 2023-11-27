import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.locations.ui.create_location_page import (
    CreateLocationPage,
)
from hpe_glcp_automation_lib.libs.locations.ui.location_details_page import (
    LocationDetails,
)
from hpe_glcp_automation_lib.libs.locations.ui.locators import LocationsPageSelectors

log = logging.getLogger(__name__)


class Locations(HeaderedPage):
    """
    Locations page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Locations page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Locations page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/locations"

    def search_location(self, location_name):
        """
        Search Locations
        :param location_name: Name of location to search for
        return: self reference
        """
        log.info(f"Playwright: Opens Create Location page")
        self.page.fill(LocationsPageSelectors.SEARCH_FIELD, location_name)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_create_location(self):
        """
        Open Create Location page
        return: Create Location page object class
        """
        log.info(f"Playwright: Opens Create Location page")
        self.page.click(LocationsPageSelectors.CREATE_LOCATION_BTN)
        return CreateLocationPage(self.page, self.cluster)

    def open_location_details(self, location_name):
        """
        Open Location Details page
        :param location_name: Name of the location
        return: Location Details page object class
        """
        log.info(f"Playwright: Opens Location Details page")
        self.search_location(location_name)
        location_uuid = self.page.locator(
            LocationsPageSelectors.LOCATION_LIST_ITEM_UUID
        ).get_attribute("data-testid")
        self.page.click(
            LocationsPageSelectors.LOCATION_LIST_ITEM_DROP_BTN.format(location_name)
        )
        self.page.click(LocationsPageSelectors.LOCATION_OPTION_VIEW_BTN)
        return LocationDetails(self.page, self.cluster, location_uuid)

    def delete_location(self, location_name):
        """
        Delete Location by the name
        :param location_name: Name of the location
        return: self reference
        """
        log.info(f"Playwright: Delete Location {location_name}")
        self.page.click(
            LocationsPageSelectors.LOCATION_LIST_ITEM_DROP_BTN.format(location_name)
        )
        self.page.click(LocationsPageSelectors.LOCATION_OPTION_DELETE_BTN)
        self.page.click(LocationsPageSelectors.POPUP_CONFIRM_BTN)
        self.page.locator(LocationsPageSelectors.POPUP_CONFIRM_TITLE).wait_for(
            state="hidden"
        )
        return self

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of Location page object.
        """
        log.info("Playwright: check that title has matched text in location page.")
        expect(self.page.locator(LocationsPageSelectors.PAGE_TITLE)).to_be_visible()
        return self
