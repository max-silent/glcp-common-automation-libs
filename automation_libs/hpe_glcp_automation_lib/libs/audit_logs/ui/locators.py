class AuditLogsSelectors:
    LOADER_SPINNER = '[data-testid*="loader-spinner"]'
    PAGE_TITLE = "[data-testid='auditlog-page-header'] h1"
    SEARCH_FIELD = '[data-testid="search-field"]'
    NO_AUDIT_LOG_DATA = "[data-testid='no-audit-log-data']"
    TABLE_ROWS_COUNT = '[data-testid="table-summary"]>div>div:first-of-type>span'
    TABLE_ROW_TEMPLATE = '[data-testid="table"]>tbody>tr:nth-child({})'
    EDIT_COLUMNS_BTN = "[data-testid='edit-columns-btn']"
    EDIT_COLS_MODAL_DIALOG = "[data-testid='filter-modal-dialog']"
    TABLE_COLUMNS = (
        "[data-testid='editColumnsList'] > label:not([disabled]) input[checked]+div"
    )
    RESET_DEFAULT_COLS_BTN = "[data-testid='reset-filter-btn']"
    SAVE_EDIT_COLS_BTN = "[data-testid='apply-filters-btn']"
    SELECT_COLS_TEMPLATE = (
        "[data-testid='editColumnsList'] > label:not([disabled]) input[name='{}']+div"
    )
    AUDIT_LOGS_TABLE_ROWS = '[data-testid="table"]>tbody>tr'
    AUDIT_LOG_DESCRIPTION = '[data-testid="heading-audit-log-details"] div'
    DETAIL_CLOSE_BUTTON = '[data-testid="close-button"]'
    LOG_ENTRY_CHECK = "(//span[contains(., '{category}')]/ancestor::tr[contains(.,'{description}') and \
    contains(., '{user_name}') and contains(., '{account_name}')])[1]"

    ADVANCED_SEARCH = '[data-testid="advanced-search-btn"]'
    CLEAR_FILTERS_BUTTON = '[data-testid="clear-filters-anchor"]'

    # Advanced search popup elements
    ADV_SEARCH_FIELD_TEMPLATE = (
        "div[data-testid^='form-field']:has(>label):has(:text-is('{}')) input"
    )
    ADV_SEARCH_CATEGORY_TEMPLATE = (
        "div[data-testid^='form-field']:has(label:text-is('Category')) label[label='{}']"
    )
    ADV_SEARCH_CUSTOM_DATE_FIELD = "div:has(>div>span:text-is('Custom Date')) input"
    ADV_SEARCH_SAVE_BUTTON = '[data-testid="apply-filters-btn"]'

    EXPORT_LOG_BUTTON = 'button[data-testid="export-auditlog-btn"]'
    CONTINUE_BUTTON = 'button[data-testid="continue-btn"]'
    FILE_TYPE_TO_BE_EXPORTED_TEMPLATE = (
        "[data-testid='download-auditlogs-option-radio-btn']> div > label[for='{}']"
    )
    TABLE_COLUMNS_TEXT_TEMPLATE = "table th :text-is('{}')"
