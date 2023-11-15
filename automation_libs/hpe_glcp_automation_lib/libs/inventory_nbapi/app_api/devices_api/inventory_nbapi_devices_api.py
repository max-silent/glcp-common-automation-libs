"""
Inventory NBAPI Devices APIs
TODO: Docs link pending
"""
import logging
import time

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession
from hpe_glcp_automation_lib.libs.inventory_nbapi.helpers.helpers import NBAPIHelpers

log = logging.getLogger()


class InventoryNBAPIDevices(AppSession):
    """
    Inventory NBAPI Unified Devices API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        log.info("Initializing inventory_nbapi_devices_api for api calls")
        self.base_url = host
        super(InventoryNBAPIDevices, self).__init__(
            host, sso_host, client_id, client_secret, scope=""
        )
        self.base_path = "/devices"
        self.api_version = "/v1beta1"
        self.devices_url = f"{self.base_url}{self.base_path}{self.api_version}"

    def get_devices(
        self,
        limit=None,
        offset=None,
        filter_query=None,
        filter_tags=None,
        sort=None,
        select=None,
        tuple_response=True,
        ignore_handle_response=True,
    ):
        """
        Get the device detail of the claimed devices of the platform customer account, who submits the request,
        after applying the paging, filtering, and sorting optional query parameters.
        Note: The PCID that will be used to process this request will be inferred from the user context, in this case,
        the external API bearer token stored in the authorization header.
        :param limit: paging query param, specifies the count limit of the returned devices
        :param offset: paging query param, specifies the offset of the returned devices
        :param filter_query: filtering query param, filters by specific fields with OData 4.0 query syntax (except tags)
        :param filter_tags: filtering query param, filters by tag-related fields with OData 4.0 query syntax
        :param sort: sorting query param, specifies the field name to sort against and the sort direction
        :param select: filtering query param, selects specific field names to display as returned result
        :param tuple_response: Boolean for tuple response (status code, response body) (Default: True)
        :param ignore_handle_response: Boolean to ignore response handling (Default: True)
        :return: collection of device detail of the claimed devices of the requested platform customer.
        Note: When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise, return
                Response json or response object if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        end_point = "/devices"
        url = f"{self.devices_url}{end_point}"
        log.info("Performing GET devices request to URL: {}".format(url))

        token_claims = NBAPIHelpers.get_jwt_unverified_claims(self.get_token())
        log.debug("----PROCESSED TOKEN---- {}".format(token_claims))
        pcid = token_claims["platform_customer_id"]
        log.info(f"Request PCID inferred from bearer token: {pcid}")

        qparam = {}
        if limit is not None:
            # If no limit query param value is specified with the request,
            # limit will be set to 2000 by default at the API contract level
            qparam["limit"] = limit
        if offset is not None:
            # If no offset query param value is specified with the request,
            # offset will be set to 0 by default at the API contract level
            qparam["offset"] = offset
        if filter_query:
            qparam["filter"] = filter_query
        if filter_tags:
            qparam["filter-tags"] = filter_tags
        if sort:
            qparam["sort"] = sort
        if select:
            qparam["select"] = select

        log.info("Request query params: {}".format(qparam))
        res = self.get(
            url=url,
            params=qparam,
            tuple_response=tuple_response,
            ignore_handle_response=ignore_handle_response,
        )
        log.debug(
            f"All properties from the Response object of the getDevices restAPI call: {vars(res)}"
        )
        if ignore_handle_response:
            NBAPIHelpers.print_req_response_info(res, log)
        return res

    def get_devices_with_api_token(
        self,
        api_token,
    ):
        """
        Get the device detail of the claimed devices of the platform customer account, with no query parameters,
        but with the supply of a custom bearer token.
        Note: The PCID that will be used to process this request will be inferred from the user context, in this case,
        the external API bearer token stored in the authorization header.
        :param api_token: the bearer token to be used along with the request
        :return: collection of device detail of the claimed devices of the requested platform customer.
        """
        end_point = "/devices"
        url = f"{self.devices_url}{end_point}"
        log.info("Performing GET devices request (custom token) to URL: {}".format(url))

        # Override existing bearer token for this particular request
        original_token = self.get_token()
        self.session.headers = {"Authorization": f"Bearer {api_token}"}
        log.info(
            f"Token decoding is not applicable with custom supplied token '{api_token}'."
        )

        res = self.get(url=url, ignore_handle_response=True)
        self.session.headers = {"Authorization": f"Bearer {original_token}"}
        log.debug(
            f"All properties from the Response object of the getStatus restAPI call: {vars(res)}"
        )
        NBAPIHelpers.print_req_response_info(res, log)
        return res

    def post_devices(
        self,
        devices,
        tuple_response=True,
        ignore_handle_response=True,
        wait_for_async_resource=False,
        polling_step_in_sec=1.0,
        timeout_in_sec=300,
        use_suggestion=False,
    ):
        """
        Batch claim of devices, with support for adding tags, locations, and contact information, through unique device
        identifiers. Devices can be of network, storage or compute type, with each type has different requirements of
        unique identifiers. Each type can be a collection of multiple devices.
        Note: The PCID that will be used to process this request will be inferred from the user context, in this case,
        the external API bearer token stored in the authorization header.
        This is an asynchronous API.
        :param devices: The request payload body in dict (please refer to the design docs for an example payload body)
        :param tuple_response: Boolean for tuple response (status code, response body) (Default: True)
        :param ignore_handle_response: Boolean to ignore response handling (Default: True) (Please note that if
        wait_for_async_resource is True, then this option has to be True)
        :param wait_for_async_resource: Boolean to wait for async operation resource response synchronously (Default:
        False) (Please note if this is set to be True, then ignore_handle_response will be set to be True)
        :param polling_step_in_sec: polling step in seconds between each get request for the async operation resource
        :param timeout_in_sec: duration of time to timeout in seconds before getting the async operation resource
        :param use_suggestion: Boolean to use the suggested polling step and timeout limit from the response to get the
        async operation resource (applied after the first get request)
        :return: return the asynchronous response if wait_for_async_resource is False (default), else return the async
        operation resource response synchronously (blocking call).
        Note: When wait_for_async_resource is True, ignore_handle_response cannot be False due to the attempt to
        retrieve the async operation resource from the location header of the async response.
        Note: When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise, return
                Response json or response object if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        if wait_for_async_resource and not ignore_handle_response:
            raise Exception(
                "Invalid arguments: if wait_for_async_resource is True then ignore_handle_response cannot be False"
            )

        end_point = "/devices"
        url = f"{self.devices_url}{end_point}"
        log.info("Performing POST devices request to URL: {}".format(url))
        log.info("POST request payload: {}".format(devices))

        token_claims = NBAPIHelpers.get_jwt_unverified_claims(self.get_token())
        log.debug("----PROCESSED TOKEN---- {}".format(token_claims))
        pcid = token_claims["platform_customer_id"]
        log.info(f"Request PCID inferred from bearer token: {pcid}")

        res = self.post(
            url=url,
            json=devices,
            tuple_response=tuple_response,
            ignore_handle_response=ignore_handle_response,
        )
        log.debug(
            f"All properties from the Response object of the postDevices restAPI call: {vars(res)}"
        )
        if ignore_handle_response:
            NBAPIHelpers.print_req_response_info(res, log)
        if wait_for_async_resource:
            if res.status_code is None or res.status_code != 202:
                raise Exception(
                    f"Received status '{res.status_code}' of the async response while attempting to "
                    f"retrieve the async resource identifier to get the async operation resource"
                )
            elif res.headers is None or res.headers.get("location", "None") == "None":
                raise Exception(
                    f"Failed to decode the headers of the async response or the value of the location "
                    f"header (if exists): headers={res.headers}"
                )
            else:
                location = str(res.headers.get("location", "None"))
                identifier = location.strip().split("/")[-1]
                if not identifier:
                    raise Exception(
                        f"Retrieved invalid async resource identifier '{identifier}' "
                        f"from the async response"
                    )
                log.info(
                    f"Start the GET request to get devices async operation resource with identifier: {identifier}"
                )
                res = self.get_devices_async_operation_resource(
                    identifier,
                    tuple_response,
                    polling_step_in_sec,
                    timeout_in_sec,
                    use_suggestion,
                )
        return res

    def get_devices_async_operation_resource(
        self,
        identifier,
        tuple_response=True,
        polling_step_in_sec=1.0,
        timeout_in_sec=300,
        use_suggestion=False,
    ):
        """
        Get the async operation resource of devices in a synchronous way by repeatedly attempting to retrieve the
        resource through get requests. The resource should be uniquely identifiable via an identifier from the
        location header of an async response.
        :param identifier: The identifier to uniquely identify the async operation resource of devices (Note: This
        should be retrieved from the location header of the async response)
        :param tuple_response: Boolean for tuple response (status code, response body) (Default: True) (Please note no
        ignore_handle_response with a value of True is allowed here due to recurrent GET requests based on responses)
        :param polling_step_in_sec: polling step in seconds between each get request for the async operation resource
        :param timeout_in_sec: duration of time to timeout in seconds before getting the async operation resource
        :param use_suggestion: Boolean to use the suggested polling step and timeout limit from the response to get the
        async operation resource (applied after the first get request)
        :return: return the response that contains the status and details of the requested async operation resource
        """
        end_point = "/devices/async-operations/"
        url = f"{self.devices_url}{end_point}{identifier}"
        log.info("Performing GET async operation resource request to URL: {}".format(url))

        start_at = time.time()
        curr_time = start_at
        timeout_at = start_at + timeout_in_sec
        ret_response = None
        suggestion_used = False
        while True:
            curr_time = time.time()
            if curr_time > timeout_at:
                log.info(
                    f"Retrieving async operation resource timed out at {time.ctime(curr_time)}"
                )
                break
            timeout_remaining = timeout_at - curr_time
            log.info(
                f"Retrieving async operation resource at {time.ctime(curr_time)}: started at {time.ctime(start_at)}, "
                f"timeout at {time.ctime(timeout_at)} in {timeout_remaining:.2f}/{timeout_in_sec:.2f} seconds with"
                f"{'' if use_suggestion and suggestion_used else ' no'} polling suggestion applied"
            )
            res = self.get(
                url=url,
                tuple_response=tuple_response,
            )

            if tuple_response:
                if res[0] != 200:
                    raise Exception(
                        f"Received status {res[0]} while attempting to retrieve async operation resource"
                    )
                elif type(res[1]) is not dict:
                    raise Exception(
                        f"Failed to decode the retrieved async operation resource with type {type(res[1])} instead "
                        f"of dict"
                    )
                if res[1]["status"] in ("INITIALIZED", "RUNNING", "PAUSED"):
                    if use_suggestion and not suggestion_used:
                        timeout_in_sec = res[1]["timeoutMinutes"] * 60
                        timeout_at = start_at + timeout_in_sec
                        polling_step_in_sec = res[1]["suggestedPollingIntervalSeconds"]
                        suggestion_used = True
                    time.sleep(polling_step_in_sec)
                    continue
                else:
                    ret_response = res
                    log.info(
                        f"Successfully retrieved async operation resource at {time.ctime(curr_time)}"
                    )
                    break
            else:
                if type(res) is not dict:
                    raise Exception(
                        f"Failed to decode the retrieved async operation resource with type {type(res)} instead of dict"
                    )
                if res["status"] in ("INITIALIZED", "RUNNING", "PAUSED"):
                    if use_suggestion and not suggestion_used:
                        timeout_in_sec = res["timeoutMinutes"] * 60
                        timeout_at = start_at + timeout_in_sec
                        polling_step_in_sec = res["suggestedPollingIntervalSeconds"]
                        suggestion_used = True
                    time.sleep(polling_step_in_sec)
                    continue
                else:
                    ret_response = res
                    log.info(
                        f"Successfully retrieved async operation resource at {time.ctime(curr_time)}"
                    )
                    break

        return ret_response

    def update_device(
        self,
        patch_payload,
        device_ids,
        tuple_response=True,
        ignore_handle_response=True,
        wait_for_async_resource=False,
        polling_step_in_sec=1.0,
        timeout_in_sec=300,
        use_suggestion=False,
    ):
        """
        Assign/Unassign Application Or Assign/Reassign/Unassign Subscription to the claimed devices.
        Devices can be of network or compute type, with each type has different requirements of
        unique identifiers. Each type can be a collection of multiple devices.
        Note: The PCID that will be used to process this request will be inferred from the user context, in this case,
        the external API bearer token stored in the authorization header.
        This is an asynchronous API.
        :param patch_payload :This request payload in dict(application payload or subscription payload)
        :param device_ids:This is list of claimed devices.
        :param tuple_response: Boolean for tuple response (status code, response body) (Default: True)
        :param ignore_handle_response: Boolean to ignore response handling (Default: True) (Please note that if
        wait_for_async_resource is True, then this option has to be True)
        :param wait_for_async_resource: Boolean to wait for async operation resource response synchronously (Default:
        False) (Please note if this is set to be True, then ignore_handle_response will be set to be True)
        :param polling_step_in_sec: polling step in seconds between each get request for the async operation resource
        :param timeout_in_sec: duration of time to timeout in seconds before getting the async operation resource
        :param use_suggestion: Boolean to use the suggested polling step and timeout limit from the response to get the
        async operation resource (applied after the first get request)
        :return: return the asynchronous response if wait_for_async_resource is False (default), else return the async
        operation resource response synchronously (blocking call).
        Note: When wait_for_async_resource is True, ignore_handle_response cannot be False due to the attempt to
        retrieve the async operation resource from the location header of the async response.
        Note: When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise, return
                Response json or response object if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        if wait_for_async_resource and not ignore_handle_response:
            raise Exception(
                "Invalid arguments: if wait_for_async_resource is True then ignore_handle_response cannot be False"
            )

        end_point = "/devices"
        url = f"{self.devices_url}{end_point}"
        log.info("Performing PATCH devices request to URL: {}".format(url))
        log.info("PATCH request payload: {}".format(patch_payload))

        token_claims = NBAPIHelpers.get_jwt_unverified_claims(self.get_token())
        log.debug("----PROCESSED TOKEN---- {}".format(token_claims))
        pcid = token_claims["platform_customer_id"]
        log.info(f"Request PCID inferred from bearer token: {pcid}")

        # joining all the claimed device ids to pass the ids as params
        id_suffix = "&id="
        ids = "id=" + id_suffix.join(device_ids)
        params = ids

        res = self.patch(
            url=url,
            params=params,
            json=patch_payload,
            tuple_response=tuple_response,
            ignore_handle_response=ignore_handle_response,
        )
        log.debug(
            f"All properties from the Response object of the postDevices restAPI call: {vars(res)}"
        )
        if ignore_handle_response:
            NBAPIHelpers.print_req_response_info(res, log)
        if wait_for_async_resource:
            if res.status_code is None or res.status_code != 202:
                raise Exception(
                    f"Received status '{res.status_code}' of the async response while attempting to "
                    f"retrieve the async resource identifier to get the async operation resource"
                )
            elif res.headers is None or res.headers.get("location", "None") == "None":
                raise Exception(
                    f"Failed to decode the headers of the async response or the value of the location "
                    f"header (if exists): headers={res.headers}"
                )
            else:
                location = str(res.headers.get("location", "None"))
                identifier = location.strip().split("/")[-1]
                if not identifier:
                    raise Exception(
                        f"Retrieved invalid async resource identifier '{identifier}' "
                        f"from the async response"
                    )
                log.info(
                    f"Start the GET request to get devices async operation resource with identifier: {identifier}"
                )
                res = self.get_devices_async_operation_resource(
                    identifier,
                    tuple_response,
                    polling_step_in_sec,
                    timeout_in_sec,
                    use_suggestion,
                )
        return res
