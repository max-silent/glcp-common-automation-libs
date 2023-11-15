import logging
import random
import string

import urllib3

log = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RandomGenUtils:
    """Helper methods for generating random data."""

    @staticmethod
    def random_string_of_chars(length=7, lowercase=True, uppercase=False, digits=False):
        """Generate text string with specified length and set of ascii-characters.

        Args:
            length: int - length of string to be generated
            lowercase: bool - include lowercase into source of characters for generated string
            uppercase: bool - include uppercase into source of characters for generated string
            digits: bool - include digits into source of characters for generated string

        Returns:
            str - string of randomly generated characters with requested length and set of characters
        """

        if not any([lowercase, uppercase, digits]):
            raise ValueError(
                "At least one set of characters should be selected: lowercase, uppercase or digits"
            )
        charset = ""
        if lowercase:
            charset += string.ascii_lowercase
        if uppercase:
            charset += string.ascii_uppercase
        if digits:
            charset += string.digits
        return "".join(random.choices(charset, k=length))

    @staticmethod
    def generate_random_alphanumeric_string(length_of_random_string=7):
        """

        :rtype: string
        :type length_of_random_string: int
        """
        # using random.choices()
        # generating random strings
        random_string_suffix = "".join(
            random.choices(
                string.ascii_uppercase + string.digits, k=length_of_random_string
            )
        )
        # print result
        return random_string_suffix

    @staticmethod
    def generate_random_MAC_address(mac_prefix="00"):
        """

        :return: random MAC address starting with 24 bit mac_prefix specified
        :rtype: string
        """
        # Randomize the NIC bits for MAC
        local_mac_random = mac_prefix + ":%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        return local_mac_random.upper()

    @staticmethod
    def dev_config_modify(
        parent_part_number,
        parent_part_category,
        device_config_payload,
        extra_attribute=False,
    ):
        """
        Recursively modifies the variables of the OAAS template.

        This method modifies the provided 'device_config_payload' dictionary to set specific values for its keys.
        The modification is done recursively for any child devices present in the 'child_devices' key.


        :param: parent_part_number (str): The parent part number to set in the 'part_number' key of the 'device_config_payload'.
        :param: parent_part_category (str): The parent part category to set in the 'part_category' key of the 'device_config_payload'.
        :param: device_config_payload (dict): The dictionary representing the OAAS template of the device to be modified.
        :param: extra_attribute (bool, optional): If True and 'platform_category' exists in the current object,
                                              an 'extra_attributes' key is added with extra information.
                                              Default is False.

        :return: The modified 'device_config_payload' dictionary with updated values.

        Note:
            - The keys that will be modified in 'device_config_payload' are: 'obj_key', 'serial_number', 'part_number',
              'part_category', and 'eth_mac'.
            - If 'extra_attribute' is True and 'platform_category' exists in the current object, an 'extra_attributes'
              key is added with the name and value derived from the 'parent_part_number' and 'obj_key', respectively.
            - This method modifies the original 'device_config_payload' dictionary in place and does not create a new one.
        """

        device_config_payload["obj_key"] = device_config_payload[
            "serial_number"
        ] = f"ROOT{RandomGenUtils.generate_random_alphanumeric_string(12)}"
        device_config_payload["part_number"] = parent_part_number
        device_config_payload["part_category"] = parent_part_category
        device_config_payload["eth_mac"] = RandomGenUtils.generate_random_MAC_address()
        # Check if "extra_attribute" flag is set and "platform_category" exists in the current object
        if extra_attribute and "platform_category" in device_config_payload:
            # add "extra_attributes" before it
            device_config_payload["extra_attributes"] = [
                {"name": parent_part_number, "value": device_config_payload["obj_key"]}
            ]
        if "child_devices" in device_config_payload:
            children = device_config_payload["child_devices"]
            for child in children:
                RandomGenUtils.dev_config_modify(
                    parent_part_number, parent_part_category, child, extra_attribute
                )

        return device_config_payload

    @staticmethod
    def dev_config_negative(
        device_config_payload, same_eth_mac=None, same_serial_number=None
    ):
        """
        Recursively modifies the serial number and MAC address of the OAAS template.

        :param device_config_payload: The device configuration payload to modify.
        :param same_eth_mac: Optional MAC address to set for all devices.
        :param same_serial_number: Optional serial number to set for all devices.
        :return: Modified device configuration payload.`
        """
        # Generate a random serial number and set it as the "obj_key" and "serial_number" in the payload
        device_config_payload["obj_key"] = device_config_payload[
            "serial_number"
        ] = f"ROOT{RandomGenUtils.generate_random_alphanumeric_string(12)}"

        if same_eth_mac:
            # Set the provided MAC address for all devices
            device_config_payload["eth_mac"] = same_eth_mac
        else:
            # Generate a random MAC address and set it in the payload
            device_config_payload[
                "eth_mac"
            ] = RandomGenUtils.generate_random_MAC_address()

        if same_serial_number:
            # If provided, set the same serial number for all devices
            device_config_payload[
                "obj_key"
            ] = f"ROOT{RandomGenUtils.generate_random_alphanumeric_string(12)}"
            device_config_payload["serial_number"] = same_serial_number
        else:
            # Generate a random serial number if not provided
            device_config_payload["obj_key"] = device_config_payload[
                "serial_number"
            ] = f"ROOT{RandomGenUtils.generate_random_alphanumeric_string(12)}"

        if "child_devices" in device_config_payload:
            children = device_config_payload["child_devices"]
            for child in children:
                # Recursively call dev_config for each child device
                RandomGenUtils.dev_config_negative(
                    child, same_eth_mac, same_serial_number
                )

        return device_config_payload
