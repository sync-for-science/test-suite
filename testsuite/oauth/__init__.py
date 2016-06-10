""" This is the oAuth module!
It provides oAuth strategies for connecting to secure FHIR APIs.
"""
import requests

from testsuite import fhir
from .none import NoneStrategy
from .refresh_token import RefreshTokenStrategy
from .client_credentials import ClientCredentialsStrategy


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


def refresh_token_factory(config):
    """ Build a RefreshTokenStrategy object from a behave config.

    Parameters
    ----------
    config : dict

    Returns
    -------
    lib.oauth.RefreshTokenStrategy
    """
    auth_config = config['auth']
    auth_config['aud'] = config['api']['url']
    urls = fhir.get_oauth_uris(config['api']['url'])
    authorizer = config['authorizer'](config=auth_config,
                                      authorize_url=urls['authorize'])

    return RefreshTokenStrategy(auth_config, urls, authorizer)


def client_credentials_factory(config):
    """ Build a ClientCredentialsStrategy object from a config.

    Parameters
    ----------
    config : dict

    Returns
    -------
    testsuite.oauth.ClientCredentialsStrategy
    """
    return ClientCredentialsStrategy(
        client_id=config['auth']['client_id'],
        client_secret=config['auth']['client_secret'],
        token_url=config['auth']['token_url'],
    )


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
    strategy = config['auth'].get('strategy')

    if strategy == 'none':
        return NoneStrategy()
    if strategy == 'refresh_token':
        return refresh_token_factory(config)
    if strategy == 'client_credentials':
        return client_credentials_factory(config)

    raise NotImplementedError(strategy)
