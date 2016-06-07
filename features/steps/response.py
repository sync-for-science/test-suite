# pylint: disable=missing-docstring,function-redefined
from behave import then

from features.steps import utils


ERROR_STATUS_CODE = """
Response code was {status_code}.
"""
ERROR_MISSING_FIELD = """
Field "{field}" not found in {response_fields}.
"""


@given('I have a response')
def step_impl(context):
    assert context.response, 'No response'


@then('the response code should be {response_code}')
def step_impl(context, response_code):
    response_code = int(response_code)

    assert context.response.status_code == response_code, \
        utils.bad_response_assert(context.response,
                                  ERROR_STATUS_CODE,
                                  status_code=context.response.status_code)


@then('the response code should not be {response_code}')
def step_impl(context, response_code):
    response_code = int(response_code)

    assert context.response.status_code != response_code, \
        utils.bad_response_assert(context.response,
                                  ERROR_STATUS_CODE,
                                  status_code=context.response.status_code)


@then('the JSON response will contain {field}')
def step_impl(context, field):
    data = context.response.json()

    assert field in data, \
        utils.bad_response_assert(context.response,
                                  ERROR_MISSING_FIELD,
                                  field=field,
                                  response_fields=list(data.keys()))
