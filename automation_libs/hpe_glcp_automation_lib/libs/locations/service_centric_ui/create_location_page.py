import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.service_centric_ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.locations.service_centric_ui.locators import (
    CreateLocationPageSelectors,
)

log = logging.getLogger(__name__)


class CreateLocationPage(BasePage):
    """
    Location page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Create Location page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Create Location page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/locations/create-location"

    def should_have_location_title(self, text="Create Location"):
        """
        Verify Location Page title
        param: text in title (optional)
        return: self reference
        """
        log.info(
            f"Playwright: check that wizard heading with '{text}' text is displayed."
        )
        self.page.wait_for_load_state()
        expect(
            self.page.locator(CreateLocationPageSelectors.SERVICE_PAGE_HEADING)
        ).to_have_text(text)
        return self
