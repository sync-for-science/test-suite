# pylint: disable=missing-docstring,function-redefined
import json

from behave import given, then, when

from features.steps import s4s, utils
from testsuite import systems


ERROR_ENTRY_COUNT = "Found {count} entries."
ERROR_FIELD_MISSING = "Resource field '{field_name}' is missing."
ERROR_FIELD_UNEXPECTED_VALUE = """
Resource field '{field_name}' does not match expected '{expected}', got '{actual}'.
"""
ERROR_NO_ACCESS = 'Could not fetch Patient demographics'
ERROR_NO_NEXT_LINK = 'Link with relation "next" not found.'
ERROR_UNRESOLVED_REFERENCE = "Reference '{reference}' failed to resolve."


def assert_field_exists(context, resource, field_name):
    assert resource.get(field_name) is not None, \
        utils.bad_response_assert(context.response,
                                  ERROR_FIELD_MISSING,
                                  field_name=field_name)


def assert_field_value_matches(context, resource, field_name, expected_value):
    assert resource[field_name] == expected_value, \
        utils.bad_response_assert(context.response,
                                  ERROR_FIELD_UNEXPECTED_VALUE,
                                  field_name=field_name,
                                  expected=expected_value,
                                  actual=resource[field_name])


@given(u'I have access to Patient demographics')
def step_impl(context):
    query = s4s.MU_CCDS_MAPPINGS['Patient demographics']
    query = query.format(patientId=context.vendor_config['versioned_api'].get('patient'))
    response = utils.get_resource(context, query)

    assert response.status_code == 200, \
        utils.bad_response_assert(response,
                                  ERROR_NO_ACCESS)


@when('I follow the "next" link')
def step_impl(context):
    resource = context.response.json()

    links = resource.get('link', [])
    urls = [link['url'] for link in links
            if link['relation'] == 'next']

    if len(urls) is not 1:
        context.scenario.skip(reason=ERROR_NO_NEXT_LINK)
        return

    context.response = utils.get_resource(context, urls[0])


@then('all the codes will be valid')
def step_impl(context):

    resource = context.response.json()

    if resource['resourceType'] == 'Bundle':
        entries = [entry['resource'] for entry in resource.get('entry', [])
                   if entry.get('search', {}).get('mode', 'match') == 'match']
    else:
        entries = [resource]

    context.scenario.systems = []
    bad_codings = []

    for entry in entries:
        found = utils.find_named_key(entry, 'coding')
        for codings in found:
            for coding in codings:
                if not coding:
                    bad_codings.append(coding)
                    continue

                try:
                    valid = systems.validate_coding(coding)
                    recognized = True
                except systems.SystemNotRecognized:
                    valid = True
                    recognized = False

                context.scenario.systems.append({
                    'system': coding.get('system'),
                    'code': coding.get('code'),
                    'valid': valid,
                    'recognized': recognized,
                })

                if not valid:
                    bad_codings.append(coding)

    assert not bad_codings, \
        utils.bad_response_assert(context.response,
                                  'Bad codings: {codings}',
                                  codings=json.dumps(bad_codings, indent=2))


@then('the {field_name} field will be the queried ID')
def step_impl(context, field_name):
    resource = context.response.json()
    patient_id = context.vendor_config['versioned_api'].get('patient')

    assert_field_exists(context, resource, field_name)
    assert_field_value_matches(context, resource, field_name, patient_id)


@then('the {field_name} field will be {value}')
def step_impl(context, field_name, value):
    resource = context.response.json()

    assert_field_exists(context, resource, field_name)
    assert_field_value_matches(context, resource, field_name, value)


@then('the {field_name} field will exist')
def step_impl(context, field_name):
    resource = context.response.json()

    assert_field_exists(context, resource, field_name)


@then('all references will resolve')
def step_impl(context):
    if context.vendor_skip:
        return

    resource = context.response.json()

    if resource['resourceType'] == 'Bundle':
        entries = [entry['resource'] for entry in resource.get('entry', [])
                   if entry.get('search', {}).get('mode', 'match') == 'match']
    else:
        entries = [resource]

    for entry in entries:
        found = utils.find_named_key(entry, 'reference')
        for reference in found:
            check_reference(reference, entry, context)


@then('there should be at least 1 {resource_type} entry')
def step_impl(context, resource_type):
    resource = context.response.json()
    entries = [entry['resource'] for entry in resource.get('entry', [])
               if entry.get('search', {}).get('mode', 'match') == 'match' and
               entry.get('resource', {}).get('resourceType') == resource_type]

    assert len(entries) >= 1, \
        utils.bad_response_assert(context.response,
                                  ERROR_ENTRY_COUNT,
                                  count=len(entries))


@given('there is at least 1 {resource_type} entry')
def step_impl(context, resource_type):
    resource = context.response.json()
    entries = [entry['resource'] for entry in resource.get('entry', [])
               if entry.get('search', {}).get('mode', 'match') == 'match' and
               entry.get('resource', {}).get('resourceType') == resource_type]

    if len(entries) < 1:
        context.scenario.skip(reason=ERROR_ENTRY_COUNT.format(count=0))


@then('all resources will have a {field_name} field')
def step_impl(context, field_name):
    resource = context.response.json()

    if resource['resourceType'] == 'Bundle':
        entries = [entry['resource'] for entry in resource.get('entry', [])
                   if entry.get('search', {}).get('mode', 'match') == 'match']
    else:
        entries = [resource]

    for entry in entries:
        assert_field_exists(context, entry, field_name)


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
        assert len(matches) == 1, \
            utils.bad_response_assert(context.response,
                                      ERROR_UNRESOLVED_REFERENCE,
                                      reference=reference)
    else:
        response = utils.get_resource(context, reference)

        assert int(response.status_code) == 200, \
            utils.bad_response_assert(context.response,
                                      ERROR_UNRESOLVED_REFERENCE,
                                      reference=reference)
