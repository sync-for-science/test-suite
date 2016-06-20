# pylint: disable=missing-docstring,unused-argument
import logging
import os

from features.steps import utils
from testsuite import fhir
from testsuite.config_reader import get_config
from testsuite.oauth import factory


CCDS_TAGS = {
    'patient-demographics',
    'smoking-status',
    'problems',
    'medication-orders',
    'medication-statements',
    'medication-dispensations',
    'medication-administrations',
    'allergies-and-intolerances',
    'lab-results',
    'vital-signs',
    'procedures',
    'immunizations',
    'patient-documents',
}


def before_all(context):
    """ Runs once before all tests.

    Set up some global state necessary to the tests and test runner.

    * Get the vendor config and attach it to the context.
    * Authorize against the vendor FHIR server and store the authorization.
    * Get the test plan so that we can show a progress meter.
    * Load the conformance statement so we know which resources are supported.
    """
    # Get the vendor config and attach it to the context.
    vendor = getattr(context.config, 'vendor', os.getenv('VENDOR'))
    vendor_config = get_config(vendor.lower())
    context.vendor_config = vendor_config

    # Authorize against the vendor FHIR server.
    context.oauth = factory(vendor_config)
    try:
        context.oauth.authorize()
        if getattr(context.oauth, 'patient', None) is not None:
            vendor_config['api']['patient'] = context.oauth.patient
    except AssertionError as error:
        logging.error(utils.bad_response_assert(error.args[0], ''))

    # Get the test plan so that we can show a progress meter.
    context.config.plan = []
    # There is no other way to get a feature list from the context.
    # Since this is for display purposes only, this should be safe.
    features = context._runner.features  # pylint: disable=protected-access
    for feature in features:
        scenariolist = []
        context.config.plan.append({
            'name': feature.name,
            'location': str(feature.location),
            'scenarios': scenariolist})
        for scenario in feature.scenarios:
            scenariolist.append({
                'name': scenario.name,
                'location': str(scenario.location)})

    # Download the conformance statement
    try:
        context.conformance = fhir.get_conformance_statement(vendor_config['api']['url'])
    except ValueError as error:
        context.conformance = None
        logging.error(utils.bad_response_assert(error.response, ''))


def before_feature(context, feature):
    """ Configure Feature scope.

    Some features need feature-level resources so that we don't need to
    make a bunch of API requests and slow things down.
    """
    tags = list(CCDS_TAGS.intersection(feature.tags))

    if len(tags) > 1:
        raise Exception('Too many CCDS tags', tags)

    if len(tags) == 1:
        ccds_type = tags[0].capitalize().replace('-', ' ')
        steps = [
            'Given I am logged in',
            'And this server supports {0}'.format(ccds_type),
            'When I request {0}'.format(ccds_type),
        ]
        try:
            context.execute_steps('\n'.join(steps))
        except AssertionError as error:
            feature.skip(error.args[0])
