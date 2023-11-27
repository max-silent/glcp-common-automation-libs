"""
My Applications page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.services.ui.my_services_page import MyServices

log = logging.getLogger(__name__)


class MyApplications(MyServices):
    """
    DEPRECATED! CONSIDER USING 'ServiceDetails()' INSTANTIATING INSTEAD OF 'ApplicationsDetails()'.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize My Applications page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize My Applications page object.")
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'MyApplications()' by 'MyServices()'."
        )
        super().__init__(page, cluster)

    def open_available_applications(self):
        """
        Navigate to Available Application page.
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'MyApplications()' by 'MyServices()'."
        )
        log.error(
            "This method is not relevant - please, use 'self.side_menu.navigate_to_catalog()' call "
            "from instance of 'MyServices' page-object class."
        )
        self.side_menu.navigate_to_catalog()

    @staticmethod
    def open_installed_application(app_uuid: str):
        """DEPRECATED!
        CONSIDER USING OF MyServices's 'self.side_menu.navigate_to_catalog()' OR 'self.click_launch_btn()' instead.

        Open an installed application
        :param app_uuid: application uuid
        :return: current instance of My Applications page object
        """
        error_message = (
            "This method is not relevant and 'MyApplications' class is deprecated! \n"
            "Please, use following methods from 'MyServices' class instance: \n"
            " - 'self.side_menu.navigate_to_catalog()' - to open service catalog page, \n"
            " - 'self.click_launch_btn()' - to launch specified service."
        )
        log.error(error_message)
        raise ValueError(error_message)

    def should_have_application(self, service_name: str):
        """DEPRECATED! CONSIDER USING OF MyServices's 'self.should_have_service()' instead.

         Check for the application existence
        :param service_name: service name
        :return: current instance of My Applications page object
        """
        error_message = (
            "This method is not relevant and 'MyApplications' class is deprecated! \n"
            "Instead - please, use 'MyServices' class' 'self.should_have_service()' method with \n"
            "corresponding arguments (i.e. use service name instead of uuid)."
        )
        log.error(error_message)
        self.should_have_service(service_name)
        return self

    def should_have_appplication(self, service_name: str):
        """DEPRECATED! CONSIDER USING OF MyServices's 'self.should_have_service()' instead."""
        return self.should_have_application(service_name)

    def should_have_my_services_link(self, name="My Services"):
        """DEPRECATED! CONSIDER USING OF MyServices's 'self.side_menu.should_have_side_menu_tab()' instead.
        Verify the link My Services
        :param name: (required) for the Service name
        :return: current instance of My Applications page object.
        """
        error_message = (
            "This method is not relevant and 'MyApplications' class is deprecated! \n"
            "Instead - please, use 'self.side_menu.should_have_side_menu_tab()' method \n"
            "of 'MyServices' class."
        )
        log.error(error_message)
        self.side_menu.should_have_side_menu_tab(name)
        return self

    def should_have_subscriptions_link(self, name="Subscriptions"):
        """DEPRECATED! CONSIDER USING OF MyServices's 'self.side_menu.should_have_side_menu_tab()' instead.
        Verify the link Subscriptions
         :param name: (required) for the Subscription name
        :return: current instance of My Applications page object.
        """
        error_message = (
            "This method is not relevant and 'MyApplications' class is deprecated! \n"
            "Instead - please, use 'self.side_menu.should_have_side_menu_tab()' method \n"
            "of 'MyServices' class."
        )
        log.error(error_message)
        self.side_menu.should_have_side_menu_tab(name)
        return self

    def should_have_catalog_link(self, name="Catalog"):
        """DEPRECATED! CONSIDER USING OF MyServices's 'self.side_menu.should_have_side_menu_tab()' instead.
        Verify the link Catalog
         :param name: (required) for the Catalog name
        :return: current instance of My Applications page object.
        """
        error_message = (
            "This method is not relevant and 'MyApplications' class is deprecated! \n"
            "Instead - please, use 'self.side_menu.should_have_side_menu_tab()' method \n"
            "of 'MyServices' class."
        )
        log.error(error_message)
        self.side_menu.should_have_side_menu_tab(name)
        return self
