# pylint: disable=missing-docstring
import json

import httpretty
import pytest

from testsuite.oauth import authorization_code
from testsuite.oauth.authorize import none


RESPONSES = [
    ({
        'access_token': 'ACCESS_TOKEN',
    }, None, None),
    ({
        'access_token': 'ACCESS_TOKEN',
        'refresh_token': 'REFRESH_TOKEN',
    }, 'REFRESH_TOKEN', None),
    ({
        'access_token': 'ACCESS_TOKEN',
        'refresh_token': 'REFRESH_TOKEN',
        'patient': 'EXAMPLE_PATIENT_ID',
    }, 'REFRESH_TOKEN', 'EXAMPLE_PATIENT_ID'),
]


@pytest.mark.usefixtures('enable_httpretty')
@pytest.mark.parametrize('response, refresh_token, patient', RESPONSES)
def test_authorize(response, refresh_token, patient):
    """ Test Authorize endpoint with optional response params.
    """
    strategy = make_strategy()
    httpretty_token_request(response)

    strategy.authorize()

    assert strategy.access_token == 'ACCESS_TOKEN'
    assert strategy.refresh_token == refresh_token
    assert strategy.patient == patient


@pytest.mark.usefixtures('enable_httpretty')
def test_refresh_access_token():
    """ Test that we can refresh access tokens.
    """
    strategy = make_strategy()

    httpretty_token_request({
        'access_token': 'ACCESS_TOKEN',
        'refresh_token': 'REFRESH_TOKEN',
    })

    strategy.authorize()

    assert strategy.access_token == 'ACCESS_TOKEN'
    assert strategy.refresh_token == 'REFRESH_TOKEN'

    # Test that refresh_token does not get replaced with None
    httpretty_token_request({
        'access_token': 'ACCESS_TOKEN_2',
    })

    strategy.refresh_access_token()

    assert strategy.access_token == 'ACCESS_TOKEN_2'
    assert strategy.refresh_token == 'REFRESH_TOKEN'

    # Test that refresh_token can be updated
    httpretty_token_request({
        'access_token': 'ACCESS_TOKEN_3',
        'refresh_token': 'REFRESH_TOKEN_3',
    })

    strategy.refresh_access_token()

    assert strategy.access_token == 'ACCESS_TOKEN_3'
    assert strategy.refresh_token == 'REFRESH_TOKEN_3'


def make_strategy():
    """ Strategy factory object.
    """
    config = {
        'client_id': 'CLIENT_ID',
        'redirect_uri': 'http://example.com/redirect_uri',
    }
    urls = {
        'token': 'http://example.com/oauth/token',
        'authorize': 'http://example.com/oauth/authorize',
    }
    authorizer = none.NoneAuthorizer()

    return authorization_code.AuthorizationCodeStrategy(
        config,
        urls,
        authorizer,
    )


def httpretty_token_request(response):
    """ Registers an httpretty token endpoint with a given response.
    """
    httpretty.register_uri(httpretty.POST,
                           'http://example.com/oauth/token',
                           body=json.dumps(response),
                           status=200,
                           content_type='application/json')
