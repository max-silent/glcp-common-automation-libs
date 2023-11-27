import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.app_prov.ui.applications_details_page import (
    ApplicationsDetails,
)
from hpe_glcp_automation_lib.libs.services.ui.service_catalog_page import ServiceCatalog

log = logging.getLogger()


class AvailableApplications(ServiceCatalog):
    """
    Available Applications Page Object Model
    """

    def __init__(self, page: Page, cluster: str):
        """
         Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Playwright: Initialize available apps page.")
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'AvailableApplications()' by 'ServiceCatalog()'."
        )
        super().__init__(page, cluster)

    def wait_for_loaded_list(self):
        """DEPRECATED! CONSIDER USING OF ServiceCatalog's 'wait_for_loaded_list()' instead.
         Wait for list of applications is not empty and loader spinner is not present on the page.
        :return: current instance of Available Applications page object.
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'AvailableApplications()' by 'ServiceCatalog()'."
        )
        super().wait_for_loaded_list()
        return self

    def open_view_details_on_application(self, service_name: str):
        """DEPRECATED! CONSIDER USING OF ServiceCatalog's 'open_service()' instead.
        click on the view details to open the application.
        :param service_name: service name.
        :return instance of ApplicatonDetails.
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'AvailableApplications()' by 'ServiceCatalog()'."
        )
        self.open_service(service_name)
        return ApplicationsDetails(self.page, self.cluster, service_name)

    def should_have_application(self, service_name: str):
        """DEPRECATED! CONSIDER USING OF ServiceCatalog's 'should_have_service()' instead.
         Check for the application existence.
        :param service_name: service name.
        :return: current instance of Available Applications page object.
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'AvailableApplications()' by 'ServiceCatalog()'."
        )
        log.error(
            f"NOTE: use correct arguments of 'should_have_service()' (i.e. use service name instead of uuid)."
        )
        self.should_have_service(service_name)
        return self

    def should_have_appplication(self, service_name: str):
        """DEPRECATED! CONSIDER USING OF ServiceCatalog's 'should_have_service()' instead."""
        return self.should_have_application(service_name)

    def open_my_applications(self):
        """DEPRECATED!
        CONSIDER USING OF ServiceCatalog's 'self.side_menu.navigate_to_my_services()' INSTEAD.

        Navigate to My Application page.
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'AvailableApplications()' by 'ServiceCatalog()'."
        )
        self.side_menu.navigate_to_my_services()
