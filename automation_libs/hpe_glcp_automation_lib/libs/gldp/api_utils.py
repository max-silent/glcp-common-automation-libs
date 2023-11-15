"""
This module contains reusable methods for data-plane API automation
"""
import json
import logging

import requests
from jsonpath_ng import parse
from jsonschema import validate

logging.basicConfig(level="DEBUG")
log = logging.getLogger("sdk api utils")


class ApiUtils:
    """
    This class has all the reusable methods for making API calls
    """

    @staticmethod
    def validate_status_code(response, code):
        """
        This method is to validate the response code
        :param response: response object received from the api call
        :param code: expected status code
        :return:
        """
        assert response.status_code == code, (
            f"status code doesn't meet with expected. Actual: "
            f"{response.status_code} and Expected: {code} "
        )
        log.info(
            "Status code validation is successful for given response, response: \n %s",
            response.text,
        )

    @staticmethod
    def validate_response_schema(response, exp_schema):
        """
        This method is to validate response schema
        :param response: response object received from the api call
        :param exp_schema: expected schema
        :return:
        """
        try:
            validate(instance=json.loads(response.text), schema=json.loads(exp_schema))
            log.info(
                "Schema validation is successful for given response, " "response: \n %s",
                response.text,
            )
        except Exception as exp:
            log.error(
                "Exception validating response schema. Response is:"
                " \n %s \n and exception is: \n %s",
                response,
                exp,
            )

    @staticmethod
    def validate_attribute_values(response, attr_dict):
        """
        This method is to validate the attributes from the response body
        :param response: Given response to validate the attribute values
        :param attr_dict: This must be in the form of dictionary
        for example : {'$.level1.level2.level3':"expected value"}
        :return:
        """
        json_response = json.loads(response.text)
        assert isinstance(
            attr_dict, dict
        ), "Expected attr_dict should be in the dict format"
        assert len(attr_dict) > 0, "Given attr_dict is empty"
        for path, value in attr_dict.items():
            jsonpath_expr = parse(path)
            act_attr_value = jsonpath_expr.find(json_response)[0].value
            if act_attr_value.strip() == value:
                log.info(
                    "Attribute validation is successful for path: '%s'. " "value is: %s",
                    path,
                    value,
                )
            else:
                log.error(
                    "Attribute validation is failed for path: '%s'. "
                    "actual: %s and expected: %s",
                    path,
                    act_attr_value,
                    value,
                )

    @staticmethod
    def retrieve_attribute_value(response, attr_path):
        """
        This method is to validate the attributes from the response body
        :param response: Given response to validate the attribute values
        :param attr_path: jsonpath to retrieve the value
        for example : '$.level1.level2.level3'
        :return: str | list
        """
        json_response = json.loads(response.text)
        assert len(attr_path) > 0, "Given attr_path is empty"
        matches = parse(attr_path).find(json_response)
        extracted_attr_value = [match.value for match in matches]
        assert extracted_attr_value, f"Attribute values for path: '{attr_path}' is Empty"
        log.info(
            "Attribute values for path: '%s' is : %s", attr_path, extracted_attr_value
        )
        return (
            extracted_attr_value
            if len(extracted_attr_value) > 1
            else extracted_attr_value[0]
        )

    @staticmethod
    def api_post_call(endpoint, request_body, headers=None, authentication=None):
        """
        This method is to perform POST operation on the given
        endpoint with payload
        :param endpoint: Service host name
        :param request_body: body of the request
        :param headers: Headers for the POST call, must include Content-Type
        if the given body is not json
        :param authentication: auth token to verify the authentication
        :return: response object

        Note: Content-Type is mandatory in headers if we use data for POST
        """
        return ApiUtils.api_request_with_payload_call(
            "POST",
            endpoint,
            request_body,
            headers=headers,
            authentication=authentication,
        )

    @staticmethod
    def api_get_call(endpoint, params=None, headers=None, authentication=None):
        """
        This method is to perform GET operation on the given endpoint
        :param endpoint: Service host name
        :param params:
        :param headers: Headers for the GET call
        :param authentication: auth token to verify the authentication
        :return:
        """
        log.info("the endpoint is %s ", endpoint)
        assert endpoint is not None, "Given endpoint is None"
        response = None
        try:
            response = requests.get(
                endpoint, params=params, headers=headers, auth=authentication
            )
            log.info(
                "Response after making get call to: %s, response: \n %s",
                endpoint,
                response.text,
            )
        except requests.exceptions.RequestException as exp:
            log.error(
                "Caught exception while making get call to : %s, " "with error : \n %s",
                endpoint,
                exp,
            )
        assert response is not None, "Response received from GET " "API call is None"
        return response

    @staticmethod
    def api_delete_call(endpoint, request_body=None, headers=None, authentication=None):
        """
        This method is to perform DELETE operation on the given endpoint
        :param request_body:
        :param endpoint: Service host name
        :param params:
        :param headers: Headers for the GET call
        :param authentication: auth token to verify the authentication
        :return:
        """
        return ApiUtils.api_request_with_payload_call(
            "DELETE",
            endpoint,
            request_body,
            headers=headers,
            authentication=authentication,
        )

    @staticmethod
    def api_patch_call(endpoint, request_body, headers=None, authentication=None):
        """
        This method is to perform PUT or PATCH operation on the given
        endpoint with payload
        :param endpoint: Service host name
        :param request_body: body of the request
        :param headers: Headers for the PATCH call, must include Content-Type
        if the given body is not json
        :param authentication: auth token to verify the authentication
        :return: response object
        Note: Content-Type is mandatory in headers if we use data for PATCH
        """
        return ApiUtils.api_request_with_payload_call(
            "PATCH",
            endpoint,
            request_body,
            headers=headers,
            authentication=authentication,
        )

    @staticmethod
    def api_put_call(endpoint, request_body, headers=None, authentication=None):
        """
        This method is to perform PUT or PUT operation on the given
        endpoint with payload
        :param endpoint: Service host name
        :param request_body: body of the request
        :param headers: Headers for the PATCH call, must include Content-Type
        if the given body is not json
        :param authentication: auth token to verify the authentication
        :return: response object
        Note: Content-Type is mandatory in headers if we use data for PATCH
        """
        return ApiUtils.api_request_with_payload_call(
            "PUT",
            endpoint,
            request_body,
            headers=headers,
            authentication=authentication,
        )

    @staticmethod
    def api_request_with_payload_call(
        method, endpoint, request_body=None, headers=None, authentication=None
    ):
        """
        This method is to perform PUT or PATCH operation on the given
        endpoint with payload
        :param method: Type of method to perform
        :param endpoint: Service host name
        :param request_body: body of the request
        :param headers: Headers for the PATCH call, must include Content-Type
        if the given body is not json
        :param authentication: auth token to verify the authentication
        :return: response object
        Note: Content-Type is mandatory in headers if we use data for PATCH
        """
        assert endpoint is not None, "Given endpoint is None"
        if method != "DELETE":
            assert request_body is not None, "Given request body is None"
        is_body_json = False
        response = None
        if isinstance(request_body, dict):
            is_body_json = True
            log.info("Request body is json, so using json for making call")
        else:
            log.info("Request body is not json, so using data for making call")
        try:
            if is_body_json:
                response = requests.request(
                    method=method,
                    url=endpoint,
                    json=request_body,
                    headers=headers,
                    auth=authentication,
                )
            else:
                response = requests.request(
                    method=method,
                    url=endpoint,
                    data=request_body,
                    headers=headers,
                    auth=authentication,
                )
            log.info(
                "Response after making %s call to: %s , response: \n %s",
                method,
                endpoint,
                response.text,
            )
        except requests.exceptions.RequestException as exp:
            log.error(
                "Caught exception while making %s call to : %s, " "with error : \n %s",
                method,
                endpoint,
                exp,
            )
        assert response is not None, f"Response received from {method} API call is None"
        return response
