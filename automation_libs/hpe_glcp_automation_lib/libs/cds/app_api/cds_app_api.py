"""
Consumption Data Service app apis
"""
import logging

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class ConsumptionDataServiceApp(AppSession):
    """
    ConsumptionDataService(CDS) App API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize ConsumptionDataService class
        :param host: cluster under test app api url
        :param sso_host: sso_host url
        :param client_id: app api client_id
        :param client_secret: app api client secret
        """
        log.info("Initializing cds_app_api for app api calls")
        super(ConsumptionDataServiceApp, self).__init__(
            host, sso_host, client_id, client_secret
        )
        self.get_token()
        self.base_path = "/cds"
        self.api_version_v1 = "/v1"
        self.api_version_v2 = "/v2"

    def get_service_instance_id(self, license_key, offering_id):
        """
        Method to get a ServiceInstanceID for a particular SubscriptionKey
        :param license_key: Subscription Key of a particular Service
        :param offering_id: UniqueId of a Particular Service
        :returns ServiceInstanceId
        """
        url = f"{self.base_url}{self.base_path}{self.api_version_v1}/offering-meterdata/{offering_id}/provision/{license_key}"
        return self.post(url)["serviceInstanceId"]

    def upload_resources(self, service_instance_id, input_date, payload, segment=1):
        """
        Method to Upload Resources for a given ServiceInstanceID and date
        :param service_instance_id: Service Instance ID of a particular License Key
        :param input_date: date for which resources to be uploaded
        :param payload: payload to be used for current requests
        :param segment: segment ID based on region/resource
        :returns JSON body
        """
        input_date = input_date.replace("-", "")
        url = f"{self.base_url}/gateway{self.api_version_v2}/usage/upload/json/{service_instance_id}/{input_date}"
        return self.put(url, data=payload, params={"segment": segment})

    def get_instance_summary(self, service_instance_id, date):
        """
        Method to get information about the processing status of uploaded CDS data for the given instance and date
        :param service_instance_id: Service Instance ID of a particular License Key
        :param date: date for which uploaded status to be fetched. Format supported is yyyyMMdd
        :returns JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version_v2}/usage/{service_instance_id}/status/{date}"
        return self.get(url)
