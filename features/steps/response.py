from behave import given, when, then

@then('the response code should be {response_code}')
def step_impl(context, response_code):
    response_code = int(response_code)
    assert context.response.status_code == response_code, \
            "response code was {0}".format(context.response.status_code)
