"""
Session Exceptions
"""


class SessionException(Exception):
    """
    Session Exception Class
    """

    def __init__(self, exc_str, response=None):
        super(SessionException, self).__init__(exc_str)
        self.response = response


class LoginFailedException(Exception):
    """
    Login Failed Exception Class
    """


class MFASecretKeyFailedException(Exception):
    """
    MFA Secret Device ID Exception Class
    """


class TokenRefreshException(Exception):
    """
    Token Refresh Failed Exception Class
    """


class LoadAccountFailedException(Exception):
    """
    Load Account Failed Exception Class
    """
