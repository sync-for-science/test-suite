from behave import given, when, then
from features.steps import utils

@given('I am logged in')
def step_impl(context):
    post_data = {
        'username': context.auth['username'],
        'password': context.auth['password'],
        'grant_type': 'password',
        'scope': 'smart/portal offline_access',
        'client_id': context.auth['client_id'],
    }
    response = utils.auth_request(context, '/token', post_data)

    token_json = response.json()
    context.access_token = token_json['access_token']
    context.refresh_token = token_json['refresh_token']
    context.authorization = "Bearer {access_token}".format(**token_json)

@given('I am not logged in')
def step_impl(context):
    context.authorization = None

@when('I revoke my access token')
def step_impl(context):
    post_data = {
        'token': context.access_token,
    }
    utils.auth_request(context, '/revoke', post_data)

@when('I refresh my access token')
def step_impl(context):
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': context.refresh_token,
        'client_id': context.auth['client_id'],
    }
    response = utils.auth_request(context, '/token', post_data)

    token_json = response.json()
    context.access_token = token_json['access_token']
    context.authorization = "Bearer {access_token}".format(**token_json)
