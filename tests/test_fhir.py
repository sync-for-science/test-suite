# pylint: disable=missing-docstring
import pytest

from testsuite import fhir


@pytest.mark.usefixtures('enable_httpretty')
@pytest.mark.usefixtures('success_oauth_uris')
def test_get_oauth_uris():
    base_url = 'http://example.com/fhir/'
    conformance = fhir.get_conformance_statement(base_url)
    uris = fhir.get_oauth_uris(conformance)

    assert uris['token'] is not None
    assert uris['authorize'] is not None
