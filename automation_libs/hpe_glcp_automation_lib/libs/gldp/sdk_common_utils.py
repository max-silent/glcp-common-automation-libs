"""
This Module contains all the reusable common methods for sdk
"""
from urllib.parse import urljoin


class SdkCommonUtils:
    """
    This Class contains all the reusable common methods for sdk
    """

    @staticmethod
    def url_join(host_name, list_path_params: list):
        """
        This method constructs the url with hostname and list of path parameters
        :param host_name: Host name of the service
        :param list_path_params: list of path parameters
        :return:
        """
        path_param = "/".join(map(lambda s: s.strip("/"), list_path_params))
        return urljoin(host_name, path_param)
