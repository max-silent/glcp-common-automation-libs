class DevSubscriptionsSelectors:
    """Selectors, used in "DeviceSubscriptions" class.
    Related URL: ".../manage-account/subscriptions/device-subscriptions".
    """

    ADD_SUBSCR_BUTTON = '[data-testid="add-device-subscription-btn"]'
    SEARCH_FIELD = '[data-testid="search-field"]'
    DEVICE_TYPES_DROPDOWN = 'button[aria-label*="All Device Types"]'
    FILTER_BUTTON = '[data-testid="filter-search-btn"]'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    TABLE_ROW_TEMPLATE = '[data-testid="table"]>tbody>tr:nth-child({})'


class ServiceSubscriptionsSelectors:
    """Selectors, used in "DeviceSubscriptions" class.
    Related URL: ".../manage-account/subscriptions/service-subscriptions".
    """

    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    ADD_SUBSCR_BTN = '[data-testid="add-service-subscription-btn"]'
    SUBSCR_KEY_ENTRY_TEMPLATE = 'span:has-text("{}")'
    SUBSCR_KEY_INPUT_FIELD = '[data-testid="license-key-input-field"]'
    SUBMIT_BTN = '[data-testid="submit-licenses-btn"]'
    SERVICE_SUB_BTN = "[data-testid='service-subscriptions-link']"
    ERROR_MSG = "[data-testid='form-global-error']"
    SERVICE_SUBSCRIPTION_TITLE = '[data-testid="service-subscription-page-title"]'


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
