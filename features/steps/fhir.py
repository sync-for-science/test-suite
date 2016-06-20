# pylint: disable=missing-docstring,function-redefined
from behave import then

from features.steps import utils


ERROR_ENTRY_COUNT = "Found {count} entries."
ERROR_FIELD_MISSING = "Resource field '{field_name}' is missing."
ERROR_FIELD_UNEXPECTED_VALUE = """
Resource field '{field_name}' does not match expected '{expected}', got '{actual}'.
"""
ERROR_UNRESOLVED_REFERENCE = "Reference '{reference}' failed to resolve."


@then('the {field_name} field will be {value}')
def step_impl(context, field_name, value):
    resource = context.response.json()

    assert resource.get(field_name) is not None, \
        utils.bad_response_assert(context.response,
                                  ERROR_FIELD_MISSING,
                                  field_name=field_name)
    assert resource[field_name] == value, \
        utils.bad_response_assert(context.response,
                                  ERROR_FIELD_UNEXPECTED_VALUE,
                                  field_name=field_name,
                                  expected=value,
                                  actual=resource[field_name])


@then('the {field_name} field will exist')
def step_impl(context, field_name):
    resource = context.response.json()

    assert resource.get(field_name) is not None, \
        utils.bad_response_assert(context.response,
                                  ERROR_FIELD_MISSING,
                                  field_name=field_name)


@then('all references will resolve')
def step_impl(context):
    resource = context.response.json()

    if resource['resourceType'] == 'Bundle':
        entries = [entry['resource'] for entry in resource.get('entry', [])]
    else:
        entries = [resource]

    for entry in entries:
        found = utils.find_references(entry)
        for reference in found:
            check_reference(reference, entry, context)


@then('there should be at least 1 entry')
def step_impl(context):
    resource = context.response.json()
    entries = resource.get('entry', [])

    assert len(entries) >= 1, \
        utils.bad_response_assert(context.response,
                                  ERROR_ENTRY_COUNT,
                                  count=len(entries))


@then('all resources will have a {field_name} field')
def step_impl(context, field_name):
    resource = context.response.json()

    if resource['resourceType'] == 'Bundle':
        entries = [entry['resource'] for entry in resource.get('entry', [])]
    else:
        entries = [resource]

    for entry in entries:
        assert entry.get(field_name) is not None, \
            utils.bad_response_assert(context.response,
                                      ERROR_FIELD_MISSING,
                                      field_name=field_name)


def check_reference(reference, orig, context):
    """ Follow references and make sure they exist.

    Args:
        reference (str): A reference in the format:
           * Resource/id
           * http://example.com/base/Resource/id
           * #id
        orig (dict): The original resource, used when checking contained references.
        context: The behave context
    """
    if reference.startswith('#'):
        matches = [contained for contained in orig.get('contained', [])
                   if contained['id'] == reference[1:]]
        assert len(matches) > 0, \
            utils.bad_response_assert(context.response,
                                      ERROR_UNRESOLVED_REFERENCE,
                                      reference=reference)
    else:
        response = utils.get_resource(context, reference)

        assert int(response.status_code) == 200, \
            utils.bad_response_assert(context.response,
                                      ERROR_UNRESOLVED_REFERENCE,
                                      reference=reference)
