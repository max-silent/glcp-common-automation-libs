"""
Manage account page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.account_type_page import AccountType
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.api_page import APIpage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.ip_access_rules_page import IPAccessRules
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.order_history_page import OrderHistory
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.usage_reporting_page import UsageReporting
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.workspace_details_page import (
    WorkspaceDetails,
)
from hpe_glcp_automation_lib.libs.adi.ui.activate_devices_page import ActivateDevices
from hpe_glcp_automation_lib.libs.audit_logs.ui.audit_logs_page import AuditLogs
from hpe_glcp_automation_lib.libs.authn.ui.authentication_page import Authentication
from hpe_glcp_automation_lib.libs.cds.ui.usage_reporting import Usage_Reporting
from hpe_glcp_automation_lib.libs.commons.ui.identity_page import Identity
from hpe_glcp_automation_lib.libs.commons.ui.locators import ManageAccountSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.locations.ui.locations_page import Locations
from hpe_glcp_automation_lib.libs.sm.ui.device_subscriptions import DeviceSubscriptions

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
        self.page.locator(ManageAccountSelectors.CARD_AUDIT_LOGS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return AuditLogs(self.page, self.cluster)

    def open_usage_reporting(self):
        """
        Navigate to Usage Reporting page by clicking on tile on manage account page.
        :return: new instance of Usage Logs page object.
        """
        log.info(f"Playwright: navigate to Usage Report page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_USAGE_REPORTING)
        self.page.locator(ManageAccountSelectors.CARD_USAGE_REPORTING).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Usage_Reporting(self.page, self.cluster)

    def open_identity_and_access(self):
        """
        Navigate to Identity & Access page by clicking on tile on manage account page.
        :return: new instance of Identity & Access page object.
        """
        log.info(f"Playwright: navigate to Identity & Access page")
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
        self.page.locator(ManageAccountSelectors.MANAGE_ACCOUNT_TYPE_BUTTON).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return AccountType(self.page, self.cluster)

    def open_activate(self):
        """
        Navigate to Activate page by clicking on tile on manage account page.
        :return: new instance of ActivateDevices page object.
        """
        log.info(f"Playwright: navigate to Activate Devices page")
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

    def open_locations(self):
        """
        Navigate to Locations page by clicking on tile on manage account page.
        :return: new instance of Locations page object.
        """
        log.info(f"Playwright: navigate to Locations page")
        self.page.locator(ManageAccountSelectors.CARD_LOCATION).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Locations(self.page, self.cluster)

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
        self.page.locator(ManageAccountSelectors.CARD_WORKSPACE_DETAILS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return WorkspaceDetails(self.page, self.cluster)

    def open_api(self):
        """
        Navigate to API page by clicking on tile on manage account page.
        :return: new instance of api page page object.
        """
        log.info(f"Playwright: navigate to API page")
        self.page.locator(ManageAccountSelectors.CARD_API).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return APIpage(self.page, self.cluster)

    def open_ip_access_rules(self):
        """
        Navigate to ip access rules page by clicking on tile on manage account page.
        :return: new instance of ip access rules page object.
        """
        log.info(f"Playwright: navigate to ip access rules page")
        self.page.locator(ManageAccountSelectors.CARD_IP_ACCESS_RULES).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return IPAccessRules(self.page, self.cluster)

    def open_usage_reporting(self):
        """
        Navigate to usage reporting page by clicking on tile on manage account page.
        :return: new instance of usage reporting page object.
        """
        log.info(f"Playwright: navigate to usage reporting page")
        self.page.locator(ManageAccountSelectors.CARD_USAGE_REPORTING).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return UsageReporting(self.page, self.cluster)

    def open_order_history(self):
        """
        Navigate to Order History page by clicking on tile on manage account page.
        :return: new instance of Order History page object.
        """
        log.info(f"Playwright: navigate to order history page")
        self.page.locator(ManageAccountSelectors.CARD_ORDER_HISTORY).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return OrderHistory(self.page, self.cluster)

    def should_have_manage_workspace_title(self):
        """
        Check that the heading page title os visible on the Manage Workspace page.
        :return: current instance of Manage Workspacepage object.
        """
        log.debug(f"Playwright: check that Manage Workspace page has valid title.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(ManageAccountSelectors.MANAGE_WORKSPACE_TITLE)
        ).to_be_visible()
        return self

    def should_have_workspace_type(self, text):
        """Check Workspace Type description.

        :param text: expected Workspace Type to match.
        return: self reference
        """
        log.debug("Playwright: check Workspace Type description.")
        expect(self.page.locator(ManageAccountSelectors.WORKSPACE_TYPE)).to_have_text(
            text
        )
        return self
