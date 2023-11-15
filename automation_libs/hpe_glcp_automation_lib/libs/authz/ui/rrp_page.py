"""
This file holds functions for Resource Restriction Policy page
"""

import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authz.ui.locators import RRPSelectors
from hpe_glcp_automation_lib.libs.authz.ui.rrp_details_page import RRPDetails
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class ResourceRestrictionPolicy(HeaderedPage):
    """
    Resource Restriction Policy page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Resource Restriction Policy page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Resource Restriction Policy page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/identity/scope-groups"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of resource restriction policy page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.page.wait_for_selector(
            RRPSelectors.TABLE_ROWS, state="visible", strict=False
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text):
        """
        Enter text to search field.
        :param search_text: search_text.
        :return: current instance of resource restriction policy page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' in roles.")
        self.pw_utils.enter_text_into_element(RRPSelectors.SEARCH_FIELD, search_text)
        self.wait_for_loaded_table()
        return self

    def navigate_to_rrp_details_page(self, rrp_name, rrp_id):
        """
        Return rrp details object for given rrp name.
        :param rrp_name: rrp name
        :params rrp_id: rrp id
        :return RRPDetails: RRP details page object
        """
        self.search_for_text(rrp_name)
        self.pw_utils.click_selector(RRPSelectors.OPEN_RRP_TEMPLATE.format(rrp_name))
        return RRPDetails(self.page, self.cluster, rrp_id)

    def create_resource_restriction_policy(
        self, rrp_name, application_name, resource_name="Group Scope", resource_opt=None
    ):
        """
        Create resource restriction policy

        :param rrp_name: resource restriction policy name
        :param application_name: application name for which rrp is made
        :param resource_name: resource name of the application
        :param resource_opt: resource option under a resource (Optional)
        :return: current instance of resource restriction policy page object.
        """
        log.info(
            f"Playwright: Create {rrp_name} rrp having access to {application_name} with {resource_name}."
        )
        self.page.locator(RRPSelectors.CREATE_RRP_BTN).click()
        self.page.locator(RRPSelectors.RRP_NAME_INPUT).fill(rrp_name)
        self.page.locator(RRPSelectors.NEXT_BUTTON).click()
        self.page.locator(
            RRPSelectors.APPLICATION_NAME_TEMPLATE.format(application_name)
        ).click()
        self.page.locator(RRPSelectors.NEXT_BUTTON).click()
        self.page.locator(RRPSelectors.ADD_RESOURCES_BTN).click()
        self.page.wait_for_selector(RRPSelectors.RESOURCE_DIALOG_TITLE)
        while not self.page.locator(
            RRPSelectors.RESOURCE_NAME_TEMPLATE.format(resource_name)
        ).first.is_visible():
            self.page.locator(RRPSelectors.RESOURCE).click()
        self.page.locator(
            RRPSelectors.RESOURCE_NAME_TEMPLATE.format(resource_name)
        ).click()
        if resource_opt:
            if self.pw_utils.wait_for_selector(
                RRPSelectors.REOSOURCE_OPT_LOADER,
                state="visible",
                timeout_ignore=True,
                timeout=5000,
            ):
                self.page.locator(RRPSelectors.REOSOURCE_OPT_LOADER).first.wait_for(
                    state="hidden"
                )
                self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_selector(
                RRPSelectors.RESOURCE_OPT_TEMPLATE.format(resource_opt)
            )
            checkbox_locator = self.page.locator(
                RRPSelectors.RESOURCE_OPT_TEMPLATE.format(resource_opt)
            )
            if checkbox_locator.locator("svg[viewBox]").is_hidden():
                checkbox_locator.click()
        self.pw_utils.click_selector(RRPSelectors.ADD_BTN)
        self.pw_utils.click_selector(RRPSelectors.NEXT_BUTTON)
        self.pw_utils.click_selector(RRPSelectors.FINISH_BUTTON)
        self.wait_for_loaded_table()
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def delete_resource_restriction_policy(self, rrp_name):
        """
        Delete resource restriction policy

        :param rrp_name: resource restriction policy name
        :return: current instance of resource restriction policy page object.
        """
        log.info(f"Playwright: Delete {rrp_name} rrp.")
        self.search_for_text(rrp_name)
        self.page.wait_for_selector(RRPSelectors.OPEN_RRP_TEMPLATE.format(rrp_name))
        self.page.locator(RRPSelectors.OPEN_RRP_TEMPLATE.format(rrp_name)).click()
        self.page.locator(RRPSelectors.RRP_ACTION_BUTTON).click()
        self.page.locator(RRPSelectors.DELETE_ACTION).click()
        self.page.locator(RRPSelectors.DELETE_POLICY_BUTTON).click()
        self.page.wait_for_selector(RRPSelectors.DELETE_CONFIRMATION_TITLE)
        self.page.locator(RRPSelectors.DELETE_POLICY_BUTTON).first.click()
        self.wait_for_loaded_table()
        self.pw_utils.save_screenshot(self.test_name)
        return self
