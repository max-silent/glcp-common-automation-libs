class InstalledAppsSelectors:
    """Selectors, used in "InstalledApplications" class.
    Related URL: ".../applications/installed-apps/{app_uuid}".
    NOTE: DEPRECATED! (Not applicable to service-centric UI).
    """

    MY_APPS = "[data-testid='my-apps-back-btn']"
    INSTALLED_APP_TEMPLATE = '[data-testid="installed-app-{}"]'
    APP_ACTION_BTN_TEMPLATE = (
        '[data-testid="installed-app-{}"] [data-testid="installed-app-list-action-btn"]'
    )
    LAUNCH_APPS_BTN_TEMPLATE = (
        '[data-testid="installed-app-{}"] [data-testid="launch-action-btn"]'
    )
    APP_NAME_HEADER = '[data-testid="heading-page-title"]'
    ACTION_REMOVE_REGION = "button:has-text('Remove Region')"
    REMOVE_APPS_MODAL = '[data-testid="remove-apps-modal"]'
    TERM_CHECKBOX = '[data-testid="app-term-form"]'
    REMOVE_REGION_BTN = '[data-testid="remove-region-btn"]'
    KEEP_REGION_BTN = '[data-testid="cancel-btn"]'
    APP_SPINNER = '[data-testid="loader-spinner"]'
