class NavBarSelectors:
    # Workspace menu elements
    WORKSPACE_MENU_BTN = "menu-button[part=workspace-menu-button]"
    WORKSPACE_MENU_TEXT = 'span[class="workspace-name"]'
    WORKSPACE_MENU_POPUP = "menu-button[part=workspace-menu-button] fast-menu.shown"
    MENU_ITEM_MANAGE_ACC = "[part='workspace-menu-button'] fast-menu-item[part=ws-workspace-menu-manage-workspace]"
    MENU_ITEM_MANAGE_USERS = "[part='workspace-menu-button'] fast-menu-item[part=ws-workspace-menu-manage-users]"
    MENU_ITEM_ROLES_PERMISSIONS = "[part='workspace-menu-button'] fast-menu-item[part=ws-workspace-menu-roles-permissions]"
    MENU_ITEM_SWITCH_WORKSPACE = "[part='workspace-menu-button'] fast-menu-item[part=ws-workspace-menu-switch-workspace]"
    # Help menu elements
    HELP_MENU_BUTTON = "[part='help-menu-button']"
    HELP_MENU_POPUP = "[part='help-menu-button'] fast-menu.shown"
    DOCUMENTATION_MENU_ITEM = (
        "[part='help-help-hpe-greenlake-help-help-nav-help-dropdown-documentation']"
    )
    BILLING_MENU_ITEM = "[part='help-help-hpe-greenlake-support-help-nav-help-dropdown-billing-metering-subscription']"
    WORKSPACE_MENU_ITEM = (
        "[part='help-help-hpe-greenlake-support-help-nav-help-dropdown-acc-user-onboard']"
    )
    VIEW_CASES_MENU_ITEM = (
        "[part='help-help-hpe-greenlake-support-help-nav-help-dropdown-view-cases']"
    )
    # Contextual help menu elements
    CONTEXTUAL_HELP_BTN = 'fast-button[id="context-help"]'
    # User menu elements
    USER_MENU_BTN = "menu-button[part=user-menu-button]"
    USER_MENU_POPUP = "menu-button[part=user-menu-button] fast-menu.shown"
    MENU_ITEM_EMAIL_ADDRESS = "span[class='user-email']"
    SIGNOUT_MENU_ITEM = "[part=user-user-profile-dropdown-sign-out]"
    PREFERENCES_MENU_ITEM = "[part=user-user-profile-dropdown-hpe-greenlake-preferences]"
    ACCOUNT_DETAILS_MENU_ITEM = "[part=user-user-profile-dropdown-hpe-account-details]"
    # Navigation elements
    MENU_BTN_HOME = 'fast-button>formatted-message:has-text("Home")'
    MENU_BTN_SERVICES = 'fast-button>formatted-message:has-text("Services")'
    MENU_BTN_DEVICES = 'fast-button>formatted-message:has-text("Devices")'
    MENU_BTN_CUSTOMERS = 'fast-button>formatted-message:has-text("Customers")'
    APP_MENU_SERVICES_HEADER = 'formatted-message[key="header_nav.services"]'
    APP_MENU_GREENLAKE_ADMIN_HEADER = (
        'formatted-message[key="app_navigation.hpe_gl_administration"]'
    )
    APP_MENU_RESOURCES_HEADER = 'formatted-message[key="app_navigation.hpe_resources"]'
    HELP_MENU_HELP_TITLE = "fast-menu [class=section-label]:has-text('Help')"
    HELP_MENU_SUPPORT_TITLE = "fast-menu [class=section-label]:has-text('Support')"
    BRAND_LOGO = 'hpe-brand[part="hpe-brand"]'
    APPS_MENU_BTN = "[part='apps-menu-button']"
    NOTIFICATIONS_BUTTON = "[aria-label='Notifications']"
    USER_MENU_ITEM = 'fast-menu-item[part="user-user-profile-dropdown-{}"]'
    HELP_MENU_ITEM_TEMPLATE = (
        'fast-menu-item[part="help-help-hpe-greenlake-help-help-nav-help-dropdown-{}"]'
    )
    SUPPORT_MENU_ITEM_TEMPLATE = (
        'fast-menu-item[part="help-help-hpe-greenlake-support-help-nav-help-dropdown-{}"]'
    )
    HELP_MENU_SUB_BUTTONS = "fast-tab[value='{}'][slot='tab']"
    APP_MENU_SERVICES_ITEM_TEMPLATE = "fast-menu-item[part='apps-header-nav-services-{}']"
    APP_MENU_ADMINISTRATION_ITEM_TEMPLATE = "fast-menu-item[part='apps-app-navigation-hpe-gl-administration-app-navigation-{}']"

    APP_MENU_RESOURCES_ITEM_TEMPLATE = (
        "fast-menu-item[part='apps-app-navigation-hpe-resources-app-navigation-{}']"
    )


class ServicesSideMenuSelectors:
    """Selectors, used in "ServicesSideMenu" class.
    Note: it's page-element class, which included as part of different page-object classes, related to different URLs.
    """

    SIDE_MENU_TAB_TEMPLATE = (
        "[data-testid='service-centric-menulist']>button :text-is('{}')"
    )
    MY_SERVICES_TAB = '[data-testid="desc-service-centric-menulist-my-services-link"]'
    SUBSCRIPTIONS_TAB = (
        '[data-testid="service-centric-menulist-service-subscriptions-link"]'
    )
    SERVICE_CATALOG = '[data-testid="desc-service-centric-menulist-service-catalog-link"]'


class DevSideMenuSelectors:
    """Selectors, used in "SideMenuNavigablePage" class.
    Note: it's page-element class, which included as part of different page-object classes, related to different URLs.
    """

    DEVICES_TAB_BUTTON = "[data-testid='devices-link']"
    TAGS_TAB_BUTTON = "[data-testid='devices-tags']"
    SUBSCRIPTIONS_TAB_BUTTON = "[data-testid='devices-subscriptions']"
    AUTO_SUBSCRIBE_TAB_BUTTON = "[data-testid='auto-subscribe-link']"


class ActivateSideMenuSelectors:
    """Selectors, used in "SideMenuNavigablePage" class.
    Note: it's page-element class, which included as part of different page-object classes, related to different URLs.
    """

    DEVICES_TAB_BUTTON = '[data-testid="devices-tab"]'
    FOLDERS_TAB_BUTTON = '[data-testid="folders-tab"]'
    DOCUMENTATION_TAB_BUTTON = '[data-testid="desc-activate-documentation-tab"]'
