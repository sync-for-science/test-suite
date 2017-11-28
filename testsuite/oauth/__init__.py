""" This is the oAuth module!
It provides oAuth strategies for connecting to secure FHIR APIs.
"""
import requests

from testsuite import fhir
from . import authorization_code, authorize, client_credentials, none


def authorization_code_factory(config):
    """ Build a AuthorizationCodeStrategy.

    Returns:
        authorization_code.AuthorizationCodeStrategy
    """
    auth_config = config['versioned_auth']
    conformance = fhir.get_conformance_statement(config['versioned_api']['url'])
    urls = fhir.get_oauth_uris(conformance)
    authorizer = authorize.Authorizer(config=auth_config,
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
        client_id=config['versioned_auth']['client_id'],
        client_secret=config['versioned_auth']['client_secret'],
        token_url=config['versioned_auth']['token_url'],
    )


def factory(config):
    """ Build an oAuth Strategy.

    Args:
        config (dict): A vendor's config.

    Returns:
        authorization_grant.AuthorizationGrant
    """

    strategy = config['versioned_auth'].get('strategy')

    if strategy == 'none':
        return none.NoneStrategy()
    if strategy == 'authorization_code':
        return authorization_code_factory(config)
    if strategy == 'client_credentials':
        return client_credentials_factory(config)

    raise NotImplementedError(strategy)
