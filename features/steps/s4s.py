# pylint: disable=missing-docstring,function-redefined
import json
import re

from behave import given, then, when, register_type
import parse
import requests

from features.steps import utils
from flask import current_app

ERROR_MISSING_CONFORMANCE_STATEMENT = '''
Could not load conformance statement.
'''
ERROR_UNSUPPORTED_RESOURCE = '''
Resource "{0}" not found in conformance statement.
'''
ERROR_VALIDATION_ISSUES = '''
Resource failed to validate.

{issues}
'''
MU_CCDS_MAPPINGS = {
    'Server metadata': 'metadata',
    'Patient demographics': 'Patient/{patientId}',
    'Smoking status': 'Observation?category=social-history&patient={patientId}',
    'Problems': 'Condition?patient={patientId}',
    'Lab results': 'Observation?category=laboratory&patient={patientId}',
    'Medication orders': 'MedicationOrder?patient={patientId}',
    'Medication requests': 'MedicationRequest?patient={patientId}',
    'Medication statements': 'MedicationStatement?patient={patientId}',
    'Medication dispensations': 'MedicationDispense?patient={patientId}',
    'Medication administrations': 'MedicationAdministration?patient={patientId}',
    'Allergies and intolerances': 'AllergyIntolerance?patient={patientId}',
    'Vital signs': 'Observation?category=vital-signs&patient={patientId}',
    'Procedures': 'Procedure?patient={patientId}',
    'Immunizations': 'Immunization?patient={patientId}',
    'Patient documents': 'DocumentReference?patient={patientId}',
    'Coverage': 'Coverage?beneficiary={patientId}',
    'Explanation of benefit': 'ExplanationOfBenefit?patient={patientId}',
}


@parse.with_pattern(r'|'.join(MU_CCDS_MAPPINGS))
def parse_mu_ccds_mapping(mu_ccds):
    return MU_CCDS_MAPPINGS[mu_ccds]
register_type(MU_CCDS=parse_mu_ccds_mapping)


@given('I have a valid conformance statement')
def step_impl(context):
    assert context.conformance is not None, \
        ERROR_MISSING_CONFORMANCE_STATEMENT


@given('this server supports {mu_ccds_query:MU_CCDS}')
def step_impl(context, mu_ccds_query):
    # If there is no conformance statement, assume this resource is supported
    if context.conformance is None:
        return

    # The resourceType is the first block before a "/" or a "?"
    resource_type = re.split(r'[/?]', mu_ccds_query)[0]

    # Get the 'server' rest block from the conformance statement.
    # If there isn't one, it's probably fine to just error out here.
    rest = [rest for rest
            in context.conformance.get('rest', [])
            if rest['mode'] == 'server'][0]

    # Get all the resources with the right type.
    resources = [resource for resource
                 in rest.get('resource', [])
                 if resource['type'] == resource_type]

    assert len(resources) > 0, \
        ERROR_UNSUPPORTED_RESOURCE.format(resource_type)


@given('this server supports at least one of')
def step_impl(context):
    # If there is no conformance statement, assume this resource is supported
    if context.conformance is None:
        return

    # The resourceType is the first block before a "/" or a "?"
    resource_types = [re.split(r'[/?]', MU_CCDS_MAPPINGS[resource['type']])[0]
                      for resource in context.table]

    # Get the 'server' rest block from the conformance statement.
    # If there isn't one, it's probably fine to just error out here.
    rest = [rest for rest
            in context.conformance.get('rest', [])
            if rest['mode'] == 'server'][0]

    # Get all the resources with the right types.
    resources = [resource for resource
                 in rest.get('resource', [])
                 if resource['type'] in resource_types]

    assert len(resources) > 0, \
        ERROR_UNSUPPORTED_RESOURCE.format(', '.join(resource_types))


@when('I request {mu_ccds_query:MU_CCDS}')
def step_impl(context, mu_ccds_query):
    query = mu_ccds_query.format(patientId=context.vendor_config['api'].get('patient'))
    response = utils.get_resource(context, query)

    context.response = response


@given('I have a {mu_ccds_query:MU_CCDS} response')
def step_impl(context, mu_ccds_query):
    query = mu_ccds_query.format(patientId=context.vendor_config['api'].get('patient'))

    assert context.response is not None, \
        'Missing response.'

    context.execute_steps('then the response code should be 200')

    assert query in context.response.request.url, \
        'Missing {query}'.format(query=query)


@then('the resource parses as valid FHIR {version_name} content')
def step_impl(context, version_name):

    resource = context.response.json()

    assert "resourceType" in resource, \
        "Resource has no resourceType: {res}".format(res=resource)

    server_config_key = "API_SERVER_{server_version}".format(server_version=version_name)

    assert server_config_key in current_app.config, \
        "No API Server configured for this version ({v}).".format(v=version_name)

    url = "{url}/{resource}/$validate".format(
        url=current_app.config[server_config_key],
        resource=resource['resourceType'],
    )

    headers = {
        'Authorization': 'Bearer {0}'.format(context.oauth.access_token),
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate,sdch',
    }
    try:
        resp = requests.post(url, json=resource, headers=headers)
    except requests.exceptions.ConnectionError as err:
        return context.scenario.skip(reason=str(err))

    outcome = resp.json()

    issues = [issue for issue in outcome.get('issue')
              if issue.get('severity') == 'error']

    assert not issues, \
        utils.bad_response_assert(context.response,
                                  ERROR_VALIDATION_ISSUES,
                                  issues=json.dumps(issues, indent=4))
