""" This is the oAuth module!
It provides oAuth strategies for connecting to secure FHIR APIs.
"""
import requests

from testsuite import fhir
from . import authorization_code, client_credentials, none
from .authorize.base import Authorizer

def authorization_code_factory(config):
    """ Build a AuthorizationCodeStrategy.

    Returns:
        authorization_code.AuthorizationCodeStrategy
    """
    auth_config = config['auth']
    auth_config['aud'] = config['api']['url']
    conformance = fhir.get_conformance_statement(config['api']['url'])
    urls = fhir.get_oauth_uris(conformance)
    authorizer_class = Authorizer if 'authorizer' not in config \
                                  else config['authorizer']
    authorizer = authorizer_class(config=auth_config,
            authorize_url=urls['authorize'])

    return authorization_code.AuthorizationCodeStrategy(
        auth_config,
        urls,
        authorizer
    )


def client_credentials_factory(config):
    """ Build a ClientCredentialsStrategy object from a config.

    Returns:
        client_credentials.ClientCredentialsStrategy
    """
    return client_credentials.ClientCredentialsStrategy(
        client_id=config['auth']['client_id'],
        client_secret=config['auth']['client_secret'],
        token_url=config['auth']['token_url'],
    )


def factory(config):
    """ Build an oAuth Strategy.

    Args:
        config (dict): A vendor's config.

    Returns:
        authorization_grant.AuthorizationGrant
    """
    strategy = config['auth'].get('strategy')

    if strategy == 'none':
        return none.NoneStrategy()
    if strategy == 'authorization_code':
        return authorization_code_factory(config)
    if strategy == 'client_credentials':
        return client_credentials_factory(config)

    raise NotImplementedError(strategy)
