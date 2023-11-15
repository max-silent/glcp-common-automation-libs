"""
This file holds functions for Resource Restriction Policy Details page
"""

import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authz.ui.locators import RRPDetailsSelectors
from hpe_glcp_automation_lib.libs.authz.ui.user_data import RRPDetailsData
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class RRPDetails(HeaderedPage):
    """
    Resource Restriction Policy details page object model class.
    """

    def __init__(self, page: Page, cluster: str, rrp_id: str):
        """
        Initialize Resource Restriction Policy details page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Resource Restriction Policy details page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/identity/scope-groups/{rrp_id}"

    def navigate_to_rrp_page(self):
        """
        Return to the previous page.
        """
        log.info(f"Playwright: navigate back to RRP page from RRP details")
        self.page.locator(RRPDetailsSelectors.BACK_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def edit_resource_restriction_policy_details(
        self, rrp_data: RRPDetailsData = RRPDetailsData
    ):
        """
        Edit RRP details.
        :param rrp_data: rrp data for editing the rrp (name and description)
        :return: current instance of rrp details page object.
        """
        log.info(f"Playwright: Edit rrp details")
        self.pw_utils.click_selector(RRPDetailsSelectors.EDIT_BUTTON)
        self.page.locator(RRPDetailsSelectors.EDIT_NAME_INPUT_BOX).fill(rrp_data.name)
        self.page.locator(RRPDetailsSelectors.EDIT_DESC_INPUT_BOX).fill(
            rrp_data.description
        )
        self.pw_utils.click_selector(RRPDetailsSelectors.EDIT_DETAILS_SAVE_BTN)
        self.pw_utils.save_screenshot(self.test_name)
        return self
