"""
NotificationPage page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.notifications.ui.locators import (
    NotificationPageSelectors,
)

log = logging.getLogger(__name__)


class NotificationPage(HeaderedPage):
    """
    Notification page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize notification page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize notification page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/notifications"

    def should_have_title(self, text):
        """
        Checking the title exists
        """
        expect(
            self.page.locator(NotificationPageSelectors.NOTIFICATION_TITLE)
        ).to_have_text(text)
        return self
