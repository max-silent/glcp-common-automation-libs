class DevSubscriptionsSelectors:
    """Selectors, used in "DeviceSubscriptions" class.
    Related URL: ".../devices/subscriptions".
    """

    ADD_SUBS_BUTTON = "[data-testid='add-device-subscription-btn']"
    SUBS_KEY_FIELD = "input#subscription_key"
    SUBMIT_SUBS_BTN = "[data-testid='submit-licenses-btn']"
    SEARCH_FIELD = '[data-testid="search-field"]'
    DEV_TYPES_DROPDOWN = "[data-testid='license-device-type-dropdown']"
    DEV_TYPES_ITEM_TEMPLATE = "[role='listbox']>button:text-is('{}')"
    FILTER_BUTTON = "[data-testid='filter-search-btn']"
    TABLE_ROWS = "[data-testid='table']>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid='table']>tbody>tr:nth-child({})"
    ACTION_BTN = 'button[aria-label="Open Drop"]'
    EXPORT_BTN = 'button:text-is("Export")'
    EXPORT_DIALOG_HEADER = 'h1[data-testid="heading-header-title"]'
    EXPORT_DIALOG_CANCEL = 'button[data-testid="cancel-btn"]'
    APPLY_FILTER_BTN = '[data-testid="apply-filters-btn"]'
    CANCEL_FILTER_BTN = '[data-testid="cancel-filter-btn"]'
    CLEAR_FILTER_BTN = '[data-testid="clear-filters-anchor"]'
    SUBSCRIPTION_KEY_TEMPLATE = 'span[data-testid="text-subscription-key"]:text-is("{}")'
    FILTER_ITEM_TEMPLATE = 'div:has(>label:text-is("{field_label}")) label:has(>span:text-is("{item_label}"))'
    DEV_SUBSCRIPTIONS_HEADER = '[data-testid="device-subscriptions-page-header"] h2:text-is("Device Subscriptions")'
    PAGE_SUBTITLE_TXT = "[data-testid=text-device-subscription-page-subtitle]:has-text('Manage and add device subscription keys. Service subscriptions can be found here')"
    SERVICE_SUBSCRIPTIONS_LNK = "[data-testid='text-device-subscription-page-subtitle']>a"


class ServiceSubscriptionsSelectors:
    """Selectors, used in "ServiceSubscriptions" class.
    Related URL: ".../services/service-subscriptions".
    """

    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    ADD_SUBSCR_BTN = '[data-testid="add-service-subscription-btn"]'
    SUBSCR_KEY_ENTRY_TEMPLATE = 'span:has-text("{}")'
    SUBSCR_KEY_INPUT_FIELD = '[data-testid="license-key-input-field"]'
    SUBMIT_BTN = '[data-testid="submit-licenses-btn"]'
    SERVICE_SUB_BTN = "[data-testid='service-subscriptions-link']"
    ERROR_MSG = "[data-testid='form-global-error']"
    SERVICE_SUBSCRIPTIONS_HEADING = (
        "[data-testid='heading-undefined-title']:text-is('Services')"
    )
    SERVICE_SUBSCRIPTIONS_TITLE = '[data-testid="service-subscriptions-page-header"]'
    SERVICE_CANCEL_BTN = '[data-testid="cancel-btn"]'
    SUBSCR_KEY_FIELD_TEMPLATE = 'span[data-testid="text-subscription-key"]:text-is("{}")'
    GO_TO_APP_BTN = 'button[data-testid="view-app-btn"]'
    TABLE_COLUMN_TEMPLATE = 'thead th span:text-is("{}")'
    FOUND_HERE_LINK = 'a[href="/devices/subscriptions"]'
    SERVICE_DIALOG_HEADER = "[data-testid='heading-undefined-title']"
    SERVICE_DETAIL_DIALOG = (
        '[data-testid="heading-service-subscription-side-panel-title"]'
    )


class ApplySubscriptionSelectors:
    """Selectors, used in "ApplySubscription" class.
    Related URL: ".../devices/inventory/apply-subscription".
    """

    APPLY_SUBSCRIPTION_BTN_TEMPLATE = (
        "div:has(span:text-is('{}')) [data-testid=\"apply-subscriptions-btn\"]"
    )
    APPLY_SUBSCRIPTION_CANCEL_BTN = '[data-testid="apply-subscription-cancel-btn"]'
    APPLY_SUBSCRIPTION_BTN = '[data-testid="apply-subscription-btn"]'
    LICENSE_TIER_DROPDOWN = '[data-testid="license-tier-dropdown"]'
    SUBSCRIPTION_KEYS = "tbody>tr>th span"
    SUBSCRIPTION_KEY_TEMPLATE = "tbody>tr:nth-child({}) th span"
    SUBSCRIPTION_CHECKBOX_TEMPLATE = (
        "tbody>tr:nth-child({}) label:has(input[type='checkbox'])"
    )
    SUBSCRIPTION_CHECKBOX_ID_TEMPLATE = (
        "tbody>tr:has(span:text-is('{}')) label:has(input[type='checkbox'])"
    )
    FINISH_BUTTON = '[data-testid="button-finish"]'
    CLOSE_BUTTON = '[data-testid="close-btn"]'
