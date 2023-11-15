import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.app_prov.ui.locators import InstalledAppsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class InstalledApplications(HeaderedPage):
    """
    Installed Apps pages object model
    """

    def __init__(self, page: Page, cluster: str, app_uuid: str):
        """
        Initialize with page, cluster and app_uuid
        :param page: Page
        :param cluster: cluster under test url
        :param app_uuid: application uuid
        """
        log.info(
            f"Playwright: Initialize the installed application page for '{app_uuid}'."
        )
        super().__init__(page, cluster)
        self.url = f"{cluster}/applications/installed-apps/{app_uuid}"

    def remove_region(self, region: str):
        """
        Remove the installed application for the given region
        :param region: region
        :return self: instance
        """
        log.info(f"Playwright: remove the application for the region: '{region}'")
        self.pw_utils.save_screenshot(self.test_name)
        _region = "-".join(region.lower().split())
        self.pw_utils.click_selector(
            InstalledAppsSelectors.APP_ACTION_BTN_TEMPLATE.format(_region)
        )
        self.page.locator(InstalledAppsSelectors.ACTION_REMOVE_REGION).click()
        self.page.wait_for_selector(InstalledAppsSelectors.REMOVE_APPS_MODAL)
        self.page.locator(InstalledAppsSelectors.TERM_CHECKBOX).click()
        self.page.locator(InstalledAppsSelectors.REMOVE_REGION_BTN).click()
        return self

    def get_app_name(self):
        """
        Returns the APP Name
        :return str
        """
        return self.page.locator(InstalledAppsSelectors.APP_NAME_HEADER).inner_text()

    def should_have_region(self, region: str):
        """
        Checks the application exists in specific region
        :param region: region
        :return self: instance
        """
        log.info(
            f"Playwright: checking for the application has installed in the region: '{region}'"
        )
        _region = "-".join(region.lower().split())
        expect(
            self.page.locator(
                InstalledAppsSelectors.LAUNCH_APPS_BTN_TEMPLATE.format(_region)
            )
        ).to_be_visible()
        return self

    def wait_for_loaded_state(self):
        """
        Wait till page is loaded and loading spinner is not present.
        :return: current instance of Installed App page object.
        """
        log.info("Playwright: wait for Installed app is loaded.")
        self.page.wait_for_url(self.url)
        self.pw_utils.wait_for_selector(
            InstalledAppsSelectors.APP_SPINNER, timeout=5000, timeout_ignore=True
        )
        self.page.locator(InstalledAppsSelectors.APP_SPINNER).wait_for(state="hidden")
        return self
