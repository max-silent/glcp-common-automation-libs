import logging


class ADDDeviceConstants:
    def __init__(self):
        logging.info("Initialize ADDDeviceConstants")

    @staticmethod
    def vgw_device_data():
        vgw_payload = {
            "vgw_payload_data": {
                "nonce": "4212d98d-3fae-4e27-80d0-aa32a3b1c05a",
                "cnonce": "ZjFkNDhiYTc2MDVmNTU1ZTQ5MzYyNmNjZmE5Zjg5ZmY=",
                "nc": "00000003",
                "response": "1c26aa996479e3359ef0b073172735bc",
            }
        }
        return vgw_payload

    @staticmethod
    def nontpm_device_data():
        nontpm_payload = {
            "nontpm_payload_data": {
                "nonce": "29eb8aae-0a98-447d-96a5-f463fb4a4723",
                "cnonce": "0B2D44EC8FF4C431A2F0BD3BCDD734462A21F8D7EF627F4BB43DA81D5EE33110",
                "nc": "00000001",
                "response": "3c4619b2037a11075bab1afe1f727950",
            }
        }
        return nontpm_payload
