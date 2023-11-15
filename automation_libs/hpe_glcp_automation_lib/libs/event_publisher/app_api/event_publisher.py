"""
Event Publisher API Library
"""

import logging
import pprint
import re

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

LOG = logging.getLogger(__name__)


class EventPublisherAppAPI(AppSession):
    """
    Class definitions for Event Publisher App API
    """

    def __init__(self, host, sso_host, client_id, client_secret, scope):
        """
        Initialize Event publisher object for App API calls.

        :param host: MANDATORY
                host details for cluster to connect to.
        :param sso_host: MANDATORY
                sso_host details to validate client credentials against.
        :param client_id: MANDATORY
                client id details for app-instance client.
        :param client_secret: MANDATORY
                client secret details for app-instance client.
        :param scope: MANDATORY
                scope authroizations allowed for the client.

        :RETURNS APP session object to make app-api calls.
        """

        super(EventPublisherAppAPI, self).__init__(
            host, sso_host, client_id, client_secret, scope
        )
        # self.get_token()
        self.base_path = "/event-publisher/"
        self.api_version = "v1/"

    def _log_response(func):
        def decorated_func(*args, **kwargs):
            res = func(*args, **kwargs)
            LOG.debug(
                f"{' '.join(func.__name__.title().split('_'))} Response"
                + "\n\n"
                + pprint.pformat(res)
                + "\n"
            )
            return res

        return decorated_func

    def _get_path(self, path, secondary=None):
        """
        Internal Secondary call made if any API call was made with secondary=True as a parameter.

        Eg: To make an API call on the secondary region for getting event subscriptions on the app-instance.
            API call on secondary region:
            app_session.get_event_subscriptions(get_appinstance, secondary=True)
            API call on primary region:
            app_session.get_event_subscriptions(get_appinstance)
        """
        if secondary:
            mats = re.split("\\.", self.base_url)
            base_secondary_url = mats[0] + "-r." + ".".join(mats[1:])
            return f"{base_secondary_url}{self.base_path}{self.api_version}{path}"
        else:
            return f"{self.base_path}{self.api_version}{path}"

    @_log_response
    def get_status(self, ignore_handle_response=False):
        """
        Status API Call for Event Publisher
        """

        return self.get(
            self._get_path("status"), ignore_handle_response=ignore_handle_response
        )

    @_log_response
    def get_event_subscriptions(
        self, appinstance_id, secondary=None, ignore_handle_response=False, **params
    ):
        """
        App API Call to get event subscriptions configured on the app-instance.
        :param appinstance_id: MANDATORY
            Default: None
            Specified to get what event app-instance was subscribed to.
        :param secondary: OPTIONAL -
            Boolean (True or False)
            If Specified True runs the API call on the secondary region.
        :param ignore_handle_response: OPTIONAL -
            Boolen (True or False)
            Details specified based on the boolean flag in the return response.

        :RETURN returns JSON body with all the event subscriptions information if ignore_handle_response=False
                return JSON object with all the event subscriptions information if ignore_handle_response=True

        """

        return self.get(
            self._get_path(f"event-subscription/{appinstance_id}"),
            ignore_handle_response=ignore_handle_response,
        )

    @_log_response
    def post_event_subscriptions(
        self, appinstance_id, subscribed_events=[], ignore_handle_response=False
    ):
        """
        App API Call to post event subscriptions configured on the app-instance.
        :param appinstance_id: MANDATORY
            Default: None
            Specified to get what event app-instance was subscribed to.
        :param subscribed_events: MANDATORY -
            Should be a list of all the subscribed events that app-instance should recieve events from GLP.
        :param ignore_handle_response: OPTIONAL -
            Boolen (True or False)
            Details specified based on the boolean flag in the return response.

        :RETURN returns JSON body with all the event subscriptions information if ignore_handle_response=False
                return JSON object with all the event subscriptions information if ignore_handle_response=True

        """

        jsondata = {"subscriptions": subscribed_events}

        return self.post(
            self._get_path(f"event-subscription/{appinstance_id}"),
            json=jsondata,
            ignore_handle_response=ignore_handle_response,
        )

    @_log_response
    def put_event_subscriptions(
        self, appinstance_id, subscribed_events=[], ignore_handle_response=False
    ):
        """
        App API Call to post event subscriptions configured on the app-instance.
        :param appinstance_id: MANDATORY
            Default: None
            Specified to get what event app-instance was subscribed to.
        :param subscribed_events: MANDATORY -
            Should be a list of all the subscribed events that app-instance should recieve events from GLP.
        :param ignore_handle_response: OPTIONAL -
            Boolen (True or False)
            Details specified based on the boolean flag in the return response.

        :RETURN returns JSON body with all the event subscriptions information if ignore_handle_response=False
                return JSON object with all the event subscriptions information if ignore_handle_response=True

        """

        jsondata = {"subscriptions": subscribed_events}

        return self.put(
            self._get_path(f"event-subscription/{appinstance_id}"),
            json=jsondata,
            ignore_handle_response=ignore_handle_response,
        )

    @_log_response
    def delete_event_subscriptions(self, appinstance_id, ignore_handle_response=False):
        """
        App API Call to post event subscriptions configured on the app-instance.
        :param appinstance_id: MANDATORY
            Default: None
            Specified to get what event app-instance was subscribed to.
        :param subscribed_events: MANDATORY -
            Should be a list of all the subscribed events that app-instance should recieve events from GLP.
        :param ignore_handle_response: OPTIONAL -
            Boolen (True or False)
            Details specified based on the boolean flag in the return response.

        :RETURN returns JSON body with all the event subscriptions information if ignore_handle_response=False
                return JSON object with all the event subscriptions information if ignore_handle_response=True

        """

        return self.delete(
            self._get_path(f"event-subscription/{appinstance_id}"),
            ignore_handle_response=ignore_handle_response,
        )
