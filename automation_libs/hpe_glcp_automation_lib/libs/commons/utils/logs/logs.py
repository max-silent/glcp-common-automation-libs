import logging
import pprint

log = logging.getLogger(__name__)


class Logs:
    """
    class for all logs decorators
    """

    @staticmethod
    def log_response(func):
        def decorated_func(*args, **kwargs):
            log.debug(f"{' '.join(func.__name__.title().split('_'))} API Request")
            res = func(*args, **kwargs)
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response"
                + "\n\n"
                + pprint.pformat(res)
                + "\n"
            )
            return res

        return decorated_func
