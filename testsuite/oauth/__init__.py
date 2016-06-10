""" This is the oAuth module!
It provides oAuth strategies for connecting to secure FHIR APIs.
"""
import requests

from testsuite import fhir
from . import authorization_code, client_credentials, none


def authorization_code_factory(config):
    """ Build a AuthorizationCodeStrategy.

    Returns:
        authorization_code.AuthorizationCodeStrategy
    """
    auth_config = config['auth']
    auth_config['aud'] = config['api']['url']
    urls = fhir.get_oauth_uris(config['api']['url'])
    authorizer = config['authorizer'](config=auth_config,
                                      authorize_url=urls['authorize'])

    return authorization_code.AuthorizationCodeStrategy(
        auth_config,
        urls,
        authorizer
    )


def client_credentials_factory(config):
    """ Build a ClientCredentialsStrategy object from a config.

    Parameters
    ----------
    config : dict

    Returns
    -------
    testsuite.oauth.ClientCredentialsStrategy
    """
    return client_credentials.ClientCredentialsStrategy(
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
        return none.NoneStrategy()
    if strategy == 'authorization_code':
        return authorization_code_factory(config)
    if strategy == 'client_credentials':
        return client_credentials_factory(config)

    raise NotImplementedError(strategy)
