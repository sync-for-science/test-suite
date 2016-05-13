""" This is the oAuth module!
It provides oAuth strategies for connecting to secure FHIR APIs.
"""
from .smart import SmartStrategy
from .none import NoneStrategy
from .refresh_token import RefreshTokenStrategy


class Strategy(object):
    """ oAuth Strategy interface. """
    access_token = None
    refresh_token = None

    def request_offline_access(self):
        """ Request a refresh token. """
        raise NotImplementedError

    def revoke_access_token(self):
        """ Request that the oAuth server revoke stored access token. """
        raise NotImplementedError

    def refresh_access_token(self):
        """ Request a new access token. """
        raise NotImplementedError

    def authorization(self):
        """ Get an Authorization header value. """
        raise NotImplementedError


def smart_factory(context):
    """ Build a Smart object from a behave context.

    Parameters
    ----------
    context : behave.runner.Context

    Returns
    -------
    lib.oauth.SmartStrategy
    """
    import requests
    from testsuite import fhir

    urls = fhir.get_oauth_uris(context.api_url)
    auth = requests.auth.HTTPBasicAuth(context.auth['client_id'],
                                       context.auth['client_secret'])

    return SmartStrategy(client_id=context.auth['client_id'],
                         username=context.auth.get('username', None),
                         password=context.auth.get('password', None),
                         urls=urls,
                         auth=auth)


def refresh_token_factory(context):
    """ Build a RefreshTokenStrategy object from a behave context.

    Parameters
    ----------
    context : behave.runner.Context

    Returns
    -------
    lib.oauth.RefreshTokenStrategy
    """
    from testsuite import fhir

    urls = fhir.get_oauth_uris(context.api_url)

    return RefreshTokenStrategy(client_id=context.auth['client_id'],
                                client_secret=context.auth['client_secret'],
                                urls=urls,
                                refresh_token=context.auth['refresh_token'])


def factory(context):
    """ Build an oAuth Strategy from a behave context.

    Parameters
    ----------
    context : behave.runner.Context

    Returns
    -------
    lib.oauth.Strategy implementation
    """
    strategy = context.auth.get('strategy', 'smart')

    if strategy == 'smart':
        return smart_factory(context)
    if strategy == 'none':
        return NoneStrategy()
    if strategy == 'refresh_token':
        return refresh_token_factory(context)
