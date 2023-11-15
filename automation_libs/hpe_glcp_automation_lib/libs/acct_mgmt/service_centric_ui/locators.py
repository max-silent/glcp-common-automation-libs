class AccountTypeSelectors:
    """
    Class for Account Type locators
    """

    ELIGIBILITY_HEADER = "h3:text-is('Check Your Eligibility')"
    CHECK_ELIGIBILITY_BUTTON = "[data-testid='check-eligibility-button']"
    CONVERT_ACCT_BUTTON = "[data-testid='convert-account-button']"
    CONFIRM_CONVERT_BUTTON = "[data-testid='submit-btn']"
    FORBIDDEN_CONVERSION_MESSAGE = "[data-testid='notification-message']"
    REMOVE_WORKSPACES_HEADER = "h3:text-is('Remove All Customer workspaces')"
    REVIEW_CUSTOMER_WORKSPACES_BUTTON = "[data-testid='remove-customer-account-button']"
    CONVERT_ACC_BTN = "[data-testid='convert-account-button']"
    SUBMIT_BTN = "[data-testid='submit-btn']"
    MANAGE_WORKSPACE_TITLE = "[data-testid='heading-page-title']"
    STEP_REMOVE_UNSUPPORTED_SERVICE_BUTTON = (
        "[data-testid='review-unsupported-apps-button']"
    )
    REVIEW_CUST_WORKSPACES = "[data-testid='remove-customer-account-button']"
    SDS_WS_TITLE = "[data-testid='heading-company-name']"
