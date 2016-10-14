# pylint: disable=missing-docstring,function-redefined
import uuid

from behave import given, then, when
import requests

from features.steps import s4s, utils
from testsuite.oauth import authorize
from testsuite import fhir


AUTHORIZATION_ACTIONS = ['allow', 'deny']
ERROR_AUTHORIZATION_FAILED = 'Authorization failed.'
ERROR_BAD_CONFORMANCE = 'Could not parse conformance statement.'
ERROR_NO_REVOKE = 'Revoking authorizations is not enabled.'
ERROR_OAUTH_DISABLED = 'OAuth is not enabled on this server.'
ERROR_SELENIUM_SCREENSHOT = '''
An authorization error occurred: {0}

Current URL: {2}

For more information, see:
    {3}{1}
'''


@given('OAuth is enabled')
def step_impl(context):
    assert context.vendor_config['auth']['strategy'] != 'none', \
        ERROR_OAUTH_DISABLED

    if context.conformance is None:
        assert False, ERROR_BAD_CONFORMANCE

    fhir.get_oauth_uris(context.conformance)


@given('revoking authorizations is enabled')
def step_impl(context):
    auth_config = context.vendor_config['auth']
    keys = ('revoke_steps', 'revoke_url')

    if not all(key in auth_config for key in keys):
        context.scenario.skip(reason=ERROR_NO_REVOKE)
        return


@given('I am logged in')
def step_impl(context):
    assert context.oauth is not None, ERROR_AUTHORIZATION_FAILED
    assert context.oauth.access_token is not None, \
        ERROR_AUTHORIZATION_FAILED


@given('I am not logged in')
def step_impl(context):
    context.oauth.access_token = None

    context.cache.clear()


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


@when('I revoke my authorization')
def step_impl(context):
    revoker = authorize.AuthorizationRevoker(context.vendor_config['auth'])

    try:
        with revoker:
            revoker.revoke_authorization()
    except authorize.AuthorizationException as err:
        error = ERROR_SELENIUM_SCREENSHOT.format(
            err.args[0],
            err.args[1],
            context.vendor_config['host'],
        )
        assert False, error

    context.cache.clear()


@when('I ask for authorization without the {field_name} field')
def step_impl(context, field_name):
    """ A step 1 implementation with a named field missing.
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


@when('I request authorization with the following override')
def step_impl(context):
    """ A step 1 implementation with a named field missing.
    """
    fields = {
        'response_type': 'code',
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
        'scope': context.vendor_config['auth']['scope'],
        'state': uuid.uuid4(),
    }

    fields.update(dict(context.table))

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
    try:
        context.code = context.oauth.request_authorization()
    except authorize.AuthorizationException as err:
        error = ERROR_SELENIUM_SCREENSHOT.format(
            err.args[0],
            err.args[1],
            context.vendor_config['host'],
        )
        assert False, error


@when('I authorize the app {action}ing access to {resource_type}')
def step_impl(context, action, resource_type):

    assert action in AUTHORIZATION_ACTIONS
    assert resource_type in s4s.MU_CCDS_MAPPINGS

    # Filter the steps to only what is required for this authorization
    condition = '{0}.{1}'.format(action, resource_type)
    steps = context.vendor_config['auth'].get('steps', [])
    steps = [step for step in steps
             if 'when' not in step or step['when'] == condition]
    context.vendor_config['auth']['steps'] = steps

    # Construct a modified authorizer
    urls = fhir.get_oauth_uris(context.conformance)
    authorizer = authorize.Authorizer(config=context.vendor_config['auth'],
                                      authorize_url=urls['authorize'])
    context.oauth.authorizer = authorizer

    # Authorize the app as usual
    try:
        context.code = context.oauth.request_authorization()
    except authorize.AuthorizationException as err:
        error = ERROR_SELENIUM_SCREENSHOT.format(
            err.args[0],
            err.args[1],
            context.vendor_config['host'],
        )
        assert False, error


@when('I exchange my authorization code')
def step_impl(context):
    """ A fully formed and correct step 3 implementation.
    """
    fields = {
        'grant_type': 'authorization_code',
        'code': context.code,
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
    }

    context.response = token_request(fields,
                                     context.vendor_config['auth'],
                                     context.conformance)


@when('I exchange my authorization code without the {field_name} field')
def step_impl(context, field_name):
    """ A step 3 implementation missing a named field.
    """
    fields = {
        'grant_type': 'authorization_code',
        'code': context.code,
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
    }

    del fields[field_name]

    context.response = token_request(fields,
                                     context.vendor_config['auth'],
                                     context.conformance)


@when('I exchange my authorization code with the following override')
def step_impl(context):
    """ A step 3 implementation with a table specified override.
    """
    fields = {
        'grant_type': 'authorization_code',
        'code': context.code,
        'client_id': context.vendor_config['auth']['client_id'],
        'redirect_uri': context.vendor_config['auth']['redirect_uri'],
    }

    fields.update(dict(context.table))

    context.response = token_request(fields,
                                     context.vendor_config['auth'],
                                     context.conformance)


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
    """ A fully formed and correct implementation of step 5.
    """
    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.oauth.refresh_token,
        'scope': context.vendor_config['auth']['scope'],
    }

    context.response = token_request(fields,
                                     context.vendor_config['auth'],
                                     context.conformance)


@when('I ask for a new access token without the {field_name} field')
def step_impl(context, field_name):
    """ A step 5 implementation missing a named field.
    """
    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.oauth.refresh_token,
        'scope': context.vendor_config['auth']['scope'],
    }

    del fields[field_name]

    context.response = token_request(fields,
                                     context.vendor_config['auth'],
                                     context.conformance)


def token_request(post_data, auth_config, conformance):
    """ Make a token request.

    Should be modeled after `testsuite.oauth.authorization_code._token_request`.

    Args:
        post_data (dict): The parameters to send.
        auth_config (dict): The vendor auth config.
        conformance (dict): The server's conformance statement so that URIs can be determined.

    Returns:
        A requests Response object.
    """
    auth = None
    if auth_config.get('confidential_client'):
        auth = requests.auth.HTTPBasicAuth(auth_config['client_id'],
                                           auth_config['client_secret'])

    uris = fhir.get_oauth_uris(conformance)

    response = requests.post(uris['token'],
                             data=post_data,
                             allow_redirects=False,
                             auth=auth,
                             timeout=5)

    return response
