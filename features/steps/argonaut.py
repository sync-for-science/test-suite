# pylint: disable=missing-docstring,function-redefined

import json
import re

from behave import then

from features.steps import utils

from testsuite import systems

ERROR_CODING_MISSING = '''
{field_name} is missing field "coding".
{json}
'''
ERROR_MISSING_SYSTEM_CODING = 'No codings in {field_name} match {system}.'
ERROR_FIELD_NOT_PRESENT = '''
{field} is not set.
{json}
'''
ERROR_INVALID_BINDING = '''
{code} is not found in {system}.
{json}
'''
ERROR_REFERENCE_MATCH = '{reference} is not a {resource_type}.'
ERROR_REQUIRED = '{name} not found.'
ERROR_MISSING_FIELD = ('The resources identified by ids ({resource_ids}) were absent'
                       ' all of the following fields: {field_list}')

ERROR_WRONG_FIXED = 'None of {values} match {value}.'


def get_resources(resource, filter_type):
    if 'entry' in resource:
        return [entry['resource'] for entry in resource['entry']
                if entry['resource']['resourceType'] == filter_type]
    else:
        return [resource]


def in_value_set(coding, value_set_url):
    try:
        return systems.validate_code(coding.get('code'), value_set_url)
    except systems.SystemNotRecognized:
        return False


@then(u'there exists one or more {name} in {field_name}')
def step_impl(context, name, field_name):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = utils.traverse(res, path)
        assert len(found) > 0, utils.bad_response_assert(context.response,
                                                         ERROR_REQUIRED,
                                                         name=name)


@then(u'each {field_name} must have a {sub_field}')
def step_impl(context, field_name, sub_field):
    path = field_name.split('.')
    filter_type = path.pop(0)
    sub_path = sub_field.split('.')
    sub_type = sub_path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = utils.traverse(res, path)
        for item in found:
            match = utils.traverse(item, sub_path)
            assert match is not None, \
                utils.bad_response_assert(context.response,
                                          ERROR_REQUIRED,
                                          name=sub_type)


@then(u'there exists one reference to a {resource_type} in {field_name}')
def step_impl(context, resource_type, field_name):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        try:
            reference = utils.traverse(res, path).get('reference')

            reference_regex = r'((http|https)://([A-Za-z0-9\\\.\:\%\$]\/)*)?(' + \
                resource_type + ')\/[A-Za-z0-9\-\.]{1,64}(\/_history\/[A-Za-z0-9\-\.]{1,64})?'
            compiled_regex = re.compile(reference_regex)
            regex_search_results = compiled_regex.search(reference)

        except AttributeError:
            reference = ''

        assert regex_search_results, \
            utils.bad_response_assert(context.response,
                                      ERROR_REFERENCE_MATCH,
                                      reference=reference,
                                      resource_type=resource_type)


@then(u'one of the following paths exist: {field_string} in {resource}')
def step_impl(context, field_string, resource):

    fields_to_find = field_string.split(",")

    resources = get_resources(context.response.json(), resource)

    valid_resource_ids = set([
        res.get("id") for res in resources
        if utils.has_one_of(res, fields_to_find)])

    all_resource_ids = set([res.get("id") for res in resources])

    invalid_resource_ids = all_resource_ids - valid_resource_ids

    assert len(invalid_resource_ids) == 0, \
        utils.bad_response_assert(context.response,
                                  ERROR_MISSING_FIELD,
                                  resource_ids=', '.join(invalid_resource_ids),
                                  field_list=field_string)


@then(u'there exists one {name} in {field_one_name} or {field_two_name}')
def step_impl(context, name, field_one_name, field_two_name):
    path_one = field_one_name.split('.')
    path_two = field_two_name.split('.')

    filter_type = path_one.pop(0)
    assert filter_type == path_two.pop(0)

    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found_one = utils.traverse(res, path_one)
        found_two = utils.traverse(res, path_two)

        assert (found_one is not None) or (found_two is not None), \
            utils.bad_response_assert(context.response,
                                      ERROR_REQUIRED,
                                      name=name)


@then(u'there exists one {name} in {field_name}')
def step_impl(context, name, field_name):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = utils.traverse(res, path)
        assert found is not None, utils.bad_response_assert(context.response,
                                                            ERROR_REQUIRED,
                                                            name=name)


@then(u'{field_name} is bound to {value_set_url_one} or {value_set_url_two}')
def step_impl(context, field_name, value_set_url_one, value_set_url_two):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)
    system_names = '{0} or {1}'.format(value_set_url_one, value_set_url_two)

    for res in resources:
        found = utils.traverse(res, path)
        if isinstance(found, str):
            found = [found]
        elif isinstance(found, dict):
            assert 'coding' in found, \
                utils.bad_response_assert(context.response,
                                          ERROR_CODING_MISSING,
                                          field_name=field_name,
                                          json=json.dumps(found, indent=2))
            found = [coding.get('code') for coding in found.get('coding')
                     if in_value_set(coding, value_set_url_one) or
                     in_value_set(coding, value_set_url_two)]

        assert found, \
            utils.bad_response_assert(context.response,
                                      ERROR_MISSING_SYSTEM_CODING,
                                      field_name=field_name,
                                      system=system_names)

        for code in found:
            try:
                valid = systems.validate_code(code, value_set_url_one) or \
                        systems.validate_code(code, value_set_url_two)
            except systems.SystemNotRecognized:
                valid = False

            assert valid, utils.bad_response_assert(context.response,
                                                    ERROR_INVALID_BINDING,
                                                    code=code,
                                                    system=system_names,
                                                    json=json.dumps(res, indent=2))


@then(u'{field_name} is bound to {value_set_url}')
def step_impl(context, field_name, value_set_url):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = utils.traverse(res, path)
        if isinstance(found, str):
            found = [found]
        elif isinstance(found, dict):
            assert 'coding' in found, \
                utils.bad_response_assert(context.response,
                                          ERROR_CODING_MISSING,
                                          field_name=field_name,
                                          json=json.dumps(found, indent=2))
            found = [coding.get('code') for coding in found.get('coding')
                     if in_value_set(coding, value_set_url)]

        assert found, \
            utils.bad_response_assert(context.response,
                                      ERROR_MISSING_SYSTEM_CODING,
                                      field_name=field_name,
                                      system=value_set_url)

        for code in found:
            try:
                valid = systems.validate_code(code, value_set_url)
            except systems.SystemNotRecognized:
                valid = False

            assert valid, utils.bad_response_assert(context.response,
                                                    ERROR_INVALID_BINDING,
                                                    code=code,
                                                    system=value_set_url,
                                                    json=json.dumps(res, indent=2))


@then(u'there exists a fixed {field_name}={value}')
def step_impl(context, field_name, value):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = utils.traverse(res, path)
        assert found, utils.bad_response_assert(context.response,
                                                ERROR_FIELD_NOT_PRESENT,
                                                field=field_name,
                                                json=json.dumps(res, indent=2))
        assert value in found, utils.bad_response_assert(context.response,
                                                         ERROR_WRONG_FIXED,
                                                         values=found,
                                                         value=value)
