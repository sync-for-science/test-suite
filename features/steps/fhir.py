# pylint: disable=missing-docstring,function-redefined
import logging
import json

from behave import then

from features.steps import utils


ERROR_FIELD_MISSING = "Resource field '{field_name}' is missing"
ERROR_FIELD_UNEXPECTED_VALUE = """
Resource field '{field_name}' does not match expected '{expected}', got '{actual}'.
"""
ERROR_UNRESOLVED_REFERENCE = "Reference '{reference}' failed to resolve."


@then('the {field_name} field will be {value}')
def step_impl(context, field_name, value):
    resource = context.response.json()

    assert resource[field_name] is not None, \
        ERROR_FIELD_MISSING.format(field_name=field_name)
    assert resource[field_name] == value, \
        ERROR_FIELD_UNEXPECTED_VALUE.format(field_name=field_name,
                                            expected=value,
                                            actual=resource[field_name])


@then('all references will resolve')
def step_impl(context):
    def check_reference(reference):
        response = utils.get_resource(context, reference)

        assert int(response.status_code) == 200, \
            ERROR_UNRESOLVED_REFERENCE.format(reference=reference)

    resource = context.response.json()
    found_references = utils.find_references(resource)

    logging.info(json.dumps(resource))

    for reference in found_references:
        check_reference(reference)
