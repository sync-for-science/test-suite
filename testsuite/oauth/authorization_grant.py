""" Authorization Grant.

An authorization grant is a credential representing the resource
owner's authorization (to access its protected resources) used by the
client to obtain an access token.

@see: https://tools.ietf.org/html/rfc6749#section-1.3
"""
from abc import ABCMeta, abstractmethod


class AuthorizationGrant(metaclass=ABCMeta):
    """ Authorization Grant Interface.
    """

    @abstractmethod
    def authorize(self) -> None:
        """ Obtain an access token.

        Implement this method to request an access token.
        """

    @property
    @abstractmethod
    def access_token(self) -> str:
        """ Return the requested access token.
        """
