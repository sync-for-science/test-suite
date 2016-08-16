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


@then(u'there exists one reference to a {resource_type} in {field_name}')
def step_impl(context, resource_type, field_name):
    resource = context.response.json()

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = [entry['resource'] for entry in resource['entry']
                 if entry['resource']['resourceType'] == filter_type]

    for res in resources:
        reference = traverse(res, path).get('reference')
        assert reference.startswith(resource_type), \
            utils.bad_response_assert(context.response,
                                      ERROR_REFERENCE_MATCH,
                                      reference=reference,
                                      resource_type=resource_type)


@then(u'there exists one {name} in {field_name}')
def step_impl(context, name, field_name):
    resource = context.response.json()

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = [entry['resource'] for entry in resource['entry']
                 if entry['resource']['resourceType'] == filter_type]

    for res in resources:
        found = traverse(res, path)
        assert found, utils.bad_response_assert(context.response,
                                                ERROR_REQUIRED,
                                                name=name)


@then(u'{field_name} is bound to {value_set_url}')
def step_impl(context, field_name, value_set_url):
    resource = context.response.json()

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = [entry['resource'] for entry in resource['entry']
                 if entry['resource']['resourceType'] == filter_type]

    for res in resources:
        found = traverse(res, path)
        if isinstance(found, str):
            found = [found]

        for code in found:
            coding = {
                'system': value_set_url,
                'code': code,
            }
            valid = systems.validate_coding(coding)

            assert valid, utils.bad_response_assert(context.response,
                                                    ERROR_INVALID_BINDING,
                                                    code=code,
                                                    system=value_set_url)


@then(u'there exists a fixed {field_name}={value}')
def step_impl(context, field_name, value):
    resource = context.response.json()

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = [entry['resource'] for entry in resource['entry']
                 if entry['resource']['resourceType'] == filter_type]

    for res in resources:
        found = traverse(res, path)
        assert value in found, utils.bad_response_assert(context.response,
                                                         ERROR_WRONG_FIXED,
                                                         values=found,
                                                         value=value)
