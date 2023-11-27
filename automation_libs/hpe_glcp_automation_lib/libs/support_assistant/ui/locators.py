class SupportCenterSelectors:
    """Selectors, used in "SupportCenter" class.
    Related URL: "https://support.hpe.com/hpesc/public/docDisplay?docId=a00120892en_us".
    """

    PAGE_LOADER = "#loading_document"
    LINKS_LOADER = "a[title='Loading']"
    USER_GUIDE_TITLE = "a:text-is('HPE GreenLake Edge to Cloud Platform User Guide')"
    WELCOME_HPE_GLE_ETC_PLATFORM = (
        "#contentListArea :text-is('Welcome to HPE GreenLake edge-to-cloud platform')"
    )
    DASHBOARD_DOCUMENT = "#contentListArea :text-is('Dashboard')"
    APPLICATIONS_DOCUMENT = "#contentListArea :text-is('Applications')"
    DEVICES_DOCUMENT = "#contentListArea :text-is('Devices')"
    MANAGE_DOCUMENT = "#contentListArea :text-is('Manage')"
    DOCUMENTATION_FEEDBACK = "#contentListArea :text-is('Documentation feedback')"


class BillingSelectors:
    """Selectors, used in "BillingAndSubscription" class.
    Related URL: "https://h41390.www4.hpe.com/support/index.html?form=osqbm".
    """

    PAGE_HEADING_TEMPLATE = "header>h1:text-is('{}')"


class OnBoardingSelectors:
    """
    Selectors, used in "OnBoardingUserWorkspace" class.
    Related URL: "https://h41390.www4.hpe.com/support/index.html?form=glsupport".
    """

    PAGE_HEADING_TITLE = "header>h1:text-is('HPE GreenLake Platform Support')"
