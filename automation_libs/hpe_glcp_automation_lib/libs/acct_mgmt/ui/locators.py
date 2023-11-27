class ChooseAccountSelectors:
    SEARCH_BOX = '[data-testid="accounts-search-box"]'
    COMPANY_NAME_TEMPLATE = '[data-testid^="heading-company-name"]:text-is("{}")'
    GO_TO_ACCOUNT = '[data-testid="tile-action-btn"]'
    GO_TO_ACCOUNT_TEMPLATE = "[data-testid^='tile-account']:has(:text-is('{}')) [data-testid='tile-action-btn']"
    CREATE_ACCT_BTN = '[data-testid="create-account-button"]'
    BACK_TO_SIGN_IN_BTN = '[data-testid="back-to-sign-in-btn"]'
    WELCOME_HEADER = "h1:text-is('Welcome to HPE GreenLake')"
    WELCOME_SUBHEADER = '[data-testid="text-create-account-subheader"]'
    ACCOUNTS_COUNT = "[data-testid='text-customer-accounts-count']"
    ACCOUNT_TILES = "[data-testid='tile-action-btn']"
    PAGINATION_BAR = "[data-testid='pagination']"
    WELCOME_HPE_GLE_HEADER = '[data-testid="heading-choose-account-header"]'


class CreateUserSelectors:
    """
    Class holding user creation locators
    """

    SIGNUP_TXT = "id=custom-signup"
    INPUT_EMAIL = 'input[name="email"]'
    INPUT_PASSWORD = 'input[name="password"]'
    FIRST_NAME = 'input[name="firstName"]'
    LAST_NAME = 'input[name="lastName"]'
    BUSINESS_NAME = 'input[name="businessName"]'
    STREET_ADDRESS = 'input[name="streetAddress"]'
    STREET_ADDRESS2 = 'input[name="streetAddress2"]'
    INPUT_CITY = 'input[name="city"]'
    STATE_PROVINCE = 'input[name="stateOrProvince"]'
    POSTAL_CODE = 'input[name="postalCode"]'
    CREATE_ACCT_BTN = '[data-testid="create-account-button"]'
    SETUP_ACCT_COMP_NAME = '[data-testid="set-up-account-company-name-input"]'
    SETUP_ACCT_PAGE = "/onboarding/set-up-account"
    SELECT_COUNTRY = '[placeholder="Select Country or Region"]'
    COUNTRY_MENY_ITEM_ROLE = "menuitem"
    SELECT_LANG_DROP = "text={}"
    SELECT_LANG = 'input[name="selectLanguage"]'
    SELECT_TZ = 'input[name="selectTimezone"]'
    SELECT_TZ1 = "text={}"
    INPUT_PHONE = 'input[name="phoneNumber"]'
    EMAIL_CTCT_PREF = "#emailContactPreference div"
    PHONE_CTCT_PREF = "#phoneContactPreference div"
    LEGAL_CHECK_BOX = (
        ".StyledCheckBox__StyledCheckBoxContainer-sc-1dbk5ju-1 >"
        " div > .StyledBox-sc-13pk1d4-0"
    )
    CREATE_ACCT_TXT = "text=Create Account"
    ACCT_STREET_ADDRESS = '[data-testid="set-up-account-street-address-input"]'
    ACCT_CITY_INPUT = '[data-testid="set-up-account-city-input"]'
    ACCT_STATE_INPUT = '[data-testid="set-up-account-state-input"]'
    ACCT_LEGAL_TERMS = '[data-testid="set-up-account-legal-terms-form-field"] div'
    ACCT_SUBMIT = '[data-testid="set-up-account-submit"]'
    MANAGE_NAV_MENU = '[data-testid="manage-nav-menu"]'
    VERIFICATION_EMAIL_SENT_TEXT = "text=Verification email sent"


class CreateAcctSelectors:
    """
    Class for account creation locators
    """

    CREATE_ACCT_BTN = '[data-testid="create-account-button"]'
    SETUP_ACCT_COMP_NAME = '[data-testid="set-up-account-company-name-input"]'
    SELECT_COUNTRY = '[placeholder="Select Country"]'

    COUNTRY_OPTION = "button:text-is('{}')"
    COUNTRY_MENY_ITEM_ROLE = "option"
    ACCT_STREET_ADDRESS = '[data-testid="set-up-account-street-address-input"]'
    ACCT_CITY_INPUT = '[data-testid="set-up-account-city-input"]'
    ACCT_STATE_INPUT = '[data-testid="set-up-account-state-input"]'
    POSTAL_CODE = '[data-testid="set-up-account-zip-code-input"]'
    INPUT_PHONE = '[data-testid="set-up-account-phone-number-input"]'
    INPUT_EMAIL = '[data-testid="set-up-account-email-input"]'
    ACCT_LEGAL_TERMS = '[data-testid="set-up-account-legal-terms-form-field"] div'
    ACCT_SUBMIT = '[data-testid="set-up-account-submit"]'
    INPUT_COUNTRY_SEARCH = '[placeholder="Country"]'


class CustomerAccountSelectors:
    """
    Class for customer account locators
    """

    PAGE_HEADER = 'h1:text-is("Customer Accounts")'
    ADD_CUSTOMER_BTN = 'button:text("Add Customer")'
    SEARCH_CUSTOMER = '[data-testid="search-field"]'
    FILTER_BTN = '[data-testid="filter-btn"]'
    ACTIONS_BTN = '[data-testid="oneaction-action-btn"]'
    EXPORT_BTN = '[data-testid="export-btn"]'
    CUSTOMER_TABLE_ROWS = '[data-testid="table"] > tbody > tr'
    LOADER_SPINNER = '[data-testid$="spinner-with-text"]'
    CUSTOMER = 'span:text-is("{}")'
    CUSTOMER_ACTIONS = (
        '[data-testid="table"] > tbody > tr:has(span:text-is("{}")) > td:has(button)'
    )
    VIEW_DETAILS_BTN = '[data-testid="view-details-btn"]'
    DELETE_CUSTOMER_BTN = '[data-testid="delete-btn"]'
    EXPORT_EMAIL_INPUT = '[data-testid="email-address-form-input"]'
    GENERATE_REPORT_BTN = '[data-testid="generate-report-btn"]'
    REMOVE_TENANT_APP_MODAL = '[data-testid="remove-tenant-application-modal"]'
    CANCEL_BUTTON = '[data-testid="cancel-btn"]'
    LAUNCH_WORKSPACE_BTN = '[data-testid="launch-account-btn"]'
    CLEAR_FILTER_BTN = '[data-testid="text-clear-filters-anchor"]'
    SERVICE_FILTER_DROPDOWN = '[data-testid="application-instance-input"]'
    SERVICE_FILTER_BTN_TEMPLATE = '[role="listbox"] > button:text-is("{}")'
    SERVICE_TIME_RANGE_DROPDOWN = '[data-testid="application-instance-time-input"]'
    CUSTOM_TIME_RANGE_INPUT = '[data-testid="custom-time-range-input"]'
    APPLY_FILTER_BTN = '[data-testid="submit-btn"]'


class CustomerDetailSelectors:
    """
    Class for customer details locators
    """

    PAGE_TITLE = '[data-testid="heading-page-title"]'
    DETAILS_ACTION_BTN = '[data-testid="customer-detail-view-action-btn"]'
    LAUNCH_CUSTOMER_BTN = '[data-testid="launch-btn"]'
    DELETE_CUSTOMER_BTN = '[data-testid="delete-btn"]'
    EDIT_DETAILS_BTN = '[data-testid="edit-customer-details-btn"]'
    WORKSPACE_NAME = '[data-testid="company_name-form-input"]'
    EDIT_LOGO = "button:has-text('Select File')"
    UPLOAD_LOGO_BUTTON = '[data-testid="account-image-input"]'
    DESCRIPTION = '[data-testid="description-input"]'
    COUNTRY = '[data-testid="country-input"]'
    INPUT_COUNTRY_SEARCH = "input[placeholder='Country'][type='search']"
    STREET_ADDRESS_1 = '[data-testid="street_address-form-input"]'
    STREET_ADDRESS_2 = '[data-testid="street_address_2-form-input"]'
    CITY = '[data-testid="city-form-input"]'
    STATE_OR_REGION = '[data-testid="state_or_region-form-input"]'
    ZIP = '[data-testid="zip-form-input"]'
    EMAIL_DETAILS = '[data-testid="email-form-input"]'
    PHONE_DETAILS = '[data-testid="phone-form-input"]'
    SAVE_CHANGES_BTN = '[data-testid="save-changes-btn"]'
    CANCEL_CHANGES_BTN = '[data-testid="cancel-btn"]'
    UPDATE_MSG_POPUP = '[data-testid="notification-status-ok"]'
    UPDATE_MSG = 'span:text("updated successfully.")'
    UPDATE_MSG_CLOSE_BTN = '[data-testid="notification-status-ok"] button'


class WorkspaceDetailSelectors:
    """
    Class for Workspace details locators
    """

    PAGE_TITLE = '[data-testid="heading-company-account-page-title"]'
    EDIT_DETAILS_BTN = '[data-testid="account-details-edit-btn"]'
    EDIT_LOGO = "button:has-text('Select File')"
    UPLOAD_LOGO_BUTTON = '[data-testid="logo"]'
    WORKSPACE_NAME = '[data-testid="account-details-company-name-input"]'
    COUNTRY = '[data-testid="account-details-country-form-field"]'
    INPUT_COUNTRY_SEARCH = "input[placeholder='Country'][type='search']"
    STREET_ADDRESS_1 = '[data-testid="account-details-street-address-input"]'
    STREET_ADDRESS_2 = '[data-testid="account-details-street-address-2-input"]'
    CITY = '[data-testid="account-details-city-input"]'
    STATE_OR_REGION = '[data-testid="account-details-state-input"]'
    ZIP = '[data-testid="account-details-zip-input"]'
    PHONE_DETAILS = '[data-testid="account-details-phone-input"]'
    EMAIL_DETAILS = '[data-testid="account-details-email-input"]'
    SAVE_CHANGES_BTN = '[data-testid="save-changes-action-btn"]'
    CANCEL_CHANGES_BTN = '[data-testid="cancel-btn"]'
    UPDATE_MSG_POPUP = '[data-testid="notification-status-ok"]'
    UPDATE_MSG = 'span:text("updated successfully.")'
    UPDATE_MSG_CLOSE_BTN = '[data-testid="notification-status-ok"] button'
    SECURITY_BTN = "[data-testid='menu-item-manage-mfa']"
    BACK_TO_MANAGE_BUTTON = '[data-testid="back-btn"]'


class AddCustomerSelectors:
    """
    Class for customer account creation locators
    """

    MODAL_DIALOG = '[data-testid="add-customer-modal-dialog"]'
    COMPANY_NAME = '[data-testid="company-name-form-input"]'
    COMPANY_DESCRIPTION = '[data-testid="description-input"]'
    COUNTRY_INPUT = '[data-testid="country-input"]'
    SEARCH_COUNTRY = "input[type='search']"
    COUNTRY_OPTION = "button:text-is('{}')"
    COUNTRY_ITEM_ROLE = "option"
    STREET_ADDRESS = '[data-testid="street-address-form-input"]'
    STREET_ADDRESS2 = '[data-testid="street-address-2-form-input"]'
    CITY_INPUT = '[data-testid="city-form-input"]'
    REGION_INPUT = '[data-testid="state-or-region-form-input"]'
    POSTAL_CODE = '[data-testid="zip-form-input"]'
    CANCEL_BTN = '[data-testid="cancel-btn"]'
    CREATE_BTN = '[data-testid="create-btn"]'
    CREATION_MSG_POPUP = '[data-testid="notification-status-ok"]'
    CREATION_MSG = 'span:text-is("Customer Added Successfully")'
    CREATION_MSG_CLOSE_BTN = '[data-testid="notification-status-ok"] button'


class DeleteCustomerSelectors:
    """
    Class for holding Delete customer locators
    """

    TERMS_CHECKBOX = '[data-testid="customer-account-term-checkbox"] + div'
    KEEP_ACCOUNT_BTN = '[data-testid="cancel-btn"]'
    DELETE_ACCOUNT_BTN = '[data-testid="delete-account-btn"]'
    ERROR_NOTIFICATION = '[data-testid="notification_error"]'


class AccountTypeSelectors:
    """
    Class for Account Type locators
    """

    ELIGIBILITY_HEADER = "h3:text-is('Check Your Eligibility')"
    CHECK_ELIGIBILITY_BUTTON = "[data-testid='check-eligibility-button']"
    CONVERT_ACCT_BUTTON = "[data-testid='convert-account-button']"
    CONFIRM_CONVERT_BUTTON = "[data-testid='submit-btn']"
    FORBIDDEN_CONVERSION_MESSAGE = "[data-testid='notification-message']"
    REMOVE_WORKSPACES_HEADER = "h3:text-is('Remove All Customer workspaces')"
    REVIEW_CUSTOMER_WORKSPACES_BUTTON = "[data-testid='remove-customer-account-button']"
    CONVERT_ACC_BTN = "[data-testid='convert-account-button']"
    SUBMIT_BTN = "[data-testid='submit-btn']"
    MANAGE_WORKSPACE_TITLE = "[data-testid='heading-page-title']"
    STEP_REMOVE_UNSUPPORTED_SERVICE_BUTTON = (
        "[data-testid='review-unsupported-apps-button']"
    )
    REVIEW_CUST_WORKSPACES = "[data-testid='remove-customer-account-button']"
    SDS_WS_TITLE = "[data-testid='heading-company-name']"
    BACK_TO_MANAGE_BUTTON = '[data-testid="manage-account-btn"]'


class CheckEligibilitySelectors:
    """
    Class for Check Eligibility Selectors
    """

    NM_SERVICE_OPTION = "span:text-is('{}')"
    DEVICE_DROP_DOWN = "data-testid=input-select-nw-as-a-svs"
    DEVICE_OPTION_ROLE = "option"
    SELECT_COUNTRY_DROP_DOWN = "input[placeholder='Select Country']"
    COUNTRY_OPTION_ROLE = "option"
    CUSTOMER_LOCATION_DROP_DOWN = "data-testid=input-select-customer-located"
    CUSTOMER_LOCATION_OPTION_ROLE = "option"
    NETWORK_COUNT_INPUT = "data-testid=input-text-num-of-nw"
    MAIL_ID = "#input-text-email"
    SALES_REP_MAIL_ID = "#input-text-sales-rep-email"
    SUBMIT_BUTTON = "data-testid=button-next"
    EXIT_BTN = "[data-testid='button-finish']"
    CANCEL_BTN = "[data-testid='button-header-cancel']"
    PROVIDE_WORKSPACE_DETAILS_BTN = "[data-testid='button-header-previous']"
    NO_CONTINUE_BTN = "[data-testid='button-cancel-continue']"
    YES_EXIT_BTN = "[data-testid='button-cancel-exit']"
    CONTACT_SUPPORT_BTN = "[data-testid='contact-support-btn']"
    HEADING_STEP_TITLE = '[data-testid="heading-step-title"]'


class UserProfileSelectors:
    """
    Class for holding the user profile locators
    """

    LOADER_SPINNER = ".profile-page-spinner-wrapper"
    PERSONAL_EDIT_INFO_BTN = 'h4:text-is("Personal Information") + button:text-is("Edit")'
    PASSWORD_EDIT_BTN = 'h4:text-is("Password") + button:text-is("Edit")'
    INPUT_EMAIL = 'input[id="email"]'
    FIRST_NAME = 'input[id="firstName"]'
    LAST_NAME = 'input[id="lastName"]'
    ORGANISATION_NAME = 'input[id="hpeCompanyName"]'
    STREET_ADDRESS = 'input[id="streetAddress"]'
    STREET_ADDRESS2 = 'input[id="hpeStreetAddress2"]'
    INPUT_CITY = 'input[id="city"]'
    STATE_PROVINCE = 'input[id="state"]'
    POSTAL_CODE = 'input[id="zipCode"]'
    COUNTRY_BTN = 'input[id="hpeCountryCode__input"]'
    COUNTRY_ELEMENT_ROLE = "option"
    TIME_ZONE = 'input[id="hpeTimezone__input"]'
    TIME_ELEMENT_ROLE = "option"
    SELECT_LANG = "#preferredLanguage__input"
    SELECT_LANG_ROLE = "option"
    PRIMARY_PHONE = 'input[id="primaryPhone"]'
    MOBILE_PHONE = 'input[id="mobilePhone"]'
    EMBARGO_COUNTRY_WARNING_TEXT = 'span:text("This country code is not allowed.")'
    EMBARGO_COUNTRY_NAME = "//button[normalize-space()='North Korea']"
    SAVE_INFO_BTN = 'button:text-is("Save")'
    CURRENT_PASSWORD = 'input[id="currentPassword"]'
    NEW_PASSWORD = 'input[id="newPassword"]'
    CONFIRM_NEW_PASSWORD = 'input[id="confirmPassword"]'
    CHANGE_PASSWORD_BTN = 'button:text-is("Change Password")'
    INFO_SUCCESS_TXT = 'span:text("Your profile has been updated successfully.")'
    PASSWD_ERR_MSG_TXT = (
        'span:text("The password does not meet the password requirements.")'
    )
    CANCEL_BTN = 'button:text-is("Cancel")'
    MFA_TOGGLE_BTN = "label[for='mfa-status']"
    OKTA_VERIFY_SETUP_BTN = "span:text-is('Okta Verify')~a:has-text('Set Up')"
    OKTA_REMOVE_BTN = "span:text-is('Okta Verify')~a:has-text('Remove')"
    GOOGLE_AUTH_VERIFY_SETUP_BTN = (
        "span:text-is('Google Authenticator')~a:has-text('Set Up')"
    )
    GOOGLE_AUTH_REMOVE_BTN = "span:text-is('Google Authenticator')~a:has-text('Remove')"


class UserPreferencesSelectors:
    ACCT_SELECTION_BTN = "data-testid=account-selection-btn"
    LANGUAGE_DROPDOWN = "input[name=language]"
    LANGUAGE_DROP_ROLE = "option"
    SESSION_TIMEOUT = "data-testid=timeout-number-form-field-input"
    SAVE_CHANGES_BTN = "data-testid=profile-button-submit"
    SUCCESS_MSG_TXT = "data-testid=success-info-box"
    ERROR_MSG_TXT = "span:text-is('Bad Request')"
    INVALID_TXT_MSG = "span:has-text('Invalid session timeout value')"
    DISCARD_BTN = "data-testid=profile-button-discard"
    SIGN_IN_INFO = ".okta-form-title.o-form-head"


class SwitchAccountSelectors:
    CREATE_NEW_ACCOUNT_BTN = "data-testid=create-new-account-button"
    SEARCH_ACCOUNT_FIELD = "data-testid=search-field"
    ACCOUNT_TYPE_DROPDOWN = "data-testid=account-type-input"
    SORT_BY_DROPDOWN = "data-testid=sort-by-input"
    DROPDOWN_OPTS_TEMPLATE = "button:text-is('{}')"
    RECENT_ACCOUNTS_COUNTER = "[data-testid='text-total-accounts']"
    RECENT_ACCOUNT_CARDS = "[data-testid^='card']:has(button)"
    RECENT_ACCOUNT_NAME = (
        "[data-testid^='card']:first-of-type h2[data-testid^='heading-account-title']"
    )
    RECENT_ACCOUNT_LAUNCH = "[data-testid^='card']:first-of-type button"
    LIST_OF_ACCOUNTS_TITLES = "[data-testid='switch-account-subheader'] ~ div > div > \
              [data-testid^='card-'] [data-testid^='account-title']"
    LIST_OF_ACCOUNTS_CARDS = "[data-testid='switch-account-subheader'] \
                                ~ div > div > [data-testid^='card-']"
    PAGINATION_BAR = "data-testid=pagination-switch-account"
    GO_TO_NEXT_PAGE = "button[aria-label='Go to next page']"
    GO_TO_PREVIOUS_PAGE = "button[aria-label='Go to previous page']"
    LIST_OF_MSP_ACCOUNTS_CARDS = "[data-testid='switch-account-subheader'] ~ \
                        div > div > [data-testid^='card-'] \
                       [data-testid^='account-avatar'] ~ div span:text-is('MSP')"


class ManageMFASelectors:
    """
    Class for Manage MFA Page locators
    """

    EDIT_DETAILS_BTN = "[data-testid='MFA-edit-details-btn']"
    MFA_GOOGLE_AUTH_TOGGLE_BTN = "[data-testid='mfa-toggle-btn1']+span"
    SAVE_CHANGES_BTN = "[data-testid='MFA-save-changes-btn']"
    MFA_STATUS = "[data-testid='text-MFA-status']"
    MFA_STATUS_TEXT_TEMPLATE = "[data-testid='text-MFA-status']:text('{}')"
    MFA_NOTIFICATION_TEMPLATE = "[data-testid='notification-status-ok']:has-text('{}')"
    CANCEL_BTN = "[data-testid='MFA-cancel-btn']"
    MFA_NOTIFICATION_CLOSE_BTN = "[data-testid='notification-status-ok'] button"


class ApiPageSelectors:
    PAGE_TITLE = "[data-testid='api-page-header'] h1"
    CLIENT_BTN_TEMPLATE = "button:has(>[data-testid$='-accordion-panel'] [data-testid='heading-accordion-title']:text-is('{}'))"
    CREATE_CREDENTIAL_BTN = "[data-testid='create-credentials-btn']"
    SERVICE_MANAGER_DROPDOWN = "[id='create-credential-select-app__input']"
    CREDENTIAL_NAME = "[data-testid='credential-name-input']"
    CREATE_CREDENTIAL_FORM_BTN = "[data-testid='create-credential-form-btn']"
    CLIENT_ID = "[data-testid='client-id-copy-field-text-field-input']"
    CLIENT_SECRET = "[data-testid='client-secret-copy-field-text-field-input']"
    CLOSE_MODAL_BTN = "[data-testid$='-close-modal-btn']"
    API_CLIENT_ACTION_BTN = "[data-testid='api-client-action-btn']"
    DELETE_CLIENT_BTN = "button:has-text('Delete Credentials')"
    DELETE_CLIENT_CREDENTIAL_BTN = "[data-testid='delete-credential-btn']"
    GENERATE_ACCESS_TOKEN_BTN = "[data-testid='generate-access-token-btn']"
    CLIENT_SECRET_INPUT = "[data-testid='client-secret-input']"
    CREATE_ACCESS_TOKEN_BTN = "[data-testid='create-access-token-form-btn']"
    ACCESS_TOKEN = "[data-testid='access-token-text-field-input']"


class IpAccessRulesSelectors:
    PAGE_TITLE = "[data-testid='heading-page-title']"


class UsageReportingSelectors:
    PAGE_TITLE = "[data-testid='heading-page-title']"


class OrderHistorySelectors:
    PAGE_TITLE = '[data-testid="order-history-page-header"]'
