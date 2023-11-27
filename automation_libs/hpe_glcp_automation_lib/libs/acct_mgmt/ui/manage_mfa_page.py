"""
Mange MFA page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import ManageMFASelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class ManageMFA(HeaderedPage):
    """
    Manage MFA page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Manage Mfa page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/account-details/manage-mfa"

    def set_mfa_status(self, status="Enabled"):
        """
        Set MFA
        :Param: Status of MFA - Can be Enabled/Disabled
        :return: instance of the Manage_mfa page object
        """
        log.info(f"Set MFA status to {status}")
        if self.page.locator(
            ManageMFASelectors.MFA_STATUS_TEXT_TEMPLATE.format(status)
        ).is_visible():
            raise ValueError(f"MFA is already {status}")
        self.pw_utils.click_selector(ManageMFASelectors.EDIT_DETAILS_BTN)
        self.pw_utils.click_selector(ManageMFASelectors.MFA_GOOGLE_AUTH_TOGGLE_BTN)
        self.page.locator(ManageMFASelectors.SAVE_CHANGES_BTN).click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def close_mfa_notifiction_popup(self):
        """
        Close MFA Notification
        :return: current instance of the manage_mfa page object
        """
        self.page.locator(ManageMFASelectors.MFA_NOTIFICATION_CLOSE_BTN).click()
        return self

    def should_have_notification(self, text):
        """
        Check the notifications message for setting up MFA
        :param:text : Notification message
        :return: Current instance of the Manage_Mfa Page Object
        """
        log.info(f"Playwright: Check the MFA Notification-{text}")
        expect(
            self.page.locator(ManageMFASelectors.MFA_NOTIFICATION_TEMPLATE.format(text))
        ).to_be_visible()
        return self

    def should_have_mfa(self, status="Enabled"):
        """
        Check the status of MFA whether it is enabled or disabled
        :param:status: Status of the MFA - Enabled/Disabled
        :return: current instance of the manage_mfa object
        """
        log.info(f"Playwright: Check the {status} status of MFA")
        expect(
            self.page.locator(ManageMFASelectors.MFA_STATUS_TEXT_TEMPLATE.format(status))
        ).to_be_visible()
        return self
