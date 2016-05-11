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


@when('I revoke my access token')
def step_impl(context):
    context.smart.revoke_access_token()
    context.authorization = context.smart.authorization()


@when('I refresh my access token')
def step_impl(context):
    context.smart.refresh_access_token()
    context.authorization = context.smart.authorization()
