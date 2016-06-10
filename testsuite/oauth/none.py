""" No-op authorization.
"""
from . import authorization_grant


class NoneStrategy(authorization_grant.AuthorizationGrant):
    """ NoneStrategy.

    Does nothing.
    """
    access_token = ''

    def authorize(self):
        """ Authorize.
        """
