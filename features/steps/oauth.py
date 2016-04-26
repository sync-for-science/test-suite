from behave import given, when, then
import requests

@given('I am logged in')
def step_impl(context):

    client_auth = requests.auth.HTTPBasicAuth('app-demo', 'demo-secret-s4s')
    post_data = {
        'username': 'demo',
        'password': 'demo',
        'grant_type': 'password',
        'scope': 'smart/portal',
        'client_id': 'app-demo',
    }
    response = requests.post('http://52.39.26.206:9000/api/oauth/token',
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()

    context.api_auth = '{token_type} {access_token}'.format(**token_json)
