import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.locations.ui.locators import (
    LocationDetailsPageSelectors,
)

log = logging.getLogger(__name__)


class LocationDetails(HeaderedPage):
    """
    Location Details page object model class.
    """

    def __init__(self, page: Page, cluster: str, location_uuid):
        """
        Initialize Location Details page object.
        :param page: page.
        :param cluster: cluster url.
        :param location_uuid: location UUID.
        """
        log.info("Initialize Location Details page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/locations/{location_uuid}"

    def go_back_to_locations(self):
        """
        Navigate back to Locations page
        """
        log.info(f"Playwright: Navigating to Locations page")
        self.page.click(LocationDetailsPageSelectors.BACK_TO_LOCATIONS_BTN)
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_name_in_title(self, location_name):
        """
        Verifying presence of the location name in the header
        :param location_name: Name of the location
        :return: self reference
        """
        expect(
            self.page.locator(LocationDetailsPageSelectors.LOCATION_DETAILS_HEADER)
        ).to_have_text(location_name)
        return self
