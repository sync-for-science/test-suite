# pylint: disable=missing-docstring,function-redefined

import json
import re

from behave import then

from features.steps import utils

from testsuite import systems

from features.steps.deciders import StepDecider, ArgonautObservationDecider

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

ERROR_UCUM_CODES = 'Unit validation failed for {field_name}.'

ERROR_NO_VALID_ENTRIES = 'No resources have {field_name} set to {value}.'

vitals_code_lookup = {"9279-1": ["/min"],
                      "8867-4": ["/min"],
                      "59408-5": ["%"],
                      "8310-5": ["Cel", "[degF]"],
                      "8302-2": ["cm", "[in_i]"],
                      "8306-3": ["cm", "[in_i]"],
                      "8287-5": ["cm", "[in_i]"],
                      "29463-7": ["g", "kg", "[lb_av]"],
                      "39156-5": ["kg/m2"],
                      "8480-6": ["mm[Hg]"],
                      "8462-4": ["mm[Hg]"]}


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

    if not StepDecider(context).should_run_test():
        return

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

    if not StepDecider(context).should_run_test():
        return

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
                utils.bad_response_assert_with_resource(response=context.response,
                                                        message=ERROR_REQUIRED,
                                                        resource=res,
                                                        name=sub_type)


@then(u'there exists one reference to a {resource_type} in {field_name}')
def step_impl(context, resource_type, field_name):

    if not StepDecider(context).should_run_test():
        return

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        try:
            reference = utils.traverse(res, path).get('reference')

            # Validate the reference for FHIR compliance formatting.
            # http://hl7.org/fhir/references.html
            reference_regex = r'((http|https)://([A-Za-z0-9\\\.\:\%\$]\/)*)?(' + \
                resource_type + r')\/[A-Za-z0-9\-\.]{1,64}(\/_history\/[A-Za-z0-9\-\.]{1,64})?'
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

    if not StepDecider(context).should_run_test():
        return

    fields_to_find = field_string.split(",")

    resources = get_resources(context.response.json(), resource)

    valid_resource_ids = set([
        res.get("id") for res in resources
        if not ArgonautObservationDecider(res).should_validate() or
        utils.has_one_of(res, fields_to_find)])

    all_resource_ids = set([res.get("id") for res in resources])

    invalid_resource_ids = all_resource_ids - valid_resource_ids

    assert len(invalid_resource_ids) == 0, \
        utils.bad_response_assert(context.response,
                                  ERROR_MISSING_FIELD,
                                  resource_ids=', '.join(invalid_resource_ids),
                                  field_list=field_string)


@then(u'there exists one {name} in {field_one_name} or {field_two_name}')
def step_impl(context, name, field_one_name, field_two_name):

    if not StepDecider(context).should_run_test():
        return

    path_one = field_one_name.split('.')
    path_two = field_two_name.split('.')

    filter_type = path_one.pop(0)
    assert filter_type == path_two.pop(0)

    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found_one = utils.traverse(res, path_one)
        found_two = utils.traverse(res, path_two)

        assert (found_one is not None) or (found_two is not None), \
            utils.bad_response_assert_with_resource(response=context.response,
                                                    message=ERROR_REQUIRED,
                                                    resource=res,
                                                    name=name
                                                    )


@then(u'there exists one {name} in {field_name}')
def step_impl(context, name, field_name):

    if not StepDecider(context).should_run_test():
        return

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        found = utils.traverse(res, path)
        assert found is not None, utils.bad_response_assert_with_resource(response=context.response,
                                                                          message=ERROR_REQUIRED,
                                                                          name=name,
                                                                          resource=res)


@then(u'{field_name} is bound to {value_set_url_one} or {value_set_url_two}')
def step_impl(context, field_name, value_set_url_one, value_set_url_two):

    if not StepDecider(context).should_run_test():
        return

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
                utils.bad_response_assert_with_resource(response=context.response,
                                                        message=ERROR_CODING_MISSING,
                                                        resource=res,
                                                        field_name=field_name,
                                                        json=json.dumps(found, indent=2))
            found = [coding.get('code') for coding in found.get('coding')
                     if in_value_set(coding, value_set_url_one) or
                     in_value_set(coding, value_set_url_two)]

        assert found, \
            utils.bad_response_assert_with_resource(response=context.response,
                                                    message=ERROR_MISSING_SYSTEM_CODING,
                                                    resource=res,
                                                    field_name=field_name,
                                                    system=system_names)

        for code in found:
            try:
                valid = systems.validate_code(code, value_set_url_one) or \
                        systems.validate_code(code, value_set_url_two)
            except systems.SystemNotRecognized:
                valid = False

            assert valid, utils.bad_response_assert_with_resource(response=context.response,
                                                                  message=ERROR_INVALID_BINDING,
                                                                  resource=res,
                                                                  code=code,
                                                                  system=system_names,
                                                                  json=json.dumps(res, indent=2))


@then(u'{field_name} is bound to {value_set_url}')
def step_impl(context, field_name, value_set_url):
    if not StepDecider(context).should_run_test():
        return

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        if ArgonautObservationDecider(res).should_validate():
            found = utils.traverse(res, path)
            if isinstance(found, str):
                found = [found]
            elif isinstance(found, dict):
                assert 'coding' in found, \
                    utils.bad_response_assert_with_resource(response=context.response,
                                                            message=ERROR_CODING_MISSING,
                                                            resource=res,
                                                            field_name=field_name,
                                                            json=json.dumps(found, indent=2))
                found = [coding.get('code') for coding in found.get('coding')
                         if in_value_set(coding, value_set_url)]

            assert found, \
                utils.bad_response_assert_with_resource(response=context.response,
                                                        message=ERROR_MISSING_SYSTEM_CODING,
                                                        resource=res,
                                                        field_name=field_name,
                                                        system=value_set_url)

            for code in found:
                try:
                    valid = systems.validate_code(code, value_set_url)
                except systems.SystemNotRecognized:
                    valid = False

                assert valid, utils.bad_response_assert_with_resource(
                    response=context.response,
                    message=ERROR_INVALID_BINDING,
                    resource=res,
                    code=code,
                    system=value_set_url,
                    json=json.dumps(res, indent=2))


@then(u'there is at least one entry with a fixed {field_name}={value}')
def step_impl(context, field_name, value):
    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    found_one = found_at_least_one(resources, path, value)

    assert found_one, utils.bad_response_assert(
        response=context.response,
        message=ERROR_NO_VALID_ENTRIES,
        field_name=field_name,
        value=value)


def found_at_least_one(resources, path, value):
    """
    Return a boolean indicating if we found a resource with
    the specified path declared, having the specified value.
    :param resources: A list of dictionaries.
    :param path: A list representing the steps in the path, top element is NOT the resource type.
    :param value: The value you want the last element in the path to have.
    :return: Boolean
    """
    for res in resources:
        found_path = utils.traverse(res, path)

        if found_path and value in found_path:
            return True

    return False


@then(u'there exists a fixed {field_name}={value}')
def step_impl(context, field_name, value):

    if not StepDecider(context).should_run_test():
        return

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    for res in resources:
        if ArgonautObservationDecider(res).should_validate():
            found = utils.traverse(res, path)

            assert found, utils.bad_response_assert_with_resource(
                response=context.response,
                message=ERROR_FIELD_NOT_PRESENT,
                resource=res,
                field=field_name,
                json=json.dumps(res, indent=2))

            assert value in found, utils.bad_response_assert_with_resource(
                response=context.response,
                message=ERROR_WRONG_FIXED,
                resource=res,
                values=found,
                value=value)


def vital_unit_validation(field_name, resource, system_url):

    path = field_name.split('.')
    path.pop(0)

    systems_to_validate = utils.traverse(resource, path + ["system"])
    codes_to_validate = utils.traverse(resource, path + ["code"])
    resource_components = utils.traverse(resource, ["component"])
    values_to_validate = [resource] + \
        (resource_components if resource_components is not None else [])

    if not isinstance(systems_to_validate, list):
        systems_to_validate = [systems_to_validate]

    if not isinstance(codes_to_validate, list):
        codes_to_validate = [codes_to_validate]

    if any(system != system_url for system in systems_to_validate):
        return {"resource": resource, "status": "Wrong System"}

    if any(not in_value_set({"code": code}, system_url) for code in codes_to_validate):
        return {"resource": resource, "status": "Invalid Code"}

    for value in values_to_validate:
        codes_with_unit_requirements = [c["code"] for c in value["code"]["coding"]
                                        if c["code"] in vitals_code_lookup]

        for code_with_unit_requirement in codes_with_unit_requirements:

            required_code_list = vitals_code_lookup[code_with_unit_requirement]

            if not value["valueQuantity"]["code"] in required_code_list:
                return {"resource": resource, "status": "Mismatched vital unit and vital type"}

    return None


@then(u'Proper UCUM codes ({system_url}) are used if {field_name} is present.')
def step_impl(context, system_url, field_name):
    if not StepDecider(context).should_run_test():
        return

    path = field_name.split('.')
    filter_type = path.pop(0)
    resources = get_resources(context.response.json(), filter_type)

    bad_resource_results = []

    for res in resources:
        if ArgonautObservationDecider(res).should_validate():
            found = utils.traverse(res, path)

            if found:
                vital_validation_status = vital_unit_validation(field_name, res, system_url)

                if vital_validation_status:
                    bad_resource_results.append(vital_validation_status)

    assert len(bad_resource_results) == 0, utils.bad_response_assert_with_resource(
        response=context.response,
        message=ERROR_UCUM_CODES,
        resource=bad_resource_results,
        field_name=field_name)
