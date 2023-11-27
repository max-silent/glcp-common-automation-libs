"""
Subscription Details page object model.
"""

import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import DevSubscriptionDetailsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.navigation.side_menu_devices_navigable_page import (
    SideMenuNavigablePage,
)

log = logging.getLogger(__name__)


class SubscriptionDetails(HeaderedPage, SideMenuNavigablePage):
    """
    Subscription Details page object model.
    """

    def __init__(self, page: Page, cluster: str, key: str):
        """Initialize with page and cluster.

        :param page: Page.
        :param cluster: cluster under test url.
        """
        log.info("Initialize Device Subscriptions page object.")
        super().__init__(page, cluster)
        self.url = f"{cluster}/devices/subscriptions/{key}"

    def should_have_subscription_details_header(self):
        """
        Checks for presence of Subscription Details page header.
        :return: current instance of Subscription Details page object.
        """
        log.info("Playwright: checking for subscription details page header.")
        expect(
            self.page.locator(DevSubscriptionDetailsSelectors.SUBSCRIPTION_INFO_HEADER)
        ).to_be_visible()
        return self
