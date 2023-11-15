"""
Manage account page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.service_centric_ui.account_type_page import (
    AccountType,
)
from hpe_glcp_automation_lib.libs.acct_mgmt.service_centric_ui.workspace_details_page import (
    WorkspaceDetails,
)
from hpe_glcp_automation_lib.libs.adi.service_centric_ui.activate_devices_page import (
    ActivateDevices,
)
from hpe_glcp_automation_lib.libs.audit_logs.service_centric_ui.audit_logs_page import (
    AuditLogs,
)
from hpe_glcp_automation_lib.libs.authn.service_centric_ui.authentication_page import (
    Authentication,
)
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.headered_page import (
    HeaderedPage,
)
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.identity_page import Identity
from hpe_glcp_automation_lib.libs.commons.service_centric_ui.locators import (
    ManageAccountSelectors,
)
from hpe_glcp_automation_lib.libs.sm.service_centric_ui.device_subscriptions import (
    DeviceSubscriptions,
)

log = logging.getLogger(__name__)


class ManageAccount(HeaderedPage):
    """
    Manage account page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize manage account page object
        :param page: page
        :param cluster: cluster url
        """
        log.info("Initialize ManageAccount page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account"

    def open_audit_logs(self):
        """
        Navigate to Audit Logs page by clicking on tile on manage account page.
        :return: new instance of Audit Logs page object.
        """
        log.info(f"Playwright: navigate to Audit Logs page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_AUDIT_LOGS)
        self.page.locator(ManageAccountSelectors.CARD_AUDIT_LOGS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return AuditLogs(self.page, self.cluster)

    def open_identity_and_access(self):
        """
        Navigate to Identity & Access page by clicking on tile on manage account page.
        :return: new instance of Identity & Access page object.
        """
        log.info(f"Playwright: navigate to Identity & Access page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_IDENTITY_AND_ACCESS)
        self.page.locator(ManageAccountSelectors.CARD_IDENTITY_AND_ACCESS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Identity(self.page, self.cluster)

    def open_subscriptions(self):
        """
        Navigate to Subscriptions page by clicking on tile on manage account page.
        :return: new instance of DeviceSubscriptions page object.
        """
        log.info(f"Playwright: navigate to Device Subscriptions page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_SUBSCRIPTIONS)
        self.page.locator(ManageAccountSelectors.CARD_SUBSCRIPTIONS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return DeviceSubscriptions(self.page, self.cluster)

    def open_account_type(self):
        """
        Navigate to Account Type page.
        :return: instance of Account Type page
        """
        log.info("Playwright: navigate to Account Type page")
        self.page.wait_for_selector(
            ManageAccountSelectors.MANAGE_ACCOUNT_TYPE_BUTTON
        ).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return AccountType(self.page, self.cluster)

    def open_activate(self):
        """
        Navigate to Activate page by clicking on tile on manage account page.
        :return: new instance of ActivateDevices page object.
        """
        log.info(f"Playwright: navigate to Activate Devices page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_ACTIVATE)
        self.page.locator(ManageAccountSelectors.CARD_ACTIVATE).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return ActivateDevices(self.page, self.cluster)

    def open_authentication(self):
        """
        Navigate to Authentication page by clicking on tile on manage account page.
        :return: new instance of Authentication page object.
        """
        log.info(f"Playwright: navigate to Authentication page")
        self.page.locator(ManageAccountSelectors.CARD_AUTHENTICATION).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Authentication(self.page, self.cluster)

    def get_pcid(self):
        """
        :return: Current logged in account platform customer ID value
        """
        return self.page.locator(
            ManageAccountSelectors.PCID_VALUE_SELECTOR
        ).text_content()

    def open_workspace_details(self):
        """
        Navigate to workspace details page by clicking on tile on manage account page.
        :return: new instance of WorkspaceDetails page object.
        """
        log.info(f"Playwright: navigate to  page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_WORKSPACE_DETAILS)
        self.page.locator(ManageAccountSelectors.CARD_WORKSPACE_DETAILS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return WorkspaceDetails(self.page, self.cluster)

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of Manage page object.
        """
        log.info(
            f"Playwright: check that title has matched text '{text}' in Manage page."
        )
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(ManageAccountSelectors.MANAGE_ACCOUNT_TITLE)
        ).to_have_text(text)
        return self

    def should_have_workspace_type(self, text):
        """Check Workspace Type description.

        :param text: expected text to match.
        return: self reference
        """
        log.info("Playwright: check Workspace Type description.")
        expect(self.page.locator(ManageAccountSelectors.WORKSPACE_TYPE)).to_have_text(
            text
        )
        return self
