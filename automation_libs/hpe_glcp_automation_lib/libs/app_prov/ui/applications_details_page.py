import logging

from hpe_glcp_automation_lib.libs.services.ui.service_details_page import ServiceDetails

log = logging.getLogger()


class ApplicationsDetails(ServiceDetails):
    """
    DEPRECATED! CONSIDER USING 'ServiceDetails()' INSTANTIATING INSTEAD OF 'ApplicationsDetails()'.
    """

    def __init__(self, *args, **kwargs):
        log.info(f"Playwright: Initialize application details page.")
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'ApplicationsDetails()' by 'ServiceDetails()'."
        )

        transformed_kwargs = dict()
        transformed_kwargs["page"] = kwargs.get(
            "page", args[0] if len(args) > 0 else None
        )
        transformed_kwargs["cluster"] = kwargs.get(
            "cluster", args[1] if len(args) > 1 else None
        )
        transformed_kwargs["service_name"] = kwargs.get(
            "service_name", args[2] if len(args) > 2 else None
        )
        if not all(transformed_kwargs.values()):
            raise ValueError(
                "Incorrect set of arguments to invoke constructor of parent class 'ServiceDetails'"
            )
        super().__init__(**transformed_kwargs)

    def setup_application(self, region: str):
        """DEPRECATED! CONSIDER USING OF METHOD 'deploy_service' instead.
        Deploy service at given region.

        :param region: region.
        :return: current instance of ServiceDetails page object.
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'ApplicationsDetails()' by 'ServiceDetails()'."
        )
        return self.deploy_service(region)

    def add_regions_to_installed_application(self, region: str):
        """DEPRECATED! CONSIDER USING OF METHOD 'deploy_service' instead.
        Open an installed application
        :param : region to deploy application
        :return: current instance of My Applications page object
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'ApplicationsDetails()' by 'ServiceDetails()'."
        )
        return self.deploy_service(region)

    def should_have_setup_application(self):
        """DEPRECATED! CONSIDER USING OF METHOD 'should_have_provision_button' instead.
        Check if set up application button
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'ApplicationsDetails()' by 'ServiceDetails()'."
        )
        return self.should_have_provision_button()

    def should_not_have_setup_application(self):
        """DEPRECATED! CONSIDER USING OF METHOD 'should_not_have_provision_button' instead.
        Check if set up application button not present
        """
        log.error(
            f"NOTE: PLEASE REPLACE CALL OF DEPRECATED 'ApplicationsDetails()' by 'ServiceDetails()'."
        )
        return self.should_not_have_provision_button()
