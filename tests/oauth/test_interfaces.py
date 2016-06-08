# pylint: disable=missing-docstring,redefined-outer-name,unused-argument
import pytest

from testsuite import oauth
from testsuite.oauth.authorize import none


CONFIG = {
    'api': {
        'url': 'http://example.com/fhir/',
        'patient': 12345,
    },
    'auth': {
        'client_id': 'CLIENT ID',
        'client_secret': 'CLIENT_SECRET',
        'redirect_uri': 'http://example.com/redirect/',
        'refresh_token': 'REFRESH TOKEN',
        'token_url': 'http://example.com/oauth/token',
    },
    'authorizer': none.NoneAuthorizer,
    'host': 'http://example.com/',
}


@pytest.mark.usefixtures('success_oauth_uris')
@pytest.mark.parametrize('config, factory', [
    (CONFIG, oauth.refresh_token_factory),
    (CONFIG, oauth.client_credentials_factory),
])
def test_implements_interface(config, factory):
    strategy = factory(config)

    assert strategy.exchange_authorization_grant
    assert strategy.request_offline_access
    assert strategy.refresh_access_token
    assert strategy.authorization
