from behave import given, when, then
import requests

@given('I am logged in')
def step_impl(context):

    client_auth = requests.auth.HTTPBasicAuth(context.auth['client_id'],
                                              context.auth['client_secret'])
    post_data = {
        'username': context.auth['username'],
        'password': context.auth['password'],
        'grant_type': 'password',
        'scope': 'smart/portal',
        'client_id': context.auth['client_id'],
    }
    response = requests.post(context.auth['token_url'],
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()

    context.authorization = '{token_type} {access_token}'.format(**token_json)

@given('I am not logged in')
def step_impl(context):
    context.authorization = None
