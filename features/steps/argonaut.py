# pylint: disable=missing-docstring,function-redefined
from functools import reduce

from behave import then

from features.steps import utils
from testsuite import systems

ERROR_INVALID_BINDING = '{code} is not found in {system}.'
ERROR_REFERENCE_MATCH = '{reference} is not a {resource_type}.'
ERROR_REQUIRED = '{name} not found.'
ERROR_WRONG_FIXED = 'None of {values} match {value}.'


def traverse(resource, path):
    def walk(data, k):
        if isinstance(data, dict):
            return data.get(k)
        elif isinstance(data, list):
            return [reduce(walk, [k], el) for el in data]
        return None

    return reduce(walk, path, resource)


def get_resources(resource, filter_type):
    if 'entry' in resource:
        return [entry['resource'] for entry in resource['entry']
                if entry['resource']['resourceType'] == filter_type]
    else:
        return [resource]


@then(u'there exists one or more {name} in {field_name}')
def step_impl(context, name, field_name):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = traverse(res, path)
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
        found = traverse(res, path)
        for item in found:
            match = traverse(item, sub_path)
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
            reference = traverse(res, path).get('reference')
        except AttributeError:
            reference = ''
        assert reference.startswith(resource_type), \
            utils.bad_response_assert(context.response,
                                      ERROR_REFERENCE_MATCH,
                                      reference=reference,
                                      resource_type=resource_type)


@then(u'there exists one {name} in {field_one_name} or {field_two_name}')
def step_impl(context, name, field_one_name, field_two_name):
    path_one = field_one_name.split('.')
    path_two = field_two_name.split('.')

    filter_type = path_one.pop(0)
    assert filter_type == path_two.pop(0)

    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found_one = traverse(res, path_one)
        found_two = traverse(res, path_two)

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
        found = traverse(res, path)
        assert found is not None, utils.bad_response_assert(context.response,
                                                            ERROR_REQUIRED,
                                                            name=name)


@then(u'{field_name} is bound to {value_set_url_one} or {value_set_url_two}')
def step_impl(context, field_name, value_set_url_one, value_set_url_two):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = traverse(res, path)
        if isinstance(found, str):
            found = [found]

        for code in found:
            try:
                valid = systems.validate_code(code, value_set_url_one) or \
                        systems.validate_code(code, value_set_url_two)
            except systems.SystemNotRecognized:
                valid = False

            system_names = '{0} or {1}'.format(value_set_url_one, value_set_url_two)
            assert valid, utils.bad_response_assert(context.response,
                                                    ERROR_INVALID_BINDING,
                                                    code=code,
                                                    system=system_names)


@then(u'{field_name} is bound to {value_set_url}')
def step_impl(context, field_name, value_set_url):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = traverse(res, path)
        if isinstance(found, str):
            found = [found]

        for code in found:
            try:
                valid = systems.validate_code(code, value_set_url)
            except systems.SystemNotRecognized:
                valid = False

            assert valid, utils.bad_response_assert(context.response,
                                                    ERROR_INVALID_BINDING,
                                                    code=code,
                                                    system=value_set_url)


@then(u'there exists a fixed {field_name}={value}')
def step_impl(context, field_name, value):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = traverse(res, path)
        assert value in found, utils.bad_response_assert(context.response,
                                                         ERROR_WRONG_FIXED,
                                                         values=found,
                                                         value=value)
