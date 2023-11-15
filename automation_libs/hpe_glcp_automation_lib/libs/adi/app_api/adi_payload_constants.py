"""
Payloads templates for ADI App Api
"""
import logging

log = logging.getLogger(__name__)


class AdiInputPayload:
    """
    Preparing payloads for API method call.
    """

    def get_provisioning_info(self):
        info_list = [
            {"device_family": "IAP", "device_endpoint_url": "https://iap.prod.hpe.com"},
            {
                "device_family": "CONTROLLER",
                "device_endpoint_url": "https://controller.prod.hpe.com",
            },
            {
                "device_family": "COMPUTE",
                "device_endpoint_url": "https://compute.prod.hpe.com",
            },
            {
                "device_family": "STORAGE",
                "device_endpoint_url": "https://storage.prod.hpe.com",
            },
            {
                "device_family": "SWITCH",
                "device_endpoint_url": "https://switch.prod.hpe.com",
            },
        ]
        return info_list.copy()

    def app_category_for_device_type(self):
        # Mapping of device types to their respected categories.
        device_category = {
            "AP": "NETWORK",
            "ALS": "NETWORK",
            "BLE": "NETWORK",
            "CONTROLLER": "NETWORK",
            "SWITCH": "NETWORK",
            "GATEWAY": "NETWORK",
            "IAP": "NETWORK",
            "LTE_MODEM": "NETWORK",
            "STORAGE": "STORAGE",
            "DHCI_STORAGE": "STORAGE",
            "COMPUTE": "COMPUTE",
            "SENSOR": "NETWORK",
        }
        return device_category
