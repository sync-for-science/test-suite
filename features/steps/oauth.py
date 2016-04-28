from behave import given, when, then
import requests

ERROR_REVOKE_TOKEN = 'Unable to revoke token: {status_code} - {text}'

@given('I am logged in')
def step_impl(context):

    client_auth = requests.auth.HTTPBasicAuth(context.auth['client_id'],
                                              context.auth['client_secret'])
    post_data = {
        'username': context.auth['username'],
        'password': context.auth['password'],
        'grant_type': 'password',
        'scope': 'smart/portal offline_access',
        'client_id': context.auth['client_id'],
    }
    response = requests.post(context.auth['url'] + '/token',
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()

    context.access_token = token_json['access_token']
    context.refresh_token = token_json['refresh_token']
    context.authorization = "Bearer {access_token}".format(**token_json)

@given('I am not logged in')
def step_impl(context):
    context.authorization = None

@when('I revoke my access token')
def step_impl(context):

    client_auth = requests.auth.HTTPBasicAuth(context.auth['client_id'],
                                              context.auth['client_secret'])
    post_data = {
        'token': context.access_token,
    }
    response = requests.post(context.auth['url'] + '/revoke',
                             auth=client_auth,
                             data=post_data)

    assert int(response.status_code) == 200, \
            ERROR_REVOKE_TOKEN.format(status_code=response.status_code,
                                      text=response.text)

@when('I refresh my access token')
def step_impl(context):

    client_auth = requests.auth.HTTPBasicAuth(context.auth['client_id'],
                                              context.auth['client_secret'])
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': context.refresh_token,
        'client_id': context.auth['client_id'],
    }
    response = requests.post(context.auth['url'] + '/token',
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()

    context.access_token = token_json['access_token']
    context.authorization = "Bearer {access_token}".format(**token_json)
