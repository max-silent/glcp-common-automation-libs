class RolesSelectors:
    BACK_BUTTON = '[data-testid="identity-title"]'
    HEADING_PAGE_TITLE = '[data-testid="heading-page-title"]'
    CREATE_ROLE_BUTTON = '[data-testid="roles-create-btn"]'
    SEARCH_FIELD = '[data-testid="search-field"]'
    TABLE_HEAD_COLUMNS = '[data-testid="table"]>thead>tr>th'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    TABLE_ROW_TEMPLATE = '[data-testid="table"]>tbody>tr:nth-child({})'
    APPLICATION_DROPDOWN = "data-testid=application-dropdown"
    CREATE_ROLE = "data-testid=create-role-btn"
    ROLE_NAME_INPUT = "data-testid=role-name-input"
    NEXT_BUTTON = "data-testid=button-next"
    ADD_PERMISSIONS_BTN = "data-testid=add-permissions-btn"
    CREATE_PERMISSION_BTN = "data-testid=permissions-create-btn"
    FINISH_BUTTON = "data-testid=button-finish"
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


class UsersSelectors:
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
    CHANGE_ROLE_BUTTON = "data-testid=confirm-assignment-role-btn"
    RESOURCE_POLICY_TOGGLE = "[data-testid='toggle-btn-box']"
    RESOURCE_POLICY_DROPDOWN = '[data-testid="rrp-dropdown"]'
    ROLES_DROPDOWN_OPT_TEMPLATE = "data-testid=option-{}"
    REMOVE_ROLE_OPT = "data-testid=action-1"
    REMOVE_ROLE_BTN = "data-testid=save-btn"
    NOTIFICATION_OK_CLOSE_BTN = '[data-testid="notification-status-ok"] button'


class RRPSelectors:
    BACK_BUTTON = '[data-testid="identity-title"]'
    HEADING_PAGE_TITLE = '[data-testid="heading-page-title"]'
    SEARCH_FIELD = '[data-testid="search-field"]'
    TABLE_ROWS = '[data-testid="table"]>tbody>tr'
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


class RRPDetailsSelectors:
    BACK_BUTTON = '[data-testid="rrp-back-btn"]'
    EDIT_BUTTON = '[data-testid="edit-details-btn"]'
    EDIT_NAME_INPUT_BOX = '[data-testid="rrp-name-input"]'
    EDIT_DESC_INPUT_BOX = '[data-testid="scope-description-input"]'
    EDIT_DETAILS_SAVE_BTN = '[data-testid="details-edit-save-btn"]'
