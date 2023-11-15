import json
import logging
import os
import time

import urllib3

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger(__name__)


class ActivateBridgeCookies(Session):
    """
    Cookies AppSession API class
    """

    stored_sessions = {}

    def __init__(
        self, host, user, password, max_retries=3, retry_timeout=5, debug=True, **kwargs
    ):
        """
        Initializes the ActivateBridgeCookies session.
        Args:
            host (str): The host for the API.
            user (str): The user for authentication.
            password (str): The password for authentication.
            max_retries (int): The maximum number of retries for API calls. Default is 3.
            retry_timeout (int): The timeout between retries in seconds. Default is 5.
            debug (bool): Flag indicating whether to enable debug mode. Default is True.
            **kwargs: Additional keyword arguments.
        """
        log.info("Initializing Cookies for api calls")
        super().__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs
        )
        self.user = user
        self.password = password
        self.host = host
        self.base_url = f"https://{host}"
        self.token_json = None
        self.final_token = None
        self.headers = self.get_token()

    @property
    def __client_details(self):
        return self.base_url, self.user, self.password

    @staticmethod
    def __get_cluster_info_dict():
        cluster_info_file = "/configmap/data/infra_clusterinfo.json"
        with open(cluster_info_file) as cluster_info:
            cluster_info_json = cluster_info.read()
        return json.loads(cluster_info_json)

    @staticmethod
    def __get_hostname(hostname):
        if hostname.startswith("https://"):
            return hostname
        else:
            return f"https://{hostname}"

    def __store_current_session(self):
        self.stored_sessions[self.__client_details] = {"token": None, "session": None}

        cookie_dict = self.token_json
        cookie_string = "; ".join(
            [f"{key}={value}" for key, value in cookie_dict.items()]
        )
        headers = {"Content-Type": "application/json", "Cookie": cookie_string}
        self.final_token = headers
        self.stored_sessions[self.__client_details]["token"] = self.final_token
        self.stored_sessions[self.__client_details]["session"] = self.session
        self.stored_sessions[self.__client_details]["token_refresh_timestamp"] = int(
            time.time()
        )
        log.info(f"App session was stored successfully.")

    def __reuse_session(self, client_details):
        """
        :param client_details: key in format of tuple (host, sso_host, client_id, client_secret, scope)
         to get assigned session details
        """
        self.final_token = self.stored_sessions[client_details]["token"]
        self.session = self.stored_sessions[client_details]["session"]
        log.info(f"App session was accessed successfully for reusing.")

    def __purge_current_session(self):
        session_purged = self.stored_sessions.pop(self.__client_details, False)
        log.info("purge_current_session %s", session_purged)
        if session_purged:
            log.info(f"Stored App API session was purged successfully.")
        else:
            log.warning(
                f"There is no stored App API session, but session purge was requested for it"
            )

    def __set_headers(self):
        """Set the session headers"""
        self.session.headers = self.final_token

    def _get_app_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info(
                    "running in local env, configmap is not available, getting from settings.json"
                )
                cluster_config = self.get(f"{self.base_url}/settings.json")
                app_api_hostname = cluster_config["baseUrl"].replace("user", "app_api")
                return app_api_hostname
            else:
                cluster_info_dict = self.__get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    rw_region = cluster_info_dict.get("clusterinfo", {}).get(
                        "READ_WRITE_REGION"
                    )
                    app_api_hostname = (
                        cluster_info_dict.get("clusterinfo", {})
                        .get("HOSTNAMES", {})
                        .get(rw_region, {})
                        .get("ccs_activate_v1_device_url", {})
                    )
                    return self.__get_hostname(app_api_hostname)
                else:
                    app_api_hostname = (
                        cluster_info_dict.get("clusterinfo", {})
                        .get("HOSTNAMES", {})
                        .get("ccs_activate_v1_device_url", {})
                    )
                    return self.__get_hostname(app_api_hostname)
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_secondary_app_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info(
                    "running in local env, configmap is not available, getting from settings.json"
                )
                cluster_config = self.get(f"{self.base_url}/settings.json")
                prefix_base_url = cluster_config["baseUrl"].split(".")
                prefix_base_url[0] = (
                    cluster_config["baseUrl"].split(".")[0].replace("user", "app_api")
                    + "-r"
                )
                return ".".join(prefix_base_url)
            else:
                cluster_info_dict = self.__get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    if (
                        len(
                            (
                                cluster_info_dict.get("clusterinfo", {}).get(
                                    "LIST_OF_REGIONS", []
                                )
                            )
                        )
                    ) > 1:
                        all_regions = cluster_info_dict.get("clusterinfo", {}).get(
                            "LIST_OF_REGIONS", {}
                        )
                        region1 = all_regions[0]
                        region2 = all_regions[1]
                        rw_region = cluster_info_dict.get("clusterinfo", {}).get(
                            "READ_WRITE_REGION", {}
                        )
                        if rw_region == region1:
                            ro_region = region2
                        else:
                            ro_region = region1
                        secondary_app_api_hostname = (
                            cluster_info_dict.get("clusterinfo", {})
                            .get("HOSTNAMES", {})
                            .get(ro_region, {})
                            .get("ccs_activate_v1_device_url", {})
                        )
                        return self.__get_hostname(secondary_app_api_hostname)
                return None
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def get_token(self, set_auth_header=True):
        """Generates the token info from the sso
        :param set_auth_header: set or not value to object's Authorization header
        :return: Access Token if received successfully or None

        """

        if self.__client_details in self.stored_sessions:
            self.__reuse_session(self.__client_details)
        else:
            data = {"credential_0": self.user, "credential_1": self.password}

            response = self.post(
                f"https://{self.host}/LOGIN",
                data=data,
                ignore_handle_response=True,
                verify=False,
            )
            if response.status_code == 200:
                self.token_json = response.cookies.get_dict()
                if set_auth_header:
                    self.__set_headers()
                self.__store_current_session()
            else:
                return None

        return self.stored_sessions[self.__client_details]["token"]

    def refresh_token(self):
        """
        Refresh the token info from the authenticated session
        :return: Boolean (True or False)
        """

        session_stored = self.stored_sessions.get(self.__client_details)
        token_refresh_timestamp = (
            session_stored["token_refresh_timestamp"] if session_stored else 0
        )  # ?

        if int(time.time()) - token_refresh_timestamp > 300:
            self.__purge_current_session()
            return self.get_token()
        else:
            log.warning("Refresh token requested too frequently. Possible error")
            return False

    @staticmethod
    def validate_retriable_response(response):
        """
        Additional validation of retriable errors before going for retries
        :param response: Response object
        :return: True/False
        """
        if not response.headers.get("server") == "HPE":
            log.error("Server Header not found")
            return False
        return True
