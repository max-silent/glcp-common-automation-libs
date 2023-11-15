class ServicePageLocators:
    ALL_REGION = 'input[value="All Regions"]'
    CHOOSE_REGION_TEMPLATE = "button:text-is('{}')"
    LAUNCH_BTN = "span:has(>button:text-is('Launch'))"
    MY_SERVICES_TAB = '[data-testid="desc-service-centric-menulist-my-services-link"]'
    SERVICE_CATALOG = '[data-testid="desc-service-centric-menulist-service-catalog-link"]'
    SUBSCRIPTION_TAB = (
        '[data-testid="service-centric-menulist-service-subscriptions-link"]'
    )
    ADD_SERVICE_SUBSCRIPTIONS_HEADING = "[data-testid='heading-undefined-title']"


class ServiceDetailsSelectors:
    HEADING_PAGE_TITLE = "[data-testid='heading-undefined-title']"
    ACTIVE_TAB = "//button[@role='tab' and @aria-selected='true']//span"
    TAB_TEMPLATE = "button[role='tab'] span:has-text('{}')"
    ADD_REGION = "//button[normalize-space()='Add Region']"
    SELECT_REGION = "[data-testid='service-centric-provision-dropdown']"
    REGION_VALUE = "//span[text()='Regions (0)']"
    TERMS_CONDITION_CHECKBOX = "[data-testid='app-term-form']"
    INSTALLED_SERVICE_REGION_TEMPLATE = "[data-testid='installed-app-{}']"
    PROVISION_BTN = 'button:has-text("Provision")'
    ELLIPSIS_ICON = 'div[data-testid="installed-app-list-action-btn"]'
    LOADER_SPINNER = '[data-testid="loader-spinner"]'
    LAUNCH_BUTTON = "//button[text()='Launch']"
    VIEW_ASSIGNED_DEVICES_BUTTON = "//button[text()='View Assigned Devices']"
    REMOVE_BUTTON = "//button[text()='Remove Region']"
    REMOVE_REGION = "[data-testid='remove-region-btn']"
    KEEP_REGION = "[data-testid='cancel-btn']"
    CANCEL_BTN = "//button[text()='Cancel']"
    DEPLOY_BTN = "//button[text()='Deploy']"
