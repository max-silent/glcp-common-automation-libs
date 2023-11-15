import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.silvercreek.onprem.setup_wizard.locators import (
    WizardScreenSelectors,
)

log = logging.getLogger(__name__)


class WizardScreen:
    """
    WizardScreen page object model class.
    """

    def __init__(self, ip, page: Page):
        """
        WizardScreen page object model class.
        :param page: page.
        """
        log.info("Initialize WizardScreen page object")
        self.page = page
        self.pw_utils = PwrightUtils(page)
        self.ip = ip

    def wait_for_spinner_to_disappear(self):
        """
        Waits for spinner to disappear
        returns: Current instance of WizardScreen class
        """
        log.info("Waiting for spinner to disappear")
        self.pw_utils.wait_for_selector(
            WizardScreenSelectors.SPINNER,
            state="visible",
            timeout_ignore=True,
            timeout=5000,
        )
        self.page.locator(WizardScreenSelectors.SPINNER).wait_for(state="hidden")
        return self

    def check_secure_ntp_flag(self):
        """
        Check 'Enable Secure NTP' flag.
        :return: self
        """
        log.info("Playwright: check 'Enable Secure NTP'.")
        self.page.locator(WizardScreenSelectors.SECURE_NTP_TOGGLE).check()
        return self

    def uncheck_secure_ntp_flag(self):
        """
        Uncheck 'Enable Secure NTP' flag.
        :return: self
        """
        log.info("Playwright: uncheck 'Enable Secure NTP'.")
        self.page.locator(WizardScreenSelectors.SECURE_NTP_TOGGLE).uncheck()
        return self

    def enter_unsecure_primary_ntp_server(self, ip):
        """
        Enter the primary unsecure ntp server
        :param ip: IP of the NTP server
        :return: Current instance of WizardScreen class
        """
        self.page.locator(WizardScreenSelectors.PRIMARY_SERVER_IP_TEXTBOX).fill(ip)
        return self

    def enter_secure_primary_ntp_server(self, ip, key_type, key_id, psk):
        """
        Enter the primary secure ntp server
        :param ip: IP of the secure NTP server
        :param key_type: Key type of the secure NTP server
        :param key_id: Key ID of the secure NTP server
        :param psk: psk of the NTP secure server
        :return: Current instance of WizardScreen class
        """
        log.info("Entering secure primary NTP server details")
        self.page.locator(WizardScreenSelectors.PRIMARY_SERVER_IP_TEXTBOX).fill(ip)
        self.page.locator(WizardScreenSelectors.KEY_TYPE_DROPDOWN).click()
        self.page.get_by_text(key_type, exact=True).click()
        self.page.locator(WizardScreenSelectors.KEYID_TEXTBOX).fill(key_id)
        self.page.locator(WizardScreenSelectors.PSK_TEXTBOX).fill(psk)
        return self

    def enter_cluster_vip(self, fqdn):
        """
        Fills cluster VIP Details
        :param fqdn: cluster details
        :return: current instance of WizardScreen class
        """
        log.info("Entering cluster VIP details")
        self.page.locator(WizardScreenSelectors.FQDN_TEXTAREA).fill(fqdn)
        self.page.locator(WizardScreenSelectors.VIRTUAL_IP_TEXTAREA).click()
        log.info(f"Entered {fqdn} in cluster vip details")
        return self

    def enter_cli_user_setup(self, cli_password):
        """
        Fills CLI Password details
        :param cli_password: password
        :return: current instance of WizardScreen class
        """
        log.info(f"Entering #### in password details")
        self.page.locator(WizardScreenSelectors.CLI_PASSWORD).fill(cli_password)
        self.page.locator(WizardScreenSelectors.CLI_RETYPE_PASSWORD_TEXTAREA).fill(
            cli_password
        )
        return self

    def enter_admin_password_gui(self, password):
        """
        Fills Admin Password details
        :param password: admin password
        :return: current instance of WizardScreen class
        """
        log.info(f"Entering and ##### in admin password for GUI")
        self.page.locator(WizardScreenSelectors.PASSWORD_TEXTAREA).fill(password)
        self.page.locator(WizardScreenSelectors.RETYPE_PASSWORD_TEXTAREA_COMMON).fill(
            password
        )
        return self

    def enter_cluster_private_network(self, pod_ip_range, service_ip_range):
        """
        Fills Cluster Private Network details
        :param pod_ip_range: pod ip range for network
        :param service_ip_range: service ip range for network
        :return: current instance of WizardScreen class
        """
        log.info(
            f"Entering {pod_ip_range} and {service_ip_range} in Cluster Private Network Details"
        )
        self.page.locator(WizardScreenSelectors.POD_IP_RANGE_TEXTAREA).fill(pod_ip_range)
        self.page.locator(WizardScreenSelectors.SERVICE_IP_AREA_TEXT_RANGE).fill(
            service_ip_range
        )
        return self

    def check_proxy_server_setup(self):
        """
        Checkbox for proxy server setup
        :return: current instance of WizardScreen class
        """
        log.info(f"Checkbox clicking proxy server setup")
        self.page.locator(WizardScreenSelectors.PROXY_CHECKBOX).check()
        return self

    def enter_proxy_server_details(self, proxy_server, port, username, password):
        """
        Fills Proxy server details
        :param proxy_server: proxy server name
        :param port: proxy server port
        :param username: username
        :param password: password
        :return: current instance of WizardScreen class
        """
        log.info(
            f"Entering {proxy_server}, {port}, {username} and ##### in Cluster Private Network Details"
        )
        self.page.locator(WizardScreenSelectors.PROXY_SERVER_TEXTAREA).fill(proxy_server)
        self.page.locator(WizardScreenSelectors.PROXY_PORT_TEXTAREA).fill(port)
        self.page.locator(WizardScreenSelectors.PROXY_USERNAME).fill(username)
        self.page.locator(WizardScreenSelectors.PROXY_PASSWORD).fill(password)
        self.page.locator(WizardScreenSelectors.PROXY_RETYPE_TEXT).fill(password)
        return self

    def check_smtp_proxy_server_setup(self):
        """
        Checkbox for SMTP server setup
        :return: Current instance of WizardScreen class
        """
        log.info(f"Clicking checkbox SMTP server setup")
        self.page.locator(WizardScreenSelectors.SMTP_CHECKBOX).check()
        return self

    def enter_smtp_server_details(self, ip, port, username, password, encryption="SSL"):
        """
        Fills SMTP Server Details
        :param ip: ip address for the smtp server
        :param port: port for the smtp server
        :param username: username for the smtp server
        :param password: password for the smtp server
        :param encryption: encryption type (default value is SSL)
        :return: Current instance of WizardScreen class
        """
        log.info(
            f"Entering {ip}, {port}, {username} and ##### in Cluster Private Network Details"
        )
        self.page.locator(WizardScreenSelectors.PORT_IP_TEXTAREA).fill(ip)
        self.page.locator(WizardScreenSelectors.PORT_TEXTAREA).fill(port)
        self.page.locator(WizardScreenSelectors.USERNAME_TEXTAREA).fill(username)
        self.page.locator(WizardScreenSelectors.PASSWORD_TEXTAREA).fill(password)
        self.page.locator(WizardScreenSelectors.RETYPE_PASSWORD_TEXTAREA).fill(password)
        if encryption:
            self.page.locator(WizardScreenSelectors.ENCRYPTION_DROPDOWN).click()
            self.page.get_by_role("option", name=encryption).click()
        return self

    def finish_setup(self, decline_confirmation=False):
        """
        Finish setup at the end
        :param decline_confirmation: True for clicking no or False for yes
        :return: Current instance of WizardScreen class
        """
        self.page.get_by_role("button", name="FINISH").click()
        if decline_confirmation:
            self.page.get_by_role("button", name="No").click()
        else:
            self.page.get_by_role("button", name="Yes").click()
        return self

    def get_progress_percent(self):
        """
        :return: Progress percentage text for onprem setup
        """
        log.info("Get progress percent")
        return int(
            self.page.get_attribute(
                WizardScreenSelectors.PROGRESS_PERCENTAGE, "aria-valuenow"
            )
        )

    def get_primary_progress_text(self):
        """
        :return: Primary progress text for onprem setup
        """
        log.info("Get primary progress text")
        return self.page.locator(WizardScreenSelectors.PROGRESS_TEXT).text_content()

    def get_secondary_progress_text(self):
        """
        :return: Secondary progress text for onprem setup
        """
        log.info("Get secondary progress text")
        return self.page.locator(
            WizardScreenSelectors.PROGRESS_TEXT_SECONDARY
        ).text_content()

    def click_on_next_button(self):
        """
        Clicks on NEXT button and recursively clicks on Next button until next page is reached
        :return: Current instance of WizardScreen class
        """
        log.info("Navigating to next page")
        self.page.get_by_role("button", name="NEXT").click()
        return self

    def click_on_previous_button(self):
        """
        Clicks on PREVIOUS button
        :return: Current instance of WizardScreen class
        """
        log.info("Clicking on PREVIOUS button")
        self.page.get_by_role("button", name="PREVIOUS").click()
        return self

    def logout(self):
        """
        Logs out of application
        :return: Current instance of WizardScreen class
        """
        log.info("Clicking on Logout button")
        self.page.locator(WizardScreenSelectors.LOGOUT_BUTTON).click()
        self.page.wait_for_load_state()
        return self

    def open(self):
        """
        Navigates to home page for onprem
        :return: Current instance of WizardScreen class
        """
        log.info(f"Playwright: open onprem home page at IP: '{self.ip}'.")
        self.page.goto(f"https://{self.ip}:8443", timeout=0)
        self.page.locator(WizardScreenSelectors.LOGOUT_BUTTON).is_visible()
        return self

    def should_have_virtual_ip_resolved(self):
        """
        Verify virtual IP resolved according to given FQDN and is green
        return: current instance of WizardScreen class
        """
        log.info("Checking if virtual IP is resolved according to given FQDN")
        resolve_check_circle = self.page.locator(
            WizardScreenSelectors.GREEN_RESOLVED_TICK
        )
        expect(resolve_check_circle).to_be_visible()
        log.info("Virtual IP resolved according to given FQDN")
        return self
