"""
UI API Library
"""
import logging
import pprint
import re

import requests

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

LOG = logging.getLogger(__name__)


class Geo(UISession):
    """
    Geo Session class
    """

    def __init__(self, host, user, password, pcid):
        """
        Constructor for the class
            Parameters:
                host (str): CCS UI Hostname
                user (str): Login Credentials - Username
                password (str): Login Credentials - Password
                pcid (str): Platform Customer ID

        """
        LOG.info("Initializing geo for user api calls")
        super(Geo, self).__init__(host, user, password, pcid)
        self.base_path = "/geo/ui/"
        self.api_version = "v1/"

    def _get_path(self, path, secondary=None):
        if secondary:
            mats = re.split("\.", self.base_url)
            base_secondary_url = mats[0] + "-r." + ".".join(mats[1:])
            return f"{base_secondary_url}{self.base_path}{self.api_version}{path}"
        else:
            return f"{self.base_path}{self.api_version}{path}"

    def _log_response(func):
        def decorated_func(*args, **kwargs):
            LOG.debug(f"{' '.join(func.__name__.title().split('_'))} API Request")
            res = func(*args, **kwargs)
            LOG.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response"
                + "\n\n"
                + pprint.pformat(res)
                + "\n"
            )
            return res

        return decorated_func

    @_log_response
    def get_status(self):
        """
        Get status of the Geo service UI API

            Returns:
                   JSON object of the status
        """
        return self.get(self._get_path("status"))

    @_log_response
    def get_countries(self, code="", secondary=None, auth=True, **params):
        """
        Get API call to get countries
            Parameters:
                    code (str): Country code
                    secondary (bool): flag to use secondary cluster eg mira-r
                    auth (bool): flag if set to True, gives all countries
                    params (arr):
                        status : Status value like AVAILABLE etc
                        country_group_code : Country Group code
                        offset : Pagination offset
                        limit : Page length
            Returns:
                   JSON body containing countries
        """
        if code:
            return self.get(self._get_path(f"countries/{code}", secondary=secondary))
        else:
            if auth:
                return self.get(
                    self._get_path("countries", secondary=secondary), params=params
                )
            else:
                r = requests.get(
                    f"{self.base_url}{self._get_path('countries')}", allow_redirects=False
                )
                print(f"{self.base_url}{self._get_path('countries')}")
                if r.status_code != 200:
                    raise Exception("Cannot invoke API without auth token")
                return r.json()

    @_log_response
    def get_country_groups(self, code="", secondary=None, **params):
        """
        Get API call to get country groups
            Parameters:
                    code (str): Country code
                    secondary (bool): flag to use secondary cluster eg mira-r
                    params (arr): Keyword argument of the following:
                        offset : Pagination offset
                        limit : Page length
            Returns:
                   JSON body containing country groups
        """
        if code:
            return self.get(self._get_path(f"country-groups/{code}", secondary=secondary))
        else:
            return self.get(
                self._get_path(f"country-groups", secondary=secondary), params=params
            )

    @_log_response
    def get_regions(self, code="", secondary=None, **params):
        """
        Get API call to get regions
            Parameters:
                    code (str): Country code
                    secondary (bool): flag to use secondary cluster eg mira-r
                    params (arr): Keyword argument of the following:
                        offset : Pagination offset
                        limit : Page length
            Returns:
                   JSON body containing regions
        """
        if code:
            return self.get(self._get_path(f"regions/{code}", secondary=secondary))
        else:
            return self.get(
                self._get_path(f"regions", secondary=secondary), params=params
            )

    @_log_response
    def get_languages(self, code="", secondary=None, **params):
        """
        Get API call to get languages
            Parameters:
                    code (str): Language code
                    secondary (bool): flag to use secondary cluster eg mira-r
                    params (arr): Keyword argument of the following:
                        offset : Pagination offset
                        limit : Page length
            Returns:
                   JSON body containing languages
        """
        if code:
            return self.get(self._get_path(f"languages/{code}", secondary=secondary))
        else:
            return self.get(
                self._get_path(f"languages", secondary=secondary), params=params
            )

    @_log_response
    def get_timezones(self, secondary=None, **params):
        """
        Get API call to get timezones
            Parameters:
                    secondary (bool): flag to use secondary cluster eg mira-r
                    params (arr): Keyword argument of the following:
                        offset : Pagination offset
                        limit : Page length
            Returns:
                   JSON body containing timezones
        """
        return self.get(self._get_path(f"timezones", secondary=secondary), params=params)

    @_log_response
    def get_cloud_info_region_map(self, secondary=None, **params):
        """
        Get API call to get cloud info region map
            Parameters:
                    secondary (bool): flag to use secondary cluster eg mira-r
                    params (arr): Keyword argument of the following:
                        offset : Pagination offset
                        limit : Page length
                        provider : Cloud Provider
                        region : Region code
            Returns:
                   JSON body containing cloud info region map
        """
        return self.get(
            self._get_path(f"cloud-regions", secondary=secondary), params=params
        )
