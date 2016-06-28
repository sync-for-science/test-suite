# pylint: disable=missing-docstring,function-redefined
import uuid

from behave import given, then, when
import requests

from features.steps import utils
from testsuite.oauth import authorize
from testsuite import fhir


ERROR_AUTHORIZATION_FAILED = 'Authorization failed.'
ERROR_BAD_CONFORMANCE = 'Could not parse conformance statement.'
ERROR_OAUTH_DISABLED = 'OAuth is not enabled on this server.'
ERROR_SELENIUM_SCREENSHOT = '''
An authorization error occurred: {0}

For more information, see:
    {2}{1}
'''


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
    context.oauth.access_token = None


@when('I log in')
def step_impl(context):
    try:
        context.oauth.authorize()
    except authorize.AuthorizationException as err:
        error = ERROR_SELENIUM_SCREENSHOT.format(
            err.args[0],
            err.args[1],
            context.vendor_config['host'],
        )
        assert False, error


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


@when('I ask for authorization with the following override')
def step_impl(context):
    urls = fhir.get_oauth_uris(context.conformance)
    authorizer = authorize.Authorizer(config=context.vendor_config['auth'],
                                      authorize_url=urls['authorize'])
    with authorizer:
        parameters = authorizer.launch_params
        parameters.update(dict(context.table))

        try:
            authorizer.ask_for_authorization(parameters)
            response = authorizer.provide_user_input()
        except authorize.AuthorizationException as err:
            error = ERROR_SELENIUM_SCREENSHOT.format(
                err.args[0],
                err.args[1],
                context.vendor_config['host'],
            )
            assert False, error

    context.authorizer = authorizer
    context.authorization_sent = parameters
    context.authorization_received = response


@when('I ask for authorization')
def step_impl(context):
    context.code = context.oauth.request_authorization()


@when('I exchange my grant code')
def step_impl(context):
    fields = {
        'grant_type': 'authorization_code',
        'code': context.code,
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
    }

    uris = fhir.get_oauth_uris(context.conformance)

    auth = None
    if context.vendor_config['auth'].get('confidential_client'):
        auth = requests.auth.HTTPBasicAuth(
            context.vendor_config['auth']['client_id'],
            context.vendor_config['auth']['client_secret'],
        )

    response = requests.post(uris['token'],
                             auth=auth,
                             data=fields)

    context.response = response


@when('I exchange my grant code without the {field_name} field')
def step_impl(context, field_name):
    fields = {
        'grant_type': 'authorization_code',
        'code': context.code,
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
    }

    del fields[field_name]

    uris = fhir.get_oauth_uris(context.conformance)

    auth = None
    if context.vendor_config['auth'].get('confidential_client'):
        auth = requests.auth.HTTPBasicAuth(
            context.vendor_config['auth']['client_id'],
            context.vendor_config['auth']['client_secret'],
        )

    response = requests.post(uris['token'],
                             auth=auth,
                             data=fields)

    context.response = response


@when('I exchange my grant code with the following override')
def step_impl(context):
    fields = {
        'grant_type': 'authorization_code',
        'code': context.code,
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
    }

    fields.update(dict(context.table))

    uris = fhir.get_oauth_uris(context.conformance)

    auth = None
    if context.vendor_config['auth'].get('confidential_client'):
        auth = requests.auth.HTTPBasicAuth(
            context.vendor_config['auth']['client_id'],
            context.vendor_config['auth']['client_secret'],
        )

    response = requests.post(uris['token'],
                             auth=auth,
                             data=fields)

    context.response = response


@then('the authorization response redirect should validate')
def step_impl(context):
    try:
        response = context.authorization_received
        context.authorizer._validate_state(response)  # pylint: disable=protected-access
        context.authorizer._validate_code(response)  # pylint: disable=protected-access
    except AssertionError as err:
        assert False, utils.bad_redirect_assert(err,
                                                context.authorization_sent,
                                                response)


@when('I ask for a new access token')
def step_impl(context):
    """ TODO: reduce duplication.
    """
    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.oauth.refresh_token,
        'scope': context.vendor_config['auth']['scope'],
    }

    uris = fhir.get_oauth_uris(context.conformance)

    auth = None
    if context.vendor_config['auth'].get('confidential_client'):
        auth = requests.auth.HTTPBasicAuth(
            context.vendor_config['auth']['client_id'],
            context.vendor_config['auth']['client_secret'],
        )

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

    auth = None
    if context.vendor_config['auth'].get('confidential_client'):
        auth = requests.auth.HTTPBasicAuth(
            context.vendor_config['auth']['client_id'],
            context.vendor_config['auth']['client_secret'],
        )

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
