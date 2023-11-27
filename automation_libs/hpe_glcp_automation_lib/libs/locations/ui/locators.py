class CreateLocationPageSelectors:
    SERVICE_PAGE_HEADING = '[data-testid="text-wizard-header"]'
    CANCEL_SETUP_BTN = '[data-testid="button-header-cancel"]'
    CONFIRM_CANCEL_BTN = '[data-testid="button-cancel-exit"]'
    LOCATION_NAME_INPUT = '[data-testid="location-name-input"]'
    LOCATION_DESC_INPUT = '[data-testid="location-name-description-input"]'
    NEXT_BUTTON = '[data-testid="button-next"]'
    OPEN_ADD_ADDRESS_BTN = '[data-testid="open-add-address-modal"]'
    COUNTRY_DROPDOWN = '[data-testid="country-dropdown-street"]'
    STREET_ADDRESS_INPUT = '[data-testid="street-address-street-input"]'
    STREET_ADDRESS_2_INPUT = '[data-testid="street-address-2-street-input"]'
    CITY_ADDRESS_INPUT = '[data-testid="city-street-input"]'
    STATE_ADDRESS_INPUT = '[data-testid="state-street-input"]'
    POSTCODE_INPUT = '[data-testid="postal-code-street-input"]'
    APPLY_ADD_ADDRESS_BTN = '[data-testid="add-address-button"]'
    CONTACT_TYPE_DROPDOWN = '[data-testid="contact-type-dropdown"]'
    CONTACT_USER_DROPDOWN = '[data-testid="contact-name-dropdown"]'
    ASSIGN_CONTACT_BTN = '[data-testid="assign-contact-btn"]'
    CREATE_LOCATION_BTN = '[data-testid="create-location-btn"]'
    CONTACT_PHONE_INPUT = '[data-testid="contact-phone-input"]'


class LocationsPageSelectors:
    SEARCH_FIELD = "[data-testid=location-search-filter]"
    CREATE_LOCATION_BTN = "[data-testid=create-location-btn]"
    LOCATION_LIST_ITEM_UUID = 'li:has([data-testid=location-name]:text-is("{}")) > div'
    LOCATION_LIST_ITEM_DROP_BTN = (
        'li:has([data-testid=location-name]:text-is("{}")) '
        "[data-testid=multipleactions-action-btn]"
    )
    LOCATION_OPTION_VIEW_BTN = "[data-testid=action-0]"
    LOCATION_OPTION_DELETE_BTN = "[data-testid=action-1]"
    POPUP_CONFIRM_BTN = "[data-testid=okay-btn]"
    POPUP_CONFIRM_TITLE = "[data-testid=confirmation-header-title]"
    PAGE_TITLE = 'div[data-testid="location-page-title"] h1'


class LocationDetailsPageSelectors:
    LOCATION_DETAILS_HEADER = "[data-testid=location-details-header] h1"
    BACK_TO_LOCATIONS_BTN = "[data-testid=location-details-page-back-button]"
