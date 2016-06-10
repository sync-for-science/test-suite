# pylint: disable=missing-docstring
import json

import httpretty
import pytest

from testsuite.oauth import client_credentials


@pytest.mark.usefixtures('enable_httpretty')
def test_authorize():

    strategy = client_credentials.ClientCredentialsStrategy(
        'CLIENT_ID',
        'CLIENT_SECRET',
        'http://example.com/oauth/token',
    )

    response = {
        'access_token': 'ACCESS_TOKEN',
        'refresh_token': 'REFRESH_TOKEN',
    }

    httpretty.register_uri(httpretty.POST,
                           'http://example.com/oauth/token',
                           body=json.dumps(response),
                           status=200,
                           content_type='application/json')

    strategy.authorize()

    assert strategy.access_token == 'ACCESS_TOKEN'
    assert strategy.refresh_token == 'REFRESH_TOKEN'

    response = {
        'access_token': 'ACCESS_TOKEN',
    }

    httpretty.register_uri(httpretty.POST,
                           'http://example.com/oauth/token',
                           body=json.dumps(response),
                           status=200,
                           content_type='application/json')

    strategy.authorize()

    assert strategy.access_token == 'ACCESS_TOKEN'
    assert strategy.refresh_token == 'REFRESH_TOKEN'
