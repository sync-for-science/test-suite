# pylint: disable=missing-docstring,function-redefined
from behave import given, when
from testsuite.oauth import factory


@given('I am logged in')
def step_impl(context):
    context.smart = factory(context)

    context.smart.request_offline_access()
    context.authorization = context.smart.authorization()


@given('I am not logged in')
def step_impl(context):
    context.authorization = None


@when('I refresh my access token')
def step_impl(context):
    context.smart.refresh_access_token()
    context.authorization = context.smart.authorization()


@when('I ask for authorization without the {field_name} field')
def step_impl(context, field_name):
    """ TODO: remove inline imports, reduce duplication. """
    import requests
    from testsuite import fhir
    import uuid
    from pprint import pprint

    fields = {
        'response_type': 'code',
        'client_id': context.config['auth']['client_id'],
        'redirect_uri': context.config['auth']['redirect_uri'],
        'scope': 'launch/patient patient/Patient.read',
        'state': uuid.uuid4(),
    }

    del fields[field_name]

    uris = fhir.get_oauth_uris(context.config['api']['url'])
    response = requests.get(uris['authorize'],
                            params=fields,
                            allow_redirects=False,
                            timeout=5)

    context.response = response


@when('I ask for a new access token')
def step_impl(context):
    """ TODO: remove inline imports, reduce duplication. """
    import requests
    from testsuite import fhir

    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.smart.refresh_token,
        'scope': 'launch/patient patient/Patient.read',
    }

    auth = requests.auth.HTTPBasicAuth(context.config['auth']['client_id'],
                                       context.config['auth']['client_secret'])

    uris = fhir.get_oauth_uris(context.config['api']['url'])
    response = requests.post(uris['token'],
                             data=fields,
                             allow_redirects=False,
                             auth=auth,
                             timeout=5)

    context.response = response


@when('I ask for a new access token without the {field_name} field')
def step_impl(context, field_name):
    """ TODO: remove inline imports, reduce duplication. """
    import requests
    from testsuite import fhir

    fields = {
        'grant_type': 'refresh_token',
        'refresh_token': context.smart.refresh_token,
        'scope': 'launch/patient patient/Patient.read',
    }

    auth = requests.auth.HTTPBasicAuth(context.config['auth']['client_id'],
                                       context.config['auth']['client_secret'])

    if field_name == 'client_id':
        auth = None
    else:
        del fields[field_name]

    uris = fhir.get_oauth_uris(context.config['api']['url'])
    response = requests.post(uris['token'],
                             data=fields,
                             allow_redirects=False,
                             auth=auth,
                             timeout=5)

    context.response = response
