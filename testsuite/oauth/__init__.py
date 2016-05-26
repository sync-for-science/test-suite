""" This is the oAuth module!
It provides oAuth strategies for connecting to secure FHIR APIs.
"""
import requests

from testsuite import fhir
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

    def refresh_access_token(self):
        """ Request a new access token. """
        raise NotImplementedError

    def authorization(self):
        """ Get an Authorization header value. """
        raise NotImplementedError


def smart_factory(config):
    """ Build a Smart object from a config dict.

    Parameters
    ----------
    config : dict

    Returns
    -------
    lib.oauth.SmartStrategy
    """
    urls = fhir.get_oauth_uris(config['api']['url'])
    auth = requests.auth.HTTPBasicAuth(config['auth']['client_id'],
                                       config['auth']['client_secret'])

    return SmartStrategy(client_id=config['auth']['client_id'],
                         username=config['auth'].get('username', None),
                         password=config['auth'].get('password', None),
                         urls=urls,
                         auth=auth)


def refresh_token_factory(config):
    """ Build a RefreshTokenStrategy object from a behave config.

    Parameters
    ----------
    config : dict

    Returns
    -------
    lib.oauth.RefreshTokenStrategy
    """
    urls = fhir.get_oauth_uris(config['api']['url'])

    return RefreshTokenStrategy(client_id=config['auth']['client_id'],
                                client_secret=config['auth']['client_secret'],
                                redirect_uri=config['auth']['redirect_uri'],
                                urls=urls,
                                refresh_token=config['auth']['refresh_token'],
                                confidential_client=config['auth'].get('confidential_client', False))


def factory(context):
    """ Build an oAuth Strategy from a behave context.

    Parameters
    ----------
    context : behave.runner.Context

    Returns
    -------
    lib.oauth.Strategy implementation
    """
    config = context.config
    strategy = config['auth'].get('strategy', 'smart')

    if strategy == 'smart':
        return smart_factory(config)
    if strategy == 'none':
        return NoneStrategy()
    if strategy == 'refresh_token':
        return refresh_token_factory(config)

    raise NotImplementedError(strategy)
