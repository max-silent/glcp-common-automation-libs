class LoginPageSelectors:
    EMAIL_ID_PATH = "id=idp-discovery-username"
    NEXT_BTN_PATH = "id=idp-discovery-submit"
    PASSWD_PATH = "id=okta-signin-password"
    SUBMIT_PATH = "id=okta-signin-submit"
    USERNAME_ERROR = "p:text-is('This field cannot be left blank')"
    SIGN_IN_ERROR = "p:text-is('Unable to sign in')"
    PASSWD_ERROR = "p:text-is('Please enter a password')"
    NEED_HELP_SIGING_IN = "a:text-is('Need help signing in?')"
    FRGT_PASSWD = "a:text-is('Forgot password?')"
    ACC_RCVRY_USERNAME = "id=account-recovery-username"
    RESET_VIA_EMAIL_BTN = "a:text-is('Reset via Email')"
    BACK_TO_SIGN_BTN = "a:text-is('Back to sign in')"
    SSO_SIGN_IN = "[data-se='social-auth-general-idp-button']"
    SSO_EMAIL_INPUT = "data-testid=emailInput"
    NEXT_BUTTON = "data-testid=nextButton"
    OKTA_EMAIL_INPUT = "input[name='identifier']"
    OKTA_PASSCODE_INPUT = "input[name='credentials.passcode']"
    OKTA_NEXT_BTN = "input[value='Next']"
    OKTA_PASSWORD_SELECT = "div[data-se='okta_password']"
    OKTA_SIGN_IN_BTN = "input[value='Sign in']"
    OKTA_FORM_TITLE = 'h2:has-text("Verify with Google Authenticator")'
    VERIFY_BUTTON = "input[value='Verify']"
    REMEMBER_ME = '[data-se-for-name="remember"]'


class ResetUserPasswordSelectors:
    ACCOUNT_RECOVERY_USERNAME = "input[id='account-recovery-username']"
    NEED_HELP = '[data-se="needhelp"]'
    FORGOT_PASSWORD = '[data-se="forgot-password"]'
    REST_VIA_EMAIL = '[data-se="email-button"]'
    NEW_PASSWD_PATH = "input[name='newPassword']"
    REPEAT_PASSWD_PATH = "input[name='confirmPassword']"
    RESET_PASSWD_BUTTON = "input[value='Reset Password']"


class AuthenticationPageSelectors:
    ADD_SAML_CONNECTION_BTN = (
        '[data-testid="set-saml-connection"], [data-testid="set-samlsso-connection"]'
    )
    DOMAIN_NAME_INPUT = "data-testid=domain-name-input"
    CONTINUE_BTN = "data-testid=continue-btn"
    METADATA_URL_OPT = "label[for='Metadata URL']"
    METADATA_URL_INPUT = "data-testid=metadata-url-input"
    VALIDATE_URL_BTN = "data-testid=validate-url-button"
    ENTITY_ID_INPUT = "data-testid=entity-id-input"
    FORM_GLOBAL_ERROR = "data-testid=form-global-error"
    NEXT_BTN = "data-testid=button-next"
    SAML_ATTRIBUTE_NAME_INPUT = "[data-testid=field-name-dropdown]"
    HPE_GREENLAKE_ATTRIBUTE = "[data-testid=hpe-ccs-attribute-input]"
    FIRST_NAME_INPUT = "[data-testid=first-name-input]"
    LAST_NAME_INPUT = "[data-testid=last-name-input]"
    IDLE_SESSION_TIMEOUT_VALUE = "[data-testid=idle-session-timeout-value-input]"
    RECOVERY_USER_EMAIL = "[data-testid=user-recovery-email]"
    RECOVERY_USER_PWD = "[data-testid=edit-contact-name-input-recovery-pass]"
    RECOVERY_USER_CONTACT_EMAIL = "[data-testid=edit-contact-name-input-email]"
    FINISH_BTN = "[data-testid=button-finish]"
    EXIT_BTN = "data-testid=exit-modal-btn"
    SKIP_EMAIL_BTN = "data-testid=skip-btn"
    BACK_TO_SSO = 'button:has-text("Single Sign-On (SSO)")'
    DOMAIN_TILE_TEMPLATE = "[data-testid^='app-tile']:has-text('{}')"
    ACTION_BTN = "[data-testid='multipleactions-action-btn']"
    DELETE_OPT = 'button:has-text("Delete")'
    DELETE_BTN = "data-testid=delete-btn"
    DELETE_DOMAIN_MSG = "data-testid=status-good-notification"
    DELETE_DOMAIN_MSG_BTN = '[data-testid="status-good-notification"] button'
    VIEW_SAML_ATTRIBUTE_OPT = 'button:has-text("View SAML Attribute")'
    ENTITY_ID_VALUE = (
        '[data-testid="app-name"]:has-text("Entity ID") ~ [data-testid="app-id"]'
    )
    SIGN_ON_URL_VALUE = (
        '[data-testid="app-name"]:has-text("Sign-On URL") ~ [data-testid="app-id"]'
    )
    APP_ID_VALUE = "[data-testid=\"table\"] > tbody > tr:has(span:text-is('{}'))"
    CLOSE_BTN = '[data-testid="close-btn"]'
    DOWNLOAD_METADATA_FILE = '[data-testid="download-metadata-button"]'


class EnrollSelectors:
    """
    Class for Enroll Page Locators
    """

    OKTA_SETUP_BTN = "[data-se='OKTA_VERIFY_PUSH'] a:text-is('Setup')"
    GOOGLE_AUTH_SETUP_BTN = "[data-se='GOOGLE_AUTH'] a:text-is('Setup')"
    ANDROID_RADIO_BTN = "label:text-is('Android')"
    APPLE_RADIO_BTN = "label:text-is('iPhone')"
    BACK_TO_FACTOR_LIST = "a:text-is('Back to factor list')"
    BACK_TO_SETTINGS = "span:text-is('Back to Settings')"
    NEXT_BTN = "input[value='Next']"
    CANT_SCAN = "[data-se='manual-setup']:text-is(\"Can't scan?\")"
    ACTIVATION_TYPE_DROPDOWN = "span[data-se='o-form-input-activationType']"
    ACTIVATION_TYPE_OPTION = "li:text-is('Setup manually without push notification')"
    SHARED_SECRET_FIELD = "input[name='sharedSecret']"
    OKTA_PUSH_NEXT_BTN = "[data-se='next-button']:text-is('Next')"
    PASSCODE_INPUT_FIELD = "input[name='passCode']"
    VERIFY_BTN = "input[value='Verify']"
    FINISH_BTN = "input[value='Finish']"
    LOGIN_OTP_FIELD = "input[name='answer']"
