import requests
from behave import given, when, then, use_step_matcher
from unittest import TestCase

@when('I request a {resource_type} by id {resource_id}')
def step_impl(context, resource_type, resource_id):
    url = "{url}{resource_type}/{resource_id}".format(**{
        'url': context.api_url,
        'resource_type': resource_type,
        'resource_id': resource_id,
    })
    headers = {
        'Authorization': context.authorization,
        'Accept': 'application/json',
    }
    response = requests.get(url, headers=headers)

    context.response = response

@when('I search for {resource_type}s')
def step_impl(context, resource_type):
    url = "{url}{resource_type}?".format(url=context.api_url,
                                         resource_type=resource_type)
    headers = {
        'Authorization': context.authorization,
        'Accept': 'application/json',
    }
    response = requests.get(url, headers=headers)

    context.response = response

use_step_matcher("re")
@then('it will have an? ID')
def step_impl(context):
    resource = context.response.json()

    assert resource['id'] is not None, \
            "Resource id was missing"

@then('the bundle type will be searchset')
def step_impl(context):
    resource = context.response.json()

    assert resource['resourceType'] == 'Bundle', \
            "Resource was not a Bundle"
    assert resource['type'] == 'searchset', \
            "Bundle.type is not searchset"
