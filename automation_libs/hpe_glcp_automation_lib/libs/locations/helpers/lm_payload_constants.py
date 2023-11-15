import json
import logging

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class LMInputPayload:
    @staticmethod
    def create_location_payload():
        location_create_payload = {
            "name": "TESTING-LOCATION-",
            "description": "Creating location for ADI Fts",
            "type": "building",
            "addresses": [
                {
                    "country": "United States",
                    "street_address": "1680 America Dr",
                    "city": "San Jose",
                    "state": "CA",
                    "postal_code": "95134",
                    "type": "street",
                }
            ],
            "contacts": [
                {"type": "primary", "name": "你好", "email": "glcptestuser+002@outlook.com"}
            ],
        }

        return location_create_payload

    @staticmethod
    def create_location_event(
        location_name=None,
        city=None,
        state=None,
        country=None,
        postal_code=None,
        street_address=None,
        contact_name=None,
        email_id=None,
    ):
        """

        :param street_address:
        :param location_name:
        :param city:
        :param state:
        :param country:
        :param postal_code:
        :param contact_name:
        :param email_id:
        :return:
        """

        location_create_payload = LMInputPayload.create_location_payload()

        if city is None:
            city = "San Jose"

        if state is None:
            state = "CA"

        if country is None:
            country = "United States"

        if postal_code is None:
            postal_code = "95134"

        if location_name is None:
            location_name = (
                RandomGenUtils.random_string_of_chars(
                    length=5, lowercase=False, uppercase=True, digits=True
                )
                + " "
                + RandomGenUtils.random_string_of_chars(
                    length=5, lowercase=False, uppercase=True, digits=True
                )
            )

        if street_address is None:
            street_address = location_create_payload["addresses"][0][
                "street_address"
            ] + RandomGenUtils.random_string_of_chars(
                length=5, lowercase=False, uppercase=True, digits=True
            )

        location_create_payload["name"] = location_name
        location_create_payload["addresses"][0]["city"] = city
        location_create_payload["addresses"][0]["state"] = state
        location_create_payload["addresses"][0]["country"] = country
        location_create_payload["addresses"][0]["postal_code"] = postal_code
        location_create_payload["addresses"][0]["street_address"] = street_address
        location_create_payload["contacts"][0]["email"] = email_id
        location_create_payload["contacts"][0]["name"] = contact_name

        return location_create_payload

    @staticmethod
    def update_location_payload():
        location_update_payload = {
            "location_id": "8cd9ad69-a8e5-4529-97ea-804b2c88d2eb",
            "pc_id": "7b62a416571111eea2358e4730afc17f",
            "updated_location": {
                "id": "location7",
                "type": "building",
                "name": "loc-validation-3fdb",
            },
            "updated_address": [
                {
                    "id": "adcab465-dcdb-4c93-804c-2dae29cc16f6",
                    "location_id": "8cd9ad69-a8e5-4529-97ea-804b2c88d2eb",
                    "pgp_sym_encrypt": "United States",
                    "type": "street",
                    "pgp_sym_encrypt_2": "3333 Great America Drive",
                    "pgp_sym_encrypt_4": "San Jose",
                    "pgp_sym_encrypt_5": "CA",
                    "pgp_sym_encrypt_6": "94135",
                }
            ],
        }

        return location_update_payload

    @staticmethod
    def update_location_event(
        platform_customer_id=None,
        old_location_id=None,
        new_location_name=None,
        new_location_id=None,
        new_street_address="1 America Dr",
        new_county="Unites States",
        new_state="CA",
        new_city="San Jose",
    ):
        """

        :param new_street_address:
        :param platform_customer_id:
        :param old_location_id:
        :param new_location_name:
        :param new_location_id:
        :param new_county:
        :param new_state:
        :param new_city:
        :return:
        """

        location_update_payload = LMInputPayload.update_location_payload()

        if new_location_name is None:
            new_location_name = (
                RandomGenUtils.random_string_of_chars(
                    length=5, lowercase=False, uppercase=True, digits=True
                )
                + " "
                + RandomGenUtils.random_string_of_chars(
                    length=5, lowercase=False, uppercase=True, digits=True
                )
            )

        location_update_payload["location_id"] = old_location_id
        location_update_payload["pc_id"] = platform_customer_id
        location_update_payload["updated_location"]["name"] = new_location_name
        location_update_payload["updated_address"][0]["location_id"] = new_location_id
        location_update_payload["updated_address"][0][
            "pgp_sym_encrypt_2"
        ] = new_street_address
        location_update_payload["updated_address"][0]["pgp_sym_encrypt"] = new_county
        location_update_payload["updated_address"][0]["pgp_sym_encrypt_5"] = new_state
        location_update_payload["updated_address"][0]["pgp_sym_encrypt_4"] = new_city

        location_update_event = {
            "specversion": "1.0.0",
            "id": "1056afd0-11bc-4788-90a9-d92448b48308",
            "source": "CCS",
            "type": "LOCATION_EVENT",
            "topic": "ccs-internal",
            "time": "2023-01-01T10:10:10Z",
            "operation": "UPDATE",
            "data": json.dumps(location_update_payload),
        }

        return location_update_event

    @staticmethod
    def delete_location_payload():
        location_delete_payload = {
            "location_id": "8cd9ad69-a8e5-4529-97ea-804b2c88d2eb",
            "pc_id": "7b62a416571111eea2358e4730afc17f",
        }

        return location_delete_payload

    @staticmethod
    def delete_location_event(
        platform_customer_id=None,
        location_id=None,
    ):
        """

        :param platform_customer_id: Platform customer id
        :param location_id: Location id
        :return:
        """

        location_delete_payload = LMInputPayload.delete_location_payload()

        location_delete_payload["location_id"] = location_id
        location_delete_payload["pc_id"] = platform_customer_id

        location_delete_event = {
            "specversion": "1.0.0",
            "id": "1056afd0-11bc-4788-90a9-d92448b48308",
            "source": "CCS",
            "type": "LOCATION_EVENT",
            "topic": "ccs-internal",
            "time": "2023-01-01T10:10:10Z",
            "operation": "DELETE",
            "data": json.dumps(location_delete_payload),
        }

        return location_delete_event
