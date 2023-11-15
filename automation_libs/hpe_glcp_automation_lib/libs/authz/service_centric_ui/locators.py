class UsersSelectors:
    """User Page Locators"""

    BACK_BUTTON = '[data-testid="identity-back-btn"]'
    HEADING_PAGE_TITLE = '[data-testid="heading-page-title"]'
    INVITE_USERS_BUTTON = '[data-testid="invite-users-btn"]'
    CARD_TOTAL_USERS = '[data-testid="card-total-users-tab"]'
    CARD_ACTIVE_USERS = '[data-testid="card-active-users-tab"]'
    CARD_INACTIVE_USERS = '[data-testid="card-inactive-users-tab"]'
    CARD_UNVERIFIED_USERS = '[data-testid="card-unverified-users-tab"]'
    SEARCH_FIELD = '[data-testid="search-field"]'
    TABLE_HEAD_COLUMNS = '[data-testid="table"]>thead>tr>th'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    TABLE_ROW_TEMPLATE = '[data-testid="table"]>tbody>tr:nth-child({})'
    INVITE_USERS_EMAIL_FIELD = '[data-testid="email-form-field-input"]'
    INVITE_USERS_ROLES_DROPDOWN = '[data-testid="roles-dropdown"]'
    INVITE_USERS_ROLE_TEMPLATE = "button:has(span:text-is('{}'))"
    INVITE_USERS_SEND_INVITE_BTN = '[data-testid="send-invite-btn"]'
    USER_STATUS_TEMPLATE = "//span[normalize-space()='{}']/ancestor::tr[contains(.,'{}')]"
    TABLE_ACTION_BTN_TEMPLATE = "[data-testid=\"table\"] > tbody > tr:has(span:text-is('{}')) > td:last-child:has(button)"
    DELETE_BTN = 'button:text-is("Delete")'
    DELETE_CHECK_BTN = '[data-testid="delete-user-btn"]'
    DELETE_CONFIRM_BTN = '[data-testid="confirm-delete-user-btn"]'
    ASSIGN_ROLE_BUTTON = "[data-testid=assign-role-btn]"
    APPLICATIONS_SELECT_DROPDOWN = "button[id='applications-dropdown']"
    ROLES_DROPDOWN = "button[id='roles-dropdown']"
    ACCESS_RULE_DROPDOWN = "button[id='access-rules-dropdown']"
    CHANGE_ROLE_BUTTON = "[data-testid='confirm-assignment-role-btn']"
    RESOURCE_POLICY_TOGGLE = "[data-testid='toggle-btn-box']"
    RESOURCE_POLICY_DROPDOWN = "button[id='rrp-dropdown']"
    ROLES_DROPDOWN_OPT_TEMPLATE = "data-testid=option-{}"
    SEARCH_POLICY_INPUT = "input[placeholder='Search Resource Restriction Policies']"
    RESOURCE_POLICY_OPT_TEMPLATE = "data-testid=option-{}"
    CLEAR_ALL_POLICY_BTN = 'button:has-text("Clear All")'
    REMOVE_ROLE_OPT = "data-testid=action-1"
    REMOVE_ROLE_BTN = "data-testid=save-btn"
    NOTIFICATION_OK_CLOSE_BTN = '[data-testid="notification-status-ok"] button'


class UserDetailSelectors:
    """User Detail Locators"""

    LOADER_SPINNER = '[data-testid*="loader-spinner"]'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    ASSIGN_ROLE_BTN = '[data-testid="assign-role-btn"]'
    USER_APPLICATION_DROPDOWN = '[data-testid="applications-dropdown"]'
    INVITE_USERS_ROLES_DROPDOWN = '[data-testid="roles-dropdown"]'  # form
    USER_ROLE_OPTION_TEMPLATE = "[data-testid='option-{}']"
    APPLICATION_DROP_DOWN = "[id='applications-dropdown__select-drop']"
    CHANGE_ROLE_BUTTON = "[data-testid='confirm-assignment-role-btn']"
