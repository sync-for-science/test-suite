# pylint: disable=missing-docstring,function-redefined
from behave import then


ERROR_STATUS_CODE = """
Response code was {status_code}.
{text}
"""
ERROR_MISSING_FIELD = """
Field "{field}" not found in {response_fields}.
"""


@then('the response code should be {response_code}')
def step_impl(context, response_code):
    response_code = int(response_code)

    assert context.response.status_code == response_code, \
        ERROR_STATUS_CODE.format(status_code=context.response.status_code,
                                 text=context.response.text)


@then('the response code should not be {response_code}')
def step_impl(context, response_code):
    response_code = int(response_code)

    assert context.response.status_code != response_code, \
        ERROR_STATUS_CODE.format(status_code=context.response.status_code,
                                 text='')


@then('the JSON response will contain {field}')
def step_impl(context, field):
    data = context.response.json()

    assert field in data, \
        ERROR_MISSING_FIELD.format(field=field,
                                   response_fields=list(data.keys()))
