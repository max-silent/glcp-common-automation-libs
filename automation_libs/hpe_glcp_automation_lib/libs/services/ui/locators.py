class MyServicesSelectors:
    """Selectors, used in "MyServices" class.
    Related URL: ".../services/my-services".
    """

    LOADER_SPINNER = '[data-testid="loader-spinner"]'
    HEADING_PAGE_TITLE = "h2[class^='StyledHeading-']"
    REGIONS_DROPDOWN = "[data-testid='service-centric-my-services-dropdown']"
    GRID_VIEW_BTN = "button[aria-label='Switch to grid view']"
    LIST_VIEW_BTN = "button[aria-label='Switch to list view']"
    LAUNCH_BTN_TEMPLATE = "button[aria-label^='Launch {}']:text-is('Launch')"
    SERVICE_TILE = "div[title]:has(div[data-testid='service-category'])"
    REGION_TITLE = 'h3:has-text("{}")'


class ServiceCatalogSelectors:
    """Selectors, used in "ServiceCatalog" class.
    Related URL: ".../services/service-catalog".
    """

    SERVICES_PAGE_HEADING = "[data-testid='heading-service-centric-catalog-pageheader-title']:text-is('Services')"
    HEADING_PAGE_TITLE = "h2[class^='StyledHeading-']"
    LOADER_SPINNER = '[data-testid="loader-spinner"]'
    SERVICES_OPEN_LINK_TEMPLATE = (
        "button[data-testid='service-catalog-card']:has(h4:text-is('{}'))"
    )
    SELECT_REGION_DROPDOWN = "[data-testid='service-centric-catalog-region-dropdown']"
    SERVICES_CARDS = '[data-testid="service-catalog-card"]'


class ServiceDetailsSelectors:
    """Selectors, used in "ServiceDetails" class.
    Related URL: ".../services/service-catalog/{service_name}".
    """

    HEADING_PAGE_TITLE = "[data-testid='heading-undefined-title']"
    TAB_TEMPLATE = "button[role='tab']:has(span:has-text('{}'))"
    OVERVIEW_AREA = "[aria-label='Overview Tab Contents']"
    REGION_DROPDOWN = "[data-testid='service-centric-provision-dropdown']"
    REGION_DROPDOWN_ITEM = "button[tabindex='0']"
    TERMS_CONDITION_CHECKBOX = "[data-testid='app-term-form']"
    UNAVAILABLE_REGIONS_ERROR = "[data-testid='text-unavailable-regions-error-msg']"
    INSTALLED_APP_REGION_ITEMS = (
        "[data-testid^='installed-app-']:has([data-testid='app-name'])"
    )
    INSTALLED_APP_REGION_TEMPLATE = (
        "[data-testid^='installed-app-{}']:has([data-testid='app-name'])"
    )
    INSTALLED_APP_REGION_NAME_TEMPLATE = (
        "[data-testid^='installed-app-{}'] [data-testid='app-region']:has-text('{}')"
    )
    INSTALLED_APP_ACTION_BTN_TEMPLATE = (
        "[data-testid^='installed-app-{}'] [data-testid='installed-app-list-action-btn']"
    )
    APP_ACTION_TEMPLATE = "button[data-testid^='action']:text-is('{}')"
    ADD_REGION_BTN = "button:text-is('Add Region')"
    PROVISION_BTN = "button:text-is('Provision')"
    LAUNCH_BTN = "button:text-is('Launch')"
    LOADER_SPINNER = '[data-testid="loader-spinner"]'
    REMOVE_REGION = "[data-testid='remove-region-btn']"
    KEEP_REGION = "[data-testid='cancel-btn']"
    DEPLOY_BTN = "button:text-is('Deploy')"
    AVAILABLE_REGION_TEMPLATE = (
        'dt:has-text("Available Regions") + dd > span:text-is("{}")'
    )
    DOCUMENTATION_LINK = 'dt:has-text("Documentation") + dd > a'
    TERMS_OF_SERVICE_LINK = 'dt:has-text("Terms of Service") + dd > a'
    BACK_TO_SERVICE_CATALOG = 'a[href="/services/service-catalog"]'


class LaunchedServiceSelectors:
    """Selectors, used in "LaunchedApplications" class.
    Note: different launched applications have different related URLs and page elements.
    """

    TEXT_ELEMENT_TEMPLATE = ":has-text('{}')"
    TEXT_BUTTON_TEMPLATE = "button:has-text('{}')"
