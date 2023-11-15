class NavBarSelectors:
    MENU_BTN_HOME = 'fast-button>formatted-message:has-text("Home")'
    MENU_BTN_SERVICES = 'fast-button>formatted-message:has-text("Services")'
    MENU_BTN_DEVICES = 'fast-button>formatted-message:has-text("Devices")'
    MENU_BTN_CUSTOMERS = 'fast-button>formatted-message:has-text("Customers")'


class BasePageSelectors:
    APP_LOADER = '[data-testid="app-loader"]'
    LOADER_SPINNER = '[data-testid$="spinner-with-text"]'


class HomePageSelectors:
    LOADER_SPINNER = '[data-testid="loader-spinner"]'
    ACCT_NAME = '[data-testid="heading-heading-home"]'
    INVITE_USER_BUTTON = '[data-testid="invite-user-card-btn"]'
    ASSIGN_ROLES_BUTTON = '[data-testid="assign-user-access-card-btn"]'
    RELEASE_NOTES_BUTTON = '[data-testid="release-notes-card-btn"]'
    SWITCH_ACCOUNT_BUTTON = '[data-testid="switch-account-btn"]'
    RETURN_TO_MSP_ACCT_BTN = '[data-testid="return-to-msp-account-btn"]'
    GREEN_LAKE_BADGE_TITLE = "div.container"
    # TODO: Replace xpaths below by css.
    REGION_FEATURED_SERVICES = "(//span[text()='Available Regions']/following::span)[1]"
    RECENT_SERVICE_EMPTY_TEXT = "//div[@class='StyledBox-sc-13pk1d4-0 jZaOYR']/span"
    RECENT_SERVICES_TITLE = '//h2[text()="Recent Services"]'
    MANAGEMENT_AND_GOVERNANCE = '[data-testid="text-MANAGEMENT_AND_GOVERNANCE-tab"]'
    RECOMMENDED_TAB = '[data-testid="text-RECOMMENDED-tab"]'
    COMPUTE_TAB = '[data-testid="text-COMPUTE-tab"]'
    NETWORKING_TAB = '[data-testid="text-NETWORKING-tab"]'
    WORKLOADS_TAB = '[data-testid="text-WORKLOADS-tab"]'
    PRIVATE_CLOUD_BUSINESS_EDITION_ARROW = (
        "(//div[@data-testid='card-service-centric-featured-services-card']//button)[2]"
    )
    SERVICE_TITLE = '[title="{}"] button'
    ADD_USER_OR_ASSIGN_ROLES_LINK_PATH = '[data-testid="manage-iam-anchor"]'
    CREATE_LOCATION_LINK = '[data-testid="çreate-location-anchor"]'
    ADD_DEVICE_LINK = '[data-testid="onboard-devices-anchor"]'
    ADD_SERVICE_SUBSCRIPTIONS_LINK = '[data-testid="add-subscriptions-anchor"]'
    PRIVATE_CLOUD_TAB = '[data-testid="text-PRIVATE_CLOUD-tab"]'


class ManageAccountSelectors:
    CARD_WORKSPACE_DETAILS = '[data-testid="card-account_details"]'
    CARD_AUDIT_LOGS = '[data-testid="card-audit-logs"]'
    CARD_IDENTITY_AND_ACCESS = '[data-testid="card-identity"]'
    CARD_SUBSCRIPTIONS = '[data-testid="card-subscriptions"]'
    CARD_ACTIVATE = '[data-testid="card-activate"]'
    CARD_AUTHENTICATION = '[data-testid="card-authentication"]'
    PCID_VALUE_SELECTOR = '[data-testid="paragraph-account-id-val"]'
    MANAGE_ACCOUNT_TYPE_BUTTON = "[data-testid='manage-account-type-btn']"
    WORKSPACE_TYPE = '[data-testid="paragraph-account-type-val"]'


class IdentitySelectors:
    CARD_USERS = '[data-testid="card-users"]'
    CARD_ROLES = '[data-testid="roles-title"]'
    ROLES_AND_PERMISSIONS_LINK_PATH = '[data-testid="text-roles-title"]'
    HEADING_POPUP_PAGE_TITLE = "[data-testid='heading-header-title']"
    CANCEL_BTN = '[data-testid="cancel-btn"]'
    ASSIGN_A_ROLE_BUTTON = "[data-testid='assignments_btn']"
