# pylint: disable=missing-docstring,function-redefined
import uuid

from behave import given, when
import requests

from features.steps import utils
from testsuite.oauth import factory
from testsuite import fhir


ERROR_AUTHORIZATION_FAILED = 'Authorization failed.'
ERROR_BAD_CONFORMANCE = 'Could not parse conformance statement.'


@given('I am logged in')
def step_impl(context):
    context.oauth = factory(context)

    try:
        context.oauth.request_offline_access()
        context.authorization = context.oauth.authorization()
    except AssertionError as error:
        assert False, utils.bad_response_assert(error.args[0],
                                                ERROR_AUTHORIZATION_FAILED)

    context.config['auth']['refresh_token'] = context.oauth.refresh_token


@given('I am not logged in')
def step_impl(context):
    context.authorization = None


@when('I refresh my access token')
def step_impl(context):
    context.oauth.refresh_access_token()
    context.authorization = context.oauth.authorization()

    context.config['auth']['refresh_token'] = context.oauth.refresh_token


@when('I ask for authorization without the {field_name} field')
def step_impl(context, field_name):
    """ TODO: reduce duplication.
    """
    fields = {
        'response_type': 'code',
        'client_id': context.config['auth']['client_id'],
        'redirect_uri': context.config['auth']['redirect_uri'],
        'scope': 'launch/patient patient/Patient.read',
        'state': uuid.uuid4(),
    }

    del fields[field_name]

    try:
        uris = fhir.get_oauth_uris(context.config['api']['url'])
    except ValueError as error:
        assert False, utils.bad_response_assert(error.response,
                                                ERROR_BAD_CONFORMANCE)

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
        'scope': 'launch/patient patient/Patient.read',
    }

    auth = requests.auth.HTTPBasicAuth(context.config['auth']['client_id'],
                                       context.config['auth']['client_secret'])

    try:
        uris = fhir.get_oauth_uris(context.config['api']['url'])
    except ValueError as error:
        assert False, utils.bad_response_assert(error.response,
                                                ERROR_BAD_CONFORMANCE)

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
        'scope': 'launch/patient patient/Patient.read',
    }

    auth = requests.auth.HTTPBasicAuth(context.config['auth']['client_id'],
                                       context.config['auth']['client_secret'])

    if field_name == 'client_id':
        auth = None
    else:
        del fields[field_name]

    try:
        uris = fhir.get_oauth_uris(context.config['api']['url'])
    except ValueError as error:
        assert False, utils.bad_response_assert(error.response,
                                                ERROR_BAD_CONFORMANCE)

    response = requests.post(uris['token'],
                             data=fields,
                             allow_redirects=False,
                             auth=auth,
                             timeout=5)

    context.response = response


@given('I am authorized')
def step_impl(context):
    context.oauth = factory(context)
    token = context.oauth.authorize()

    context.config['auth']['refresh_token'] = context.oauth.refresh_token
    context.config['api']['patient'] = token.get('patient',
                                                 context.config['api'].get('patient'))
