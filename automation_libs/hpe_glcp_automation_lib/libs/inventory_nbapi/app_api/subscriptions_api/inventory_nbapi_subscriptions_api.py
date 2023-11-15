"""
Inventory NBAPI Subscriptions APIs
TODO: Docs link pending
"""
import logging
import time

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession
from hpe_glcp_automation_lib.libs.inventory_nbapi.helpers.helpers import NBAPIHelpers

log = logging.getLogger()


class InventoryNBAPISubscriptions(AppSession):
    """
    Inventory NBAPI Unified Subscriptions API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        log.info("Initializing inventory_nbapi_subscriptions_api for api calls")
        self.base_url = host
        super(InventoryNBAPISubscriptions, self).__init__(
            host, sso_host, client_id, client_secret, scope=""
        )
        self.base_path = "/subscriptions"
        self.api_version = "/v1beta1"
        self.subscriptions_url = f"{self.base_url}{self.base_path}{self.api_version}"

    def post_subscriptions(
        self,
        subscriptions,
        tuple_response=True,
        ignore_handle_response=True,
        wait_for_async_resource=False,
        polling_step_in_sec=1.0,
        timeout_in_sec=300,
        use_suggestion=False,
    ):
        """
        Batch claim of subscriptions for a platform customer workspace. Each subscription is uniquely identified
        through a subscription key.
        Note: The PCID that will be used to process this request will be inferred from the user context, in this case,
        the external API bearer token stored in the authorization header.
        This is an asynchronous API.
        :param subscriptions: The request payload body in dict (please refer to the design docs for an example payload
        body)
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

        end_point = "/subscriptions"
        url = f"{self.subscriptions_url}{end_point}"
        log.info("Performing POST subscriptions request to URL: {}".format(url))
        log.info("POST request payload: {}".format(subscriptions))

        token_claims = NBAPIHelpers.get_jwt_unverified_claims(self.get_token())
        log.debug("----PROCESSED TOKEN---- {}".format(token_claims))
        pcid = token_claims["platform_customer_id"]
        log.info(f"Request PCID inferred from bearer token: {pcid}")

        res = self.post(
            url=url,
            json=subscriptions,
            tuple_response=tuple_response,
            ignore_handle_response=ignore_handle_response,
        )
        log.debug(
            f"All properties from the Response object of the postSubscriptions restAPI call: {vars(res)}"
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
                    f"Start the GET request to get subscriptions async operation resource with identifier: {identifier}"
                )
                res = self.get_subscriptions_async_operation_resource(
                    identifier,
                    tuple_response,
                    polling_step_in_sec,
                    timeout_in_sec,
                    use_suggestion,
                )
        return res

    def get_subscriptions_async_operation_resource(
        self,
        identifier,
        tuple_response=True,
        polling_step_in_sec=1.0,
        timeout_in_sec=300,
        use_suggestion=False,
    ):
        """
        Get the async operation resource of subscriptions in a synchronous way by repeatedly attempting to retrieve the
        resource through get requests. The resource should be uniquely identifiable via an identifier from the
        location header of an async response.
        :param identifier: The identifier to uniquely identify the async operation resource of subscriptions (Note: This
        should be retrieved from the location header of the async response)
        :param tuple_response: Boolean for tuple response (status code, response body) (Default: True) (Please note no
        ignore_handle_response with a value of True is allowed here due to recurrent GET requests based on responses)
        :param polling_step_in_sec: polling step in seconds between each get request for the async operation resource
        :param timeout_in_sec: duration of time to timeout in seconds before getting the async operation resource
        :param use_suggestion: Boolean to use the suggested polling step and timeout limit from the response to get the
        async operation resource (applied after the first get request)
        :return: return the response that contains the status and details of the requested async operation resource
        """
        end_point = "/subscriptions/async-operations/"
        url = f"{self.subscriptions_url}{end_point}{identifier}"
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
