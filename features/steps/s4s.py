# pylint: disable=missing-docstring
from behave import when, register_type
import parse
from features.steps import utils


MU_CCDS_MAPPINGS = {
    'Server metadata': 'metadata',
    'Patient demographics': 'Patient/{patientId}',
    'Smoking status': 'Observation?category=social-history&patient={patientId}',
    'Problems': 'Condition?patient={patientId}',
    'Lab results': 'Observation?category=laboratory&patient={patientId}',
    'Medication orders': 'MedicationOrder?patient={patientId}',
    'Medication statements': 'MedicationStatement?patient={patientId}',
    'Medication dispensations': 'MedicationDispense?patient={patientId}',
    'Medication administrations': 'MedicationAdministration?patient={patientId}',
    'Allergies and intolerances': 'AllergyIntolerance?patient={patientId}',
    'Vital signs': 'Observation?category=vital-signs&patient={patientId}',
    'Procedures': 'Procedure?patient={patientId}',
    'Immunizations': 'Immunization?patient={patientId}',
    'Patient documents': 'DocumentReference?patient={patientId}',
}


@parse.with_pattern(r"|".join(MU_CCDS_MAPPINGS))
def parse_mu_ccds_mapping(mu_ccds):
    return MU_CCDS_MAPPINGS[mu_ccds]
register_type(MU_CCDS=parse_mu_ccds_mapping)


@when('I request {mu_ccds_query:MU_CCDS}')
def step_impl(context, mu_ccds_query):
    query = mu_ccds_query.format(patientId=context.config['api']['patient'])
    response = utils.get_resource(context, query)

    context.response = response
