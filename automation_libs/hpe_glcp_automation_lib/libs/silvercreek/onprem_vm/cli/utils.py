import logging

import pexpect
import yaml
from yaml.loader import SafeLoader

logger = logging.getLogger(__name__)


def get_vmconfig_params(abs_path_to_config_file):
    """
    Function to get the VM Configuration Parameters from onprem_vm_config.yaml file
    :param abs_path_to_config_file(string): Absolute path to config file
    :return: vm config params in a dictionary
    """
    with open(abs_path_to_config_file) as fd:
        vm_config_data = yaml.load(fd, Loader=SafeLoader)
        logger.info(">> Loading testconfig data is successful")
        logger.debug(">>> Test config data: {}".format(vm_config_data))
        return vm_config_data


def close_if_alive(child):
    """Checks if child process is alive and close the ssh connection"""
    if child.isalive:
        logger.info(">> Closing the SSH connetion!")
        child.close()
    else:
        logger.info(">> SSH Connection is not alive!")


def match_str_child_obj(child, expect_str, error=None):
    """This function will expect/match a string in child obj, Throw an error if str
    is not found.
    """
    index = child.expect([pexpect.TIMEOUT, expect_str], timeout=180)
    if index == 1:
        logger.info("Expected string - {} is found in the CLI".format(expect_str))
    else:
        if error is not None:
            assert False, error
        else:
            assert (
                False
            ), "Expected string - {} is not found in CLI\n\nCLI Output:\n{}".format(
                expect_str, child.before
            )


def assert_equal(param1, param2, err_msg):
    """
    Return assertion error if two objects are unequal.
    :param param1: first object to be compared
    :param param2: second object to be compared
    :err_msg: message to be displayed on failure
    """
    assert param1 == param2, "Assert Failed. {} is not equal to {}. {}".format(
        param1, param2, err_msg
    )


def assert_not_equal(param1, param2, err_msg):
    """
    Return assertion error if two objects are equal.
    :param param1: first object to be compared
    :param param2: second object to be compared
    :err_msg: message to be displayed on failure
    """
    assert param1 != param2, "Assert Failed. {} is equal to {}. {}".format(
        param1, param2, err_msg
    )


def assert_lessthan(param1, param2, err_msg):
    """
    Return assertion error if object1 is not less than object2
    :param param1: first object to be compared
    :param param2: second object to be compared
    :err_msg: message to be displayed on failure
    """
    assert param1 < param2, "Assert Failed. {} is not lesser than {}. {}".format(
        param1, param2, err_msg
    )


def assert_greaterthan(param1, param2, err_msg):
    """
    Return assertion error if object1 is not greater than object2
    :param param1: first object to be compared
    :param param2: second object to be compared
    :err_msg: message to be displayed on failure
    """
    assert param1 > param2, "Assert Failed. {} is not greater than {}. {}".format(
        param1, param2, err_msg
    )


def assert_condition(cond, err_msg):
    """
    Return assertion error if condition fails
    :param param1: condition to be checked
    :err_msg: message to be displayed on failure
    """
    assert cond, "Condition: {} Failed. {}".format(cond, err_msg)
