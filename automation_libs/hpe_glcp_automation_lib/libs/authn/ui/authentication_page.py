"""
This file holds functions for Authentication page
"""

import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authn.ui.locators import AuthenticationPageSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class Authentication(HeaderedPage):
    """
    Authentication Page object methods
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Authentication page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/authentication"

    def claim_domain(
        self,
        domain,
        metadata_url,
        rec_user_pwd,
        rec_contact_email,
        hpe_ccs_attribute,
        first_name=None,
        last_name=None,
        idle_session_timeout=None,
    ):
        """
        Claim domain on glcp

        :param domain: domain to claim
        :param metadata_url: idp metadata url
        :param rec_user_pwd: recovery user password
        :param rec_contact_email: recovery contact email
        :param hpe_ccs_attribute: hpe greenlake / aruba brownfield attribute
        :param first_name: first name
        :param last_name: last name
        :param session_timeout: idle session timeout value
        :return self: instance
        """
        log.info(f"Playwright: Claim {domain} domain")
        self.page.locator(AuthenticationPageSelectors.ADD_SAML_CONNECTION_BTN).click()
        self.page.locator(AuthenticationPageSelectors.DOMAIN_NAME_INPUT).fill(domain)
        self.page.locator(AuthenticationPageSelectors.CONTINUE_BTN).click()
        self.page.locator(AuthenticationPageSelectors.METADATA_URL_OPT).click()
        self.page.locator(AuthenticationPageSelectors.METADATA_URL_INPUT).fill(
            metadata_url
        )
        self.page.locator(AuthenticationPageSelectors.VALIDATE_URL_BTN).click()
        entity_id = self.page.locator(AuthenticationPageSelectors.ENTITY_ID_INPUT)
        expect(entity_id).not_to_be_empty()
        if not self.page.locator(
            AuthenticationPageSelectors.FORM_GLOBAL_ERROR
        ).is_visible():
            self.page.locator(AuthenticationPageSelectors.NEXT_BTN).click()
        else:
            self.pw_utils.save_screenshot(self.test_name)
            return self

        saml_attribute_input = self.page.locator(
            AuthenticationPageSelectors.SAML_ATTRIBUTE_NAME_INPUT
        )
        hpe_greenlake_attribute = self.page.locator(
            AuthenticationPageSelectors.HPE_GREENLAKE_ATTRIBUTE
        )
        self.page.wait_for_selector(AuthenticationPageSelectors.SAML_ATTRIBUTE_NAME_INPUT)
        if saml_attribute_input.is_enabled and hpe_greenlake_attribute.is_enabled():
            self.pw_utils.select_drop_down_element(
                AuthenticationPageSelectors.SAML_ATTRIBUTE_NAME_INPUT,
                "NameId",
                "option",
                exact_match=True,
            )
            self.page.locator(AuthenticationPageSelectors.HPE_GREENLAKE_ATTRIBUTE).fill(
                hpe_ccs_attribute
            )
            if first_name:
                self.page.locator(AuthenticationPageSelectors.FIRST_NAME_INPUT).fill(
                    first_name
                )
            if last_name:
                self.page.locator(AuthenticationPageSelectors.LAST_NAME_INPUT).fill(
                    last_name
                )
            if idle_session_timeout:
                self.page.locator(
                    AuthenticationPageSelectors.IDLE_SESSION_TIMEOUT_VALUE
                ).fill(idle_session_timeout)

        self.page.locator(AuthenticationPageSelectors.NEXT_BTN).click()
        recovery_user_email = self.page.locator(
            AuthenticationPageSelectors.RECOVERY_USER_EMAIL
        ).inner_text()
        log.info(f"Recovery user for {domain} domain is {recovery_user_email}")
        self.page.locator(AuthenticationPageSelectors.RECOVERY_USER_PWD).fill(
            rec_user_pwd
        )
        self.page.locator(AuthenticationPageSelectors.RECOVERY_USER_CONTACT_EMAIL).fill(
            rec_contact_email
        )
        self.page.locator(AuthenticationPageSelectors.NEXT_BTN).click()
        self.page.locator(AuthenticationPageSelectors.FINISH_BTN).click()
        self.page.locator(AuthenticationPageSelectors.EXIT_BTN).click()
        self.page.locator(AuthenticationPageSelectors.SKIP_EMAIL_BTN).click()
        self.pw_utils.save_screenshot(self.test_name)
        return self

    def delete_domain(self, domain):
        """
        Delete claimed domain on glcp

        :param domain: claimed domain
        :return self: instance
        """
        log.info(f"Playwright: Delete {domain} domain")
        domain_tile = self.page.locator(
            AuthenticationPageSelectors.DOMAIN_TILE_TEMPLATE.format(domain)
        )
        domain_tile.locator(AuthenticationPageSelectors.ACTION_BTN).click()
        self.page.locator(AuthenticationPageSelectors.DELETE_OPT).click()
        self.page.locator(AuthenticationPageSelectors.DELETE_BTN).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.wait_for_selector(AuthenticationPageSelectors.DELETE_DOMAIN_MSG)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(AuthenticationPageSelectors.DELETE_DOMAIN_MSG_BTN).click()
        return self

    def validate_saml_attributes(self, domain, entity_id, sign_on_url, app_ids=None):
        """
        Validate saml attributes of claimed domain on glcp

        :param domain: claimed domain
        :param entity_id: entity url of the cluster
        :param sign_on_url: single sign on url
        :param app_ids: installed applications ids
        return self: instance
        """
        log.info(f"Playwright: Validating SAML attributes")
        domain_tile = self.page.locator(
            AuthenticationPageSelectors.DOMAIN_TILE_TEMPLATE.format(domain)
        )
        domain_tile.locator(AuthenticationPageSelectors.ACTION_BTN).click()
        self.page.locator(AuthenticationPageSelectors.VIEW_SAML_ATTRIBUTE_OPT).click()
        expect(
            self.page.locator(AuthenticationPageSelectors.ENTITY_ID_VALUE)
        ).to_contain_text(entity_id)
        expect(
            self.page.locator(AuthenticationPageSelectors.SIGN_ON_URL_VALUE)
        ).to_contain_text(sign_on_url)
        if app_ids:
            for app_id in app_ids:
                expect(
                    self.page.locator(
                        AuthenticationPageSelectors.APP_ID_VALUE.format(app_id)
                    )
                ).to_be_visible()
        self.page.locator(AuthenticationPageSelectors.CLOSE_BTN).click()
        return self

    def should_have_text_in_title(self):
        """
        Check that expected text matches with the heading page title.
        :return: current instance of Authentication page object.
        """
        log.info("Playwright: check that title has matched text in Authentication page.")
        expect(self.page.locator(AuthenticationPageSelectors.PAGE_TITLE)).to_be_visible()
        return self
