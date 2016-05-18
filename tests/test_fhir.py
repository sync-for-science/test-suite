# pylint: disable=missing-docstring
from testsuite import fhir


def test_get_oauth_uris(success_oauth_uris):
    base_url = 'http://example.com/fhir/'
    uris = fhir.get_oauth_uris(base_url)

    assert uris['token'] is not None
    assert uris['authorize'] is not None
