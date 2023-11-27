"""
Identity page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authz.ui.roles_page import Roles
from hpe_glcp_automation_lib.libs.authz.ui.rrp_page import ResourceRestrictionPolicy
from hpe_glcp_automation_lib.libs.authz.ui.users_page import Users
from hpe_glcp_automation_lib.libs.commons.ui.locators import IdentitySelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class Identity(HeaderedPage):
    """
    Identity page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize identity page object
        :param page: page
        :param cluster: cluster url
        """
        log.info("Initialize Identity page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/identity"

    def open_users(self):
        """
        Navigate to Users page by clicking on tile on identity page
        returns: Users page object
        """
        log.info(f"Playwright: navigate to Users page")
        self.page.locator(IdentitySelectors.CARD_USERS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Users(self.page, self.cluster)

    def open_roles_and_permissions(self):
        """
        Navigate to Roles & Permissions page by clicking on tile on identity page
        returns: Roles and permission Page Object
        """
        log.info(f"Playwright: navigate to Roles & Permissions page")
        self.page.locator(IdentitySelectors.CARD_ROLES).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Roles(self.page, self.cluster)

    def open_resource_restriction_policy(self):
        """
        Navigate to Resource Restriction Policy page by clicking on tile on identity page
        returns: Resource Restriction Policy Page Object
        """
        log.info(f"Playwright: navigate to Resource Restriction Policy page")
        self.page.locator(IdentitySelectors.CARD_SCOPE_GROUPS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return ResourceRestrictionPolicy(self.page, self.cluster)

    def open_assign_roles(self):
        """
        Open Assign Roles Modal by clicking on Assign a Role button on Identity page
        returns: Object (self reference)
        """
        log.debug(f"Playwright: Open Assign Roles popup")
        self.page.locator(IdentitySelectors.ASSIGN_ROLE_BTN).click()
        return self

    def click_on_cancel_button(self):
        """
        Click on Cancel button on Assign a Role pop-up on Identity page
        returns: Object (self reference) .
        """
        log.debug(f"Clicking on cancel button")
        self.page.locator(IdentitySelectors.CANCEL_BTN).click()
        return self

    def should_have_assign_role_popup_title_visible(self):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of Identity page object.
        """
        log.debug(f"Playwright: check that title is present on assign roles popup.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(
            self.page.locator(IdentitySelectors.HEADING_POPUP_PAGE_TITLE)
        ).to_be_visible()
        return self

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of identity page object.
        """
        log.info("Playwright: check that title has matched text in identity page.")
        expect(self.page.locator(IdentitySelectors.PAGE_TITLE)).to_be_visible()
        return self
