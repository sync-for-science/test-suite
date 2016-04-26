from behave import given, when, then

@then('the response code should be {response_code}')
def step_impl(context, response_code):
    print(context.response);
    exit()
