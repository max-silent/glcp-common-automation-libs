"""Contains locators required by onprem classes/methods"""


class WizardScreenSelectors:
    # Locators for ClusterSetup
    SECURE_NTP_TOGGLE = (
        "label:has(>span:text-is('Enable Secure NTP'))>div[class='mat-slide-toggle-bar']"
    )
    PRIMARY_SERVER_IP_TEXTBOX = "#mat-input-0"
    KEY_TYPE_DROPDOWN = "#mat-select-1"
    KEYID_TEXTBOX = "#mat-input-19"
    PSK_TEXTBOX = "#mat-input-20"
    SPINNER = "#cdk-overlay-0 > mat-progress-spinner"

    # Locators for Common Configuration
    FQDN_TEXTAREA = "[placeholder='FQDN']"
    VIRTUAL_IP_TEXTAREA = "input[placeholder='VIRTUAL IP']"
    CLI_PASSWORD = "[placeholder='CLI PASSWORD']"
    CLI_RETYPE_PASSWORD_TEXTAREA = "[id='mat-input-8']"
    RETYPE_PASSWORD_TEXTAREA_COMMON = "[id='mat-input-12']"
    POD_IP_RANGE_TEXTAREA = "[placeholder='POD IP Range']"
    SERVICE_IP_AREA_TEXT_RANGE = "[placeholder='SERVICE IP RANGE']"
    PROXY_CHECKBOX = "#mat-checkbox-1 .mat-checkbox-inner-container"
    PROXY_SERVER_TEXTAREA = "[placeholder='PROXY SERVER']"
    PROXY_PORT_TEXTAREA = "[placeholder='PORT']"
    PROXY_USERNAME = "[id='mat-input-21']"
    PROXY_PASSWORD = "[id='mat-input-22']"
    PROXY_RETYPE_TEXT = "[id='mat-input-23']"
    GREEN_RESOLVED_TICK = (
        "mat-icon[mattooltip='IP Address has been resolved successfully']"
    )

    # Locators for Additional Setup
    SMTP_CHECKBOX = "[id='mat-checkbox-2']"
    PORT_IP_TEXTAREA = "[placeholder='HOST NAME OR IP ADDRESS']"
    PORT_TEXTAREA = "[placeholder='SMTP PORT']"
    USERNAME_TEXTAREA = "[placeholder='SMTP USERNAME']"
    PASSWORD_TEXTAREA = "[placeholder='PASSWORD']"
    RETYPE_PASSWORD_TEXTAREA = "[placeholder='RETYPE PASSWORD']"
    ENCRYPTION_DROPDOWN = "[mat-select[formcontrolname='encryption']]"
    PROGRESS_TEXT = "#customDialog > div > span:nth-child(1)"
    PROGRESS_TEXT_SECONDARY = "#customDialog > div > span:nth-child(2)"
    PROGRESS_PERCENTAGE = "[class='mat-progress-bar mat-primary']"

    # Common locators
    LOGOUT_BUTTON = "a.logout-link"
