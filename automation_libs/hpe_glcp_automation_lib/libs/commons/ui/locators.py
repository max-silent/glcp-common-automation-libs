class BasePageSelectors:
    APP_LOADER = '[data-testid="app-loader"]'
    LOADER_SPINNER = '[data-testid$="spinner-with-text"]'
    BANNER_NOTIFICATION = '[data-testid="banner-notification-test-id"]'
    BANNER_NOTIF_CLOSE_BTN = (
        "[data-testid='banner-notification-test-id'] button:has([aria-label='FormClose'])"
    )


class HeaderedPageSelectors:
    CONTEXTUAL_HELP_CLOSE_BTN = '[data-testid="contextual-help"] [aria-label="FormClose"]'
    VIEW_ALL_DOCUMENTATION = '[data-testid="contextual-help--viewall--"]'
    BACK_TO_LIST = '[data-testid="contextual-help--previous"]'
    CONTEXTUAL_HELP_ITEM_TEMPLATE = '[data-testid="contextual-help"] span:text-is("{}")'
    CONTEXTUAL_HELP_TITLE_TEMPLATE = (
        '[data-testid="contextual-help"] h1[id="ariaid-title1"]:has-text("{}")'
    )
    CONTEXTUAL_HELP_URL_TEMPLATE = '[data-testid="contextual-help"] a[href="{}"]'
    LIST_OF_ALL_TOPICS = '[data-testid^="contextual-help--topics-"]>span:first-child'


class HomePageSelectors:
    LOADER_SPINNER = '[data-testid="loader-spinner"]'
    RETURN_TO_MSP_ACCT_BTN = '[data-testid="return-to-msp-account-btn"]'
    EMPTY_RECENT_SERVICE_PLACEHOLDER = (
        ':below(h2:has-text("Recent Services")) p:has-text("You haven\'t launched any '
        'services yet. View the services catalog to get started.")'
    )
    RECENT_SERVICES_TITLE = 'h2:has-text("Recent Services")'
    MANAGEMENT_AND_GOVERNANCE = '[data-testid="MANAGEMENT_AND_GOVERNANCE-tab"]'
    RECOMMENDED_TAB = '[data-testid="RECOMMENDED-tab"]'
    PRIVATE_CLOUD_TAB = '[data-testid="PRIVATE_CLOUD-tab"]'
    COMPUTE_TAB = '[data-testid="COMPUTE-tab"]'
    NETWORKING_TAB = '[data-testid="NETWORKING-tab"]'
    WORKLOADS_TAB = '[data-testid="WORKLOADS-tab"]'
    FEATURED_SERVICE_TAB_TEMPLATE = (
        '[data-testid="dashboard-featured-tabs"] [data-testid="{}-tab"]'
    )
    FEATURED_SERVICE_CARD_SUBHEADER_TEMPLATE = '[data-testid="text-service-centric-featured-services-card-title"] span:text-is("{}")'
    PRIVATE_CLOUD_BUSINESS_EDITION_ARROW = (
        "(//div[@data-testid='card-service-centric-featured-services-card']//button)[2]"
    )
    LAUNCH_RECENT_SERVICE_TEMPLATE = 'button[aria-label="Launch {}"]'
    RECENT_SERVICES_LAUNCH = 'button:has-text("Launch")'
    LAUNCH_POPUP_REGION_DROPDOWN = "[data-testid=service-centric-launch-dropdown]"
    LAUNCH_POPUP_REGION_DROPDOWN_LIST_ITEM = 'button[role="option"]'
    LAUNCH_POPUP_LAUNCH_BTN = (
        '[data-testid=service-centric-launch-modal] button:has-text("Launch")'
    )
    LAUNCH_POPUP_CANCEL_BTN = (
        '[data-testid=service-centric-launch-modal] button:has-text("Cancel")'
    )
    ADD_USER_OR_ASSIGN_ROLES_LINK_PATH = '[data-testid="manage-iam-anchor"]'
    CREATE_LOCATION_LINK = '[data-testid="create-location-anchor"]'
    ADD_DEVICE_LINK = '[data-testid="onboard-devices-anchor"]'
    ADD_SERVICE_SUBSCRIPTIONS_LINK = '[data-testid="add-subscriptions-anchor"]'
    SERVICE_PLATE_TEMPLATE = (
        "[data-testid=\"card-service-centric-featured-services-card\"] h3:text-is('{}')"
    )
    QUICK_ACTIONS_CARD = '[data-testid="card-quick-actions-card"]'
    QUICK_ACTION_LINK_TEMPLATE = "[data-testid='card-quick-actions-card'] a:text-is('{}')"
    MANAGE_WORKSPACE_LINK = "[data-testid='manage-workspace']"
    SWITCH_WORKSPACE_LINK = "[data-testid='switch-workspace']"
    LIST_VIEW_BTN = "button[aria-label='Switch to list view']"
    RECENT_SERVICE_LAUNCH_BUTTON = 'button:has-text("Launch")'
    DISMISS_LINK = 'a:text-is("Dismiss")'
    LEARN_MORE_DEVELOPER_CARD = "[data-testid='card-developer-portal-card']"
    LEARN_MORE_WHATS_NEW_CARD = "[data-testid='card-whats-new-card']"
    LEARN_MORE_TEST_DRIVE_CARD = "[data-testid='card-test_drive_card']"
    GRID_VIEW_BTN = "button[aria-label='Switch to grid view']"
    MY_SERVICES_LINK = "//a[text()='My Services']"
    VIEW_CATALOG_LINK = "//a[text()='View Catalog']"
    RECENT_SERVICES_APP_DIV_TEMPLATE = "div[title='{}']"


class ManageAccountSelectors:
    CARD_WORKSPACE_DETAILS = '[data-testid="card-account_details"]'
    CARD_AUDIT_LOGS = '[data-testid="card-audit-logs"]'
    CARD_IDENTITY_AND_ACCESS = '[data-testid="card-identity"]'
    CARD_SUBSCRIPTIONS = '[data-testid="card-subscriptions"]'
    CARD_ACTIVATE = '[data-testid="card-activate"]'
    CARD_AUTHENTICATION = '[data-testid="card-authentication"]'
    CARD_LOCATION = '[data-testid="card-locations"]'
    CARD_API = '[data-testid="card-api"]'
    CARD_IP_ACCESS_RULES = '[data-testid="card-ip-access-rules"]'
    CARD_ORDER_HISTORY = '[data-testid="card-order-history"]'
    CARD_USAGE_REPORTING = '[data-testid="card-usage-reporting"]'
    PCID_VALUE_SELECTOR = '[data-testid="paragraph-account-id-val"]'
    MANAGE_ACCOUNT_TYPE_BUTTON = "[data-testid='manage-account-type-btn']"
    WORKSPACE_TYPE = '[data-testid="paragraph-account-type-val"]'
    MANAGE_WORKSPACE_TITLE = (
        '[data-testid=manage-account-pageHeader] :text("Manage Workspace")'
    )


class IdentitySelectors:
    CARD_USERS = '[data-testid="card-users"]'
    CARD_ROLES = '[data-testid="card-roles"]'
    CARD_SCOPE_GROUPS = "[data-testid=card-scope-groups]"
    ROLES_AND_PERMISSIONS_LINK_PATH = '[data-testid="text-roles-title"]'
    HEADING_POPUP_PAGE_TITLE = (
        '[data-testid="heading-header-title"]:has-text("Assign Role")'
    )
    CANCEL_BTN = '[data-testid="cancel-btn"]'
    ASSIGN_ROLE_BTN = "[data-testid='assignments_btn']"
    PAGE_TITLE = "[data-testid='heading-identity-title']"
