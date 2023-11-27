class RolesSelectors:
    BACK_BUTTON = '[data-testid="identity-title"]'
    HEADING_PAGE_TITLE = '[data-testid="heading-page-title"]'
    CREATE_ROLE_BUTTON = '[data-testid="roles-create-btn"]'
    SEARCH_FIELD = '[data-testid="search-field"]'
    TABLE_HEAD_COLUMNS = '[data-testid="table"]>thead>tr>th'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    TABLE_ROW_TEMPLATE = '[data-testid="table"]>tbody>tr:nth-child({})'
    APPLICATION_DROPDOWN = "data-testid=application-dropdown"
    ROLES_DROPDOWN = "data-testid=roles-dropdown"
    CREATE_ROLE = "data-testid=create-role-btn"
    ROLE_NAME_INPUT = "data-testid=role-name-input"
    NEXT_BUTTON = "data-testid=button-next"
    ADD_PERMISSIONS_BTN = "data-testid=add-permissions-btn"
    CREATE_PERMISSION_BTN = "data-testid=permissions-create-btn"
    FINISH_BUTTON = "data-testid=button-finish"
    ROLE_ACTION_BUTTON = "data-testid=roles-data-table-action-buttons-1"
    DUPLICATE_ACTION = "data-testid=action-1"
    ROLE_ACTION_BUTTON_TEMPLATE = (
        '[data-testid="table"] > tbody > tr:has(span:text-is("{}")) > td:has(button)'
    )
    DELETE_ACTION = "data-testid=action-2"
    DELETE_ROLE_BUTTON = "data-testid=primary-btn"
    DELETE_CONFIRM_BUTTON = 'button:has-text("Yes, Delete Role")'
    OK_STATUS = "data-testid=notification-status-ok"
    OK_STATUS_CLOSE_BTN = '[data-testid="notification-status-ok"] button'
    PERMISSION_DIALOG_TITLE = "[data-testid='page-title']"
    RESOURCE = "li:first-child"
    RESOURCE_NAME_TEMPLATE = "span:has-text('{}')"
    RESOURCE_OPT_TEMPLATE = "label:has-text('{}')"
    VIEW_DETAILS_ACTION = "[data-testid=action-0]"
    CUSTOM_ROLE_DROP_BUTTON = (
        "td:has(div:has(span:has-text('Custom'))) ~ td button[aria-label='Open Drop']"
    )
    CUSTOM_ROLE_VIEW_DETAILS_BUTTON = (
        "button[data-testid='action-0']:has-text('View Details')"
    )
    CUSTOM_ROLE_DUPLICATE_BUTTON = "button[data-testid='action-1']:has-text('Duplicate')"
    EDIT_CUSTOM_ROLE_PERMISSION_BUTTON = "button[data-testid='edit-permission-btn']"
    ADD_PERMISSION_BUTTON = "button[data-testid='permissions-create-btn']"
    SAVE_PERMISSION_BUTTON = "button[data-testid='permission-edit-save-btn']"
    PERMISSION_CHECKBOX_TICKED = (
        "label[label='{}'] svg > path[d='M6,11.3 L10.3,16 L18,6.2']"
    )
    DUPLICATE_EXISTING_ROLE_RADIO_BTN = 'span:has-text("Duplicate existing role")'


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
    USER_STATUS_TEMPLATE = 'tr:has-text("{}"):has(span:has-text("{}"))'
    TABLE_ACTION_BTN_TEMPLATE = "[data-testid=\"table\"] > tbody > tr:has(span:text-is('{}')) > td:last-child:has(button)"
    DELETE_BTN = 'button:text-is("Delete")'
    DELETE_CHECK_BTN = '[data-testid="delete-user-btn"]'
    DELETE_CONFIRM_BTN = '[data-testid="confirm-delete-user-btn"]'
    ASSIGN_BTN = "button:text-is('Assign Role')"
    POPUP_ASSIGN_ROLE_BUTTON = "[data-testid=two-buttons] [data-testid=assign-role-btn]"
    APPLICATIONS_SELECT_DROPDOWN = "button[id='applications-dropdown']"
    ROLES_DROPDOWN = "button[id='roles-dropdown']"
    ACCESS_RULE_DROPDOWN = "button[id='access-rules-dropdown']"
    CHANGE_ROLE_BUTTON = "data-testid=confirm-assignment-role-btn"
    RESOURCE_POLICY_TOGGLE = "[data-testid='toggle-btn-box']"
    RESOURCE_POLICY_DROPDOWN = '[data-testid="rrp-dropdown"]'
    RESOURCE_POLICY_OPT_TEMPLATE = "data-testid=option-{}"
    ROLES_DROPDOWN_OPT_TEMPLATE = "data-testid=option-{}"
    REMOVE_ROLE_OPT = "data-testid=action-1"
    REMOVE_ROLE_BTN = "data-testid=save-btn"
    ASSIGNED_ROLE_NOTIFICATION = (
        "[data-testid='notification-status-ok'] :has-text('role was assigned')"
    )
    DELETED_USER_NOTIFICATION = 'div[data-testid="notification-message"] span'
    RESEND_EMAIL_INVITE_BTN = 'button:text-is("Resend Email Invite")'
    CANCEL_DELETE_CONFIRM_BTN = '[data-testid="cancel-confirm-delete-btn"]'


class RRPSelectors:
    BACK_BUTTON = '[data-testid="identity-title"]'
    HEADING_PAGE_TITLE = '[data-testid="heading-page-title"]'
    SEARCH_FIELD = '[data-testid="search-field"]'
    TABLE_HEAD_COLUMNS = '[data-testid="table"]>thead>tr>th'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    TABLE_ROW_TEMPLATE = '[data-testid="table"]>tbody>tr:nth-child({})'
    APPLICATION_DROPDOWN = "data-testid=application-dropdown"
    CREATE_RRP_BTN = "data-testid=create-rrp-btn"
    RRP_NAME_INPUT = "data-testid=scope-name-input"
    NEXT_BUTTON = "data-testid=button-next"
    APPLICATION_NAME_TEMPLATE = "[data-testid=\"tile-title\"]:has-text('{}')"
    ADD_RESOURCES_BTN = 'button:has-text("Add Resources")'
    RESOURCE_DIALOG_TITLE = "[data-testid=scope-modal-title]"
    RESOURCE = "li:first-child"
    RESOURCE_NAME_TEMPLATE = "[data-testid='{}']"
    REOSOURCE_OPT_LOADER = '[data-testid="loader"]'
    RESOURCE_OPT_TEMPLATE = "label:has-text('{}') div:has(>input[type=\"checkbox\"])"
    ADD_BTN = "data-testid=add-resources-btn"
    FINISH_BUTTON = "data-testid=button-finish"
    OPEN_RRP_TEMPLATE = "span:has-text('{}')"
    RRP_ACTION_BUTTON = "data-testid=rrp-details-action-btn"
    DELETE_ACTION = "data-testid=action-0"
    DELETE_CONFIRMATION_TITLE = "[data-testid=delete-sg-confirm-title]"
    DELETE_POLICY_BUTTON = "[data-testid='primary-btn']"
    FILTER_BUTTON = "[data-testid='filter-search-btn']"
    FILTER_OPTION_TEMPLATE = "label:has(>span:text-is('{}')) div:has(>[type='radio'])"
    APPLY_FILTERS_BUTTON = "[data-testid='apply-filters-btn']"
    CLEAR_FILTERS_BUTTON = "[data-testid='clear-filters-anchor']"


class UserDetailSelectors:
    """User Detail Locators"""

    LOADER_SPINNER = '[data-testid*="loader-spinner"]'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    ASSIGN_ROLE_BTN = "[data-testid=assign-role-btn]"
    USER_APPLICATION_DROPDOWN = '[data-testid="applications-dropdown"]'
    USER_ROLES_DROPDOWN = '[data-testid="roles-dropdown"]'
    USER_ROLE_OPTION_TEMPLATE = "[data-testid='option-{}']"
    APPLICATION_DROP_DOWN = "[id='applications-dropdown__select-drop']"
    ASSIGN_ROLE_BUTTON = "[data-testid=assign-role-btn]"
    POPUP_ASSIGN_ROLE_BUTTON = "[data-testid=two-buttons] [data-testid=assign-role-btn]"
    CHANGE_ROLE_BUTTON = "[data-testid='confirm-assignment-role-btn']"
    ACCESS_RULE_DROPDOWN = "button[id='access-rules-dropdown']"
    RESOURCE_POLICY_TOGGLE = "[data-testid='toggle-btn-box']"
    RESOURCE_POLICY_DROPDOWN = "button[id='rrp-dropdown']"
    ROLES_DROPDOWN_OPT_TEMPLATE = "data-testid=option-{}"
    SEARCH_POLICY_INPUT = "input[placeholder='Search Resource Restriction Policies']"
    RESOURCE_POLICY_OPT_TEMPLATE = "data-testid=option-{}"
    REMOVE_ROLE_OPT = "data-testid=action-1"
    REMOVE_ROLE_BTN = "data-testid=save-btn"
    NOTIFICATION_OK = "[data-testid='notification-status-ok']"
    ASSIGNED_ROLE_NOTIFICATION = (
        "[data-testid='notification-status-ok'] :has-text('role was assigned')"
    )
    REMOVED_ROLE_NOTIFICATION = (
        "[data-testid='notification-status-ok'] :has-text('role was removed')"
    )
    USER_ACTIONS_BUTTON = '[data-testid="user-details-action-btn"]'
    ROLE_ACTIONS_BTN = '[data-testid="multipleactions-action-btn"]'
    CHECK_ROLE = "//tr[.//span[contains(text(),'{}')] and .//td[contains(., '{}')]]"
    ROLE_ACTION_BTN_TEMPLATE = "[data-testid^=action-]:text-is('{}')"
    ACTION_DROPDOWN = "[data-testid=user-details-action-btn] [aria-label='Open Drop']"


class RoleDetailsSelectors:
    BACK_BUTTON = '[data-testid="role-details_back-btn"]'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    ROLE_ACTION_BTN = '[data-testid="role-details-action-btn"]'
    DELETE_ROLE_BTN = '[data-testid="role-details_delete-role-btn"]'
    DELETE_ROLE_CONFIRM_BTN = '[data-testid="primary-btn"]'
    EDIT_BTN = "[data-testid=edit-btn]"
    EDIT_NAME_INPUT_BOX = '[data-testid="dynamic-form_name_text"]'
    EDIT_DESC_INPUT_BOX = '[data-testid="dynamic-form_description_textarea"]'
    EDIT_ROLES_SAVE_BTN = '[data-testid="roles-edit-save-btn"]'
    EDIT_PERMISSIONS_BTN = '[data-testid="edit-permission-btn"]'
    EDIT_ADD_PERMISSIONS_BTN = '[data-testid="add-permissions-btn"]'
    EDIT_PERMISSION_SAVE_BTN = '[data-testid="permission-edit-save-btn"]'
    SEARCH_FIELD = '[data-testid="search-permissions-field"]'
    RESOURCE_NAME_TEMPLATE = "span:has-text('{}')"
    RESOURCE = "li:first-child"
    RESOURCE_OPT_TEMPLATE = "label:has-text('{}')"
    CREATE_PERMISSION_BTN = "data-testid=permissions-create-btn"
