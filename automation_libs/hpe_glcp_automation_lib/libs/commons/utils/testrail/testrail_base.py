import base64
import json
import logging

import requests

from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_defines import (
    TestRailError,
)

LOG = logging.getLogger(__name__)


class TestRailBase(object):
    """
    Base class based on testrail documentation for API
    """

    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.__url = base_url + "index.php?/api/v2/"

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)

    def __send_request(self, method, uri, data) -> dict:
        url = self.__url + uri

        auth = str(
            base64.b64encode(bytes("%s:%s" % (self.username, self.password), "utf-8")),
            "ascii",
        ).strip()
        headers = {"Authorization": "Basic " + auth}

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = {"attachment": (open(data, "rb"))}
                response = requests.post(url, headers=headers, files=files)
                files["attachment"].close()
            else:
                headers["Content-Type"] = "application/json"
                payload = bytes(json.dumps(data), "utf-8")
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except Exception as e:  # response.content not formatted as JSON
                LOG.error(e)
                error = str(response.content)
            raise TestRailError(
                "TestRail API returned HTTP %s (%s)" % (response.status_code, error)
            )
        else:
            if uri[:15] == "get_attachment/":  # Expecting file, not JSON
                try:
                    open(data, "wb").write(response.content)
                    return data
                except Exception as e:
                    LOG.error(e)
                    return {"error": "Error saving attachment."}
            else:
                try:
                    return response.json()
                except Exception as e:  # Nothing to return
                    LOG.error(e)
                    return {}
