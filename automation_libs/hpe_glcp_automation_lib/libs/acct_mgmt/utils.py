import asyncio
import inspect
import logging
import os
import pprint
import random
import string
import time
from typing import Any, Union

import requests

log = logging.getLogger(__name__)


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


def log_api_response(func):
    def decorated_func(*args, **kwargs):
        res = func(*args, **kwargs)
        try:
            body = f"Response body: {pprint.pformat(res.json())}"
        except:
            body = f"Response body: {res.text}"

        log.debug(
            f"{' '.join(func.__name__.title().split('_'))} Response"
            + "\n\n"
            + pprint.pformat(res)
            + body
            + "\n"
        )
        return res

    return decorated_func


def get_function_name() -> str:
    """
    Return the name of the function that calling this method.

    Example: The below code will print "func_a":

      def func_a():
        print(get_function_name())
    """
    frameinfo = inspect.getouterframes(inspect.currentframe())[1]
    return frameinfo.frame.f_code.co_name


def get_function_caller() -> str:
    """
    Return the name of the function that called the function calling this method

    Example: The below code will print "func_b":

      def func_b():
        func_a():

      def func_a():
        print(get_function_caller())
    """
    frameinfo = inspect.getouterframes(inspect.currentframe())[2]
    return frameinfo.frame.f_code.co_name


def get_real_path(relative_path: str) -> str:
    """
    Returns the real path for the path relative to file that called this method.

    Args:
        relative_path (str): Path relative to the file (../testsetup/something.json)

    Returns:
        str: The real path
    """
    frameinfo = inspect.getouterframes(inspect.currentframe())[1]
    return os.path.join(os.path.dirname(frameinfo.filename), relative_path)


def check_type(obj: object, cls_or_tuple: Union[type, tuple]):
    """
    Checks that the object is of the specified type and thows an exception if not

    Args:
        obj (Any): Object to check
        cls_or_tuple (type | Tuple): Possible types

    Raises:
        TypeError: If the object is not of the specified type
    """
    if not isinstance(obj, cls_or_tuple):
        raise TypeError(f"Object type {type(obj)} != expected {cls_or_tuple}")

    return True


def verify_response_type(response: Any) -> requests.Response:
    """
    Verify that the value is of type response, raise exception if not.
    If the value is of type response, return it back unchanged.

    Args:
        response (Any): Response object to be verified.

    Raises:
        TypeError: If not of type requests.Response

    Returns:
        requests.Response: Returns the response object (unchanged)
    """
    if not isinstance(response, requests.Response):
        raise TypeError(
            f"Response type ({type(response)}) != {requests.Response.__name__}"
        )

    return response


def random_string(length: int, charset: str = string.ascii_letters) -> str:
    """
    Creates a random string of the specified length

    Args:
        length (int): Length of the string
        charset (str): Characters to use.

    Returns:
        str: The randomly generated string
    """
    return "".join(random.choices(charset, k=length))


def random_hexstring(length: int) -> str:
    """
    Creates a random hexidecimal string of the specified length

    Args:
        length (int): Length of the string

    Returns:
        str: The randomly generated string
    """
    return random_string(length=length, charset=string.hexdigits)


def timer(duration_s: float, poll_s: float = 1.0):
    """
    Timer that can be used in a for-loop
    The method will yield the time left before each iteration's wait period (poll_s)

    Examples:

        # Do something every second for 4 seconds
        for time_left in timer(4):
            log.info(f"do something - time left: {time_left}")

        # Do something every half second for 4 seconds
        for _ in timer(4, 0.5):
            log.info("do something")

    Args:
        duration_s (float): The duration in seconds
        poll_s (float, optional): Duration to wait in each iterationin seconds. Defaults to 1.0.

    Yields:
        float: Time remaining
    """
    log.debug(f"Staring a timer for {duration_s}s (polling period: {poll_s}s)")
    assert (
        duration_s > poll_s
    ), f"Duration ({duration_s}s) must be greater than polling period ({poll_s}s)"

    end_time = time.time() + duration_s
    remaining_time = max([end_time - time.time(), 0])

    while remaining_time > 0:
        remaining_time = max([end_time - time.time(), 0])
        yield remaining_time

        # If the remaining time is less than the polling period,
        # only delay for the remaining time.
        poll_s = min([poll_s, remaining_time])
        time.sleep(poll_s)


async def async_timer(duration_s: float, poll_s: float = 1.0):
    """
    Async timer that can be used in a for-loop wiht asyncio
    The method will yield the time left

    Examples:

        # Do something every second for 4 seconds
        for time_left in timer(4):
            log.info(f"do something - time left: {time_left}")

        # Do something every half second for 4 seconds
        for _ in timer(4, 0.5):
            log.info("do something")

    Args:
        duration_s (float): The duration in seconds
        poll_s (float, optional): Polling period in seconds. Defaults to 1.0.

    Yields:
        float: Time remaining
    """
    end_time = time.time() + duration_s
    remaining_time: float = max([end_time - time.time(), 0])

    while remaining_time > 0:
        remaining_time = max([end_time - time.time(), 0])
        yield remaining_time
        await asyncio.sleep(poll_s)
