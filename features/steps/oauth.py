# pylint: disable=missing-docstring,function-redefined
import uuid

from behave import given, when
import requests

from testsuite import fhir


ERROR_AUTHORIZATION_FAILED = 'Authorization failed.'
ERROR_BAD_CONFORMANCE = 'Could not parse conformance statement.'
ERROR_OAUTH_DISABLED = 'OAuth is not enabled on this server.'


@given('OAuth is enabled')
def step_impl(context):
    assert context.vendor_config['auth']['strategy'] != 'none', \
        ERROR_OAUTH_DISABLED

    if context.conformance is None:
        assert False, ERROR_BAD_CONFORMANCE

    fhir.get_oauth_uris(context.conformance)


@given('I am logged in')
def step_impl(context):
    assert context.oauth is not None, ERROR_AUTHORIZATION_FAILED
    assert context.oauth.access_token is not None, \
        ERROR_AUTHORIZATION_FAILED


@given('I am not logged in')
def step_impl(context):
    context.oauth = None


@when('I ask for authorization without the {field_name} field')
def step_impl(context, field_name):
    """ TODO: reduce duplication.
    """
    fields = {
        'response_type': 'code',
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
        'scope': context.vendor_config['auth']['scope'],
        'state': uuid.uuid4(),
    }

    del fields[field_name]

    uris = fhir.get_oauth_uris(context.conformance)

    response = requests.get(uris['authorize'],
                            params=fields,
                            allow_redirects=False,
                            timeout=5)

    context.response = response


@when('I ask for a new access token')
def step_impl(context):
    """ TODO: reduce duplication.
    """
    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.oauth.refresh_token,
        'scope': context.vendor_config['auth']['scope'],
    }

    auth = requests.auth.HTTPBasicAuth(context.vendor_config['auth']['client_id'],
                                       context.vendor_config['auth']['client_secret'])

    uris = fhir.get_oauth_uris(context.conformance)

    response = requests.post(uris['token'],
                             data=fields,
                             allow_redirects=False,
                             auth=auth,
                             timeout=5)

    context.response = response


@when('I ask for a new access token without the {field_name} field')
def step_impl(context, field_name):
    """ TODO: reduce duplication.
    """
    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.oauth.refresh_token,
        'scope': context.vendor_config['auth']['scope'],
    }

    auth = requests.auth.HTTPBasicAuth(context.vendor_config['auth']['client_id'],
                                       context.vendor_config['auth']['client_secret'])

    if field_name == 'client_id':
        auth = None
    else:
        del fields[field_name]

    uris = fhir.get_oauth_uris(context.conformance)

    response = requests.post(uris['token'],
                             data=fields,
                             allow_redirects=False,
                             auth=auth,
                             timeout=5)

    context.response = response
