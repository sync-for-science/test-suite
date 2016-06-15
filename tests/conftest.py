# pylint: disable=missing-docstring
import json

import pytest
import httpretty

from testsuite import fhir


@pytest.fixture
def enable_httpretty(request):
    """ Enables httpretty request intercepting for a single test.
    """
    httpretty.enable()
    request.addfinalizer(httpretty.disable)


@pytest.fixture
def success_oauth_uris(request):
    """ Defines a conformance statement with token and authorize uris.
    """
    response = {
        'rest': [{
            'security': {
                'extension': [{
                    'url': fhir.OAUTH_URIS_DEFINITION,
                    'extension': [
                        {
                            'url': 'token',
                            'valueUri': 'http://example.com/oauth/token',
                        },
                        {
                            'url': 'authorize',
                            'valueUri': 'http://example.com/oauth/authorize',
                        },
                    ],
                }],
            },
        }],
    }

    httpretty.register_uri(httpretty.GET,
                           'http://example.com/fhir/metadata',
                           body=json.dumps(response),
                           status=200,
                           content_type='application/json')
