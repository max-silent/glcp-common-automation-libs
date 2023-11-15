import io
import json
import logging
import os
import socket
from os import path

import requests

if os.getenv("POD_NAMESPACE") is not None:
    import hashlib

    import M2Crypto
    import M2Crypto.BIO
    import M2Crypto.RSA
log = logging.getLogger(__name__)

CLUSTER_PORT = 443
CLUSTER_INFO_FILE = "/configmap/data/infra_clusterinfo.json"


class CloudActivationKeyHelper:
    def __init__(self):
        self.activate_v2_device_url = "devices-v2.arubanetworks.com"
        self.activate_v1_device_url = "device.arubanetworks.com"
        self.DEVICE_PROVISION_URL = None
        self.CCS_DEVICE_URL = None

    def resolve_device_hostname_to_IP(self, device_type=None):
        """
        Resolves DNS name for CCS_DEVICE_URL to IP address
        :return: IP address resolved to CCS_DEVICE_URL
        """
        device_endpoint_ip = None
        log.info("\nEntering resolve_device_hostname_to_IP")

        with open(CLUSTER_INFO_FILE) as cluster_info:
            cluster_info_json = cluster_info.read()
            log.debug("Read cluster_info file as:\n {}.".format(cluster_info_json))
            cluster_info_dict = json.loads(cluster_info_json)
            envs = cluster_info_dict["clusterinfo"]["HOSTNAMES"]
            if device_type == "SWITCH":
                self.CCS_DEVICE_URL = (
                    envs[cluster_info_dict["clusterinfo"]["READ_WRITE_REGION"]][
                        "ccs_activate-v2_hostname"
                    ]
                    if "READ_WRITE_REGION" in cluster_info_dict["clusterinfo"]
                    else envs["ccs_activate-v2_hostname"]
                )
            else:
                self.CCS_DEVICE_URL = (
                    envs[cluster_info_dict["clusterinfo"]["READ_WRITE_REGION"]][
                        "ccs_activate-v1_hostname"
                    ]
                    if "READ_WRITE_REGION" in cluster_info_dict["clusterinfo"]
                    else envs["ccs_activate-v1_hostname"]
                )

        log.info("\nAttempting to resolve: {}".format(self.CCS_DEVICE_URL))
        device_endpoint_ip = socket.gethostbyname(self.CCS_DEVICE_URL)
        log.info("\nDevice endpoint IP : {}".format(device_endpoint_ip))
        return device_endpoint_ip

    def make_entry_in_pods_hosts_file(self, device_endpoint_ip, device_endpoint_url):
        """
        add Hostname and IP to /etc/hosts file
        :param device_endpoint_ip: CCS_DEVICE_URL
        :param device_endpoint_url: hpe_device_url or aruba_device_url
        """
        try:
            with open("/etc/hosts", "a") as f:
                f.write("\n{} {}".format(device_endpoint_ip, device_endpoint_url))
            with open("/etc/hosts", "r") as f:
                hosts_file = f.read()
                log.info("IP : {}".format(hosts_file))
        except Exception as e:
            log.error("\nUnable to add Hostname and IP to /etc/hosts file!\n".format(e))

    def get_cloud_activation_key_for_switch_device(
        self, serial_number, mac_address, part_number, certs
    ):
        """This helper function accepts serial, mac and part number and returns X-Activation-Key
        for IAP device claim in ADI

        :param serial_number: serial number of switch device
        :param mac_address: mac_address of switch device
        :param part_number: part_number of switch device
        :param certs: cert_validation - use switch certs in the param
        :return: could-activation-key (CAK)
        """

        cluster_device_endpoint_ip = self.resolve_device_hostname_to_IP(
            device_type="SWITCH"
        )
        method = "post"
        endpoint = "hpe-provision"
        ap_info = serial_number + "," + mac_address + "," + part_number
        headers = {
            "X-Type": "provision-update",
            "X-Mode": "SWITCH",
            "X-Oem-Tag": "Aruba",
            "X-Forwarded-For": "2.3.4.5",
            "X-ssl-client-s-dn": "central.com",
            "X-Forwarded-Host": "devices-v2.arubanetworks.com",
            "X-ssl-client-verify": "SUCCESS",
            "X-Ap-Info": ap_info,
            "Content-Type": "application/json",
        }
        test_params = {
            "path_params": [],
            "request_headers": headers,
            "request_body": {},
            "cert": certs,
        }
        self.make_entry_in_pods_hosts_file(
            device_endpoint_ip=cluster_device_endpoint_ip,
            device_endpoint_url=self.activate_v2_device_url,
        )
        self.DEVICE_PROVISION_URL = (
            f"https://{self.activate_v2_device_url}:{CLUSTER_PORT}"
        )
        log.info(
            "\nRESOLVED IP FOR DEVICE ENDPOINT AND MADE ENTRY IN ETC/HOSTS FILE FOR POD\n"
        )

        response = getattr(self, method.lower())(
            endpoint,
            headers=headers,
            cert=test_params["cert"]["cert"],
            key=test_params["cert"]["key"],
            ca_cert=test_params["cert"]["ca_cert"],
        )

        logging.debug(
            "\nResponse from server for final provision: {} \nheaders: {} \nstatus_code: {}".format(
                response.text, response.headers, response.status_code
            )
        )
        cak = response.headers["X-Activation-Key"]
        return cak

    def get_cloud_activation_key_for_iap_device(
        self, serial_number, mac_address, part_number, certs
    ):
        """This helper function accepts serial, mac and part number and returns X-Activation-Key
        for IAP device claim in ADI

        :param serial_number: serial number of iap device
        :param mac_address: mac_address of iap device
        :param part_number: part_number of iap device
        :param certs: cert_validation - use iap certs in the param
        :return: could-activation-key (CAK)
        """

        cluster_device_endpoint_ip = self.resolve_device_hostname_to_IP(device_type="IAP")
        self.make_entry_in_pods_hosts_file(
            device_endpoint_ip=cluster_device_endpoint_ip,
            device_endpoint_url=self.activate_v1_device_url,
        )
        iap_endpoint = "provision"
        act_url = f"https://{self.activate_v1_device_url}:{CLUSTER_PORT}/{iap_endpoint}"
        fw = "8.5.0.5-8.5.0.5_73491"
        ap_info = serial_number + "," + mac_address + "," + part_number
        headers = {
            "Content-Length": str(0),
            "X-Type": "provision-update",
            "X-Mode": "IAP",
            "X-Oem-Tag": "Aruba",
            "X-Current-Version": fw,
            "X-Organization": None,
            "X-Ap-Info": ap_info,
            "Connection": "Keep-Alive",
        }
        resp = requests.post(act_url, verify=False, headers=headers)
        session_id = resp.headers.get("X-Session-Id")
        challenge = resp.headers.get("X-Challenge")
        challenge1 = challenge.encode("utf-8")
        log.debug(
            "Response from server for challenge {} {} {}".format(
                resp.status_code, resp.headers, session_id
            )
        )
        pkey = M2Crypto.RSA.load_key(certs["key"])
        Signature = pkey.sign(hashlib.sha1(challenge1).digest())
        k = io.open((certs["cert"]), mode="r", encoding="utf-8")
        data1 = k.read().encode("utf-8")
        data2 = Signature
        data = data1 + "\n".encode() + data2
        length = len(data)
        headers = {
            "x-req-ver-key": str(pkey),
            "content-type": "text/plain;charset=utf-8",
            "content-length": str(length),
            "X-Type": "provision-update",
            "X-Mode": "IAP",
            "X-Oem-Tag": "Aruba",
            "X-Current-Version": fw,
            "X-Ap-Info": ap_info,
            "X-Session-Id": session_id,
            "X-Challenge": challenge,
            "X-Challenge-Hash": "SHA-1",
            "Connection": "close",
        }
        log.debug("Request from client for challenge {}".format(headers))
        resp = requests.post(act_url, verify=False, headers=headers, data=data)
        log.debug(
            "Response from server for final provision {} {} {}".format(
                resp.headers, resp.status_code, session_id
            )
        )

        cak = resp.headers["X-Activation-Key"]
        return cak

    def post(self, endpoint, cert="", key="", ca_cert=False, headers={}):
        """
        Make get api_request
        :param api_path: for switch device type
        :param cert: path to cert
        :param key: path to key
        :param ca_cert: cert_validation
        :param headers: request headers
        :return: response
        """
        if self.device_ca_file:
            self.device_ca_file = ca_cert
        log.info(
            "\nProcessing POST on URL - {}, with headers - {} \n".format(
                path.join(self.DEVICE_PROVISION_URL, endpoint), headers
            )
        )
        response = requests.post(
            path.join(self.DEVICE_PROVISION_URL, endpoint),
            cert=(cert, key),
            headers=headers,
            verify=self.device_ca_file,
        )
        return response
