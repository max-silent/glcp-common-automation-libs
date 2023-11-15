import logging
from pprint import pformat

from jose import jwt

log = logging.getLogger()


class NBAPIHelpers:
    @staticmethod
    def print_req_response_info(response, origin_logger=log):
        print_dict = {}
        print_dict["Response headers information"] = response.headers
        print_dict["Request method"] = response.request
        print_dict["Url"] = response.url
        print_dict["Elapsed"] = response.elapsed
        print_dict["Status Code"] = response.status_code
        print_dict["Reason"] = response.reason
        print_dict["Content"] = response.text
        content_len = len(response.content)

        origin_logger.info("---Printing request response info---")
        origin_logger.info(f"Response content length -- {content_len}")
        origin_logger.info("%s", pformat(print_dict, indent=2))

    @staticmethod
    def get_jwt_unverified_claims(token: str):
        if not token:
            raise Exception("Token is none or empty")
        claims = jwt.get_unverified_claims(token)
        log.info("JWT TOKEN CLAIMS DECODED: {}".format(claims))
        returned_claims = {}
        returned_claims["client_id"] = claims.get("client_id", "None")
        returned_claims["iss"] = claims.get("iss", "None")
        returned_claims["aud"] = claims.get("aud", "None")
        returned_claims["sub"] = claims.get("sub", "None")
        returned_claims["user_ctx"] = claims.get("user_ctx", "None")
        returned_claims["platform_customer_id"] = claims.get(
            "platform_customer_id", "None"
        )
        return returned_claims
