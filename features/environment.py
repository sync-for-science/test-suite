# pylint: disable=missing-docstring,unused-argument
import copy
import logging
import os
import pickle
import uuid
import re

import redis

from features.steps import oauth, utils
from testsuite import fhir
from testsuite.config_reader import get_vendor_config, get_env_config
from testsuite.oauth import authorize, factory

CACHE_TTL = 60 * 60  # 1 hour
FHIR_RESOURCE_TAGS = {
    'patient-demographics',
    'smoking-status',
    'problems',
    'medication-orders',
    'medication-requests',
    'medication-statements',
    'medication-dispensations',
    'medication-administrations',
    'allergies-and-intolerances',
    'lab-results',
    'vital-signs',
    'procedures',
    'immunizations',
    'patient-documents',
    'coverage',
    'explanation-of-benefit'
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
    override = getattr(context.config, 'override', os.getenv('CONFIG_OVERRIDE', ''))

    vendor_config = get_vendor_config(vendor, override)

    # Get configuration from the test server's environment.
    env_config = get_env_config()

    # Attempt to retrieve the security URL for this version.
    vendor_config['versioned_auth']['aud'] = vendor_config['versioned_api']['url']

    context.vendor_config = copy.deepcopy(vendor_config)
    context.env_config = copy.deepcopy(env_config)

    # Filter out any tagged vendor config steps
    steps = vendor_config['versioned_auth'].get('steps', [])
    steps = [step for step in steps if 'when' not in step]
    vendor_config['versioned_auth']['steps'] = steps

    # Set the ElasticSearch logging endpoint
    context.config.es_url = os.getenv('ES_URL')

    # Authorize against the vendor FHIR server.
    try:
        context.oauth = factory(vendor_config)
        context.oauth.authorize()
        if getattr(context.oauth, 'patient', None) is not None:
            context.vendor_config['versioned_api']['patient'] = context.oauth.patient
    except AssertionError as error:
        logging.error(utils.bad_response_assert(error.args[0], ''))
        raise Exception(utils.bad_response_assert(error.args[0], ''))
    except authorize.AuthorizationException as err:
        error = oauth.ERROR_SELENIUM_SCREENSHOT.format(
            err.args[0],
            err.args[1],
            err.args[2],
            context.vendor_config['host'],
        )
        raise Exception(error)
    except ValueError as error:
        logging.error(utils.bad_response_assert(error.response, ''))
        raise Exception(utils.bad_response_assert(error.response, ''))

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
        context.conformance = fhir.get_conformance_statement(vendor_config['versioned_auth']['aud'])
    except ValueError as error:
        context.conformance = None
        logging.error(utils.bad_response_assert(error.response, ''))

    # Define a global cache
    context.cache = Cache(redis.StrictRedis())


def before_feature(context, feature):
    """ Configure Feature scope.

    Some features need feature-level resources so that we don't need to
    make a bunch of API requests and slow things down.
    """

    # We handle the with_use_case tag with this custom functionality.
    # Extract which use case this feature is part of and determine
    # if we need to run it. Store use_case in the feature object for use
    # by child scenarios.
    feature.use_case = None
    skip_use_case = True

    for tag in feature.tags:
        use_case_matches = re.match("use.with_use_case=(.*)", tag)
        version_matches = re.match("use.with_version=(.*)", tag)

        if use_case_matches and feature.use_case is None:
            use_case = use_case_matches.groups()[0]

            if use_case in context.vendor_config["use_cases"]:
                feature.use_case = use_case
                skip_use_case = False

        if version_matches and feature.use_case:
            version = version_matches.groups()[0]

            if version != context.vendor_config["use_cases"][feature.use_case]:
                feature.skip("Feature version (%s) not supported in this use case (%s)."
                             % (version, use_case))

    if skip_use_case:
        feature.skip("Feature (%s) not in any use case." % feature.name)
        return

    try:
        ignored_steps = context.vendor_config["ignored_steps"][feature.location.filename]

        for step in ignored_steps:
            if step == "all":
                feature.skip("Feature (%s) requested skip by vendor." % feature.name)

    except KeyError:
        pass

    tags = list(FHIR_RESOURCE_TAGS.intersection(feature.tags))

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


def before_scenario(context, scenario):
    # The skipping logic here only applies when a use case has been defined on this feature.
    if scenario.feature.use_case:
        use_case_version = context.vendor_config["use_cases"][scenario.feature.use_case]

        # Skip the scenario if its version doesn't much the use_case version.
        for tag in scenario.effective_tags:
            matches = re.match("use.with_version=(.*)", tag)
            if matches and matches.groups()[0] != use_case_version:
                scenario.skip("Scenario's version (%s) not in Use Case (%s)."
                              % (matches.groups()[0], scenario.feature.use_case))


def before_step(context, step):

    context.vendor_skip = False

    try:
        ignored_steps = context.vendor_config["ignored_steps"][step.location.filename]

        for ignored_step in ignored_steps:
            if step.name == ignored_step:
                context.vendor_skip = True
                break
    except KeyError:
        pass


class Cache(object):
    """ A minimal caching layer.
    """
    def __init__(self, redis_client):
        self.redis_client = redis_client
        # A unique prefix ensures that each test run does not share a cache.
        self.prefix = 'cache-{0}-'.format(uuid.uuid4())

    def __getitem__(self, key):
        key = self.prefix + key
        return pickle.loads(self.redis_client.get(key))

    def __setitem__(self, key, value):
        key = self.prefix + key
        self.redis_client.setex(key,
                                CACHE_TTL,
                                pickle.dumps(value))

    def __contains__(self, key):
        key = self.prefix + key
        return self.redis_client.exists(key)

    def clear(self):
        pattern = self.prefix + '*'
        keys = self.redis_client.keys(pattern)
        if keys:
            deleted = self.redis_client.delete(*keys)
            logging.info('Deleted %d records from cache.', deleted)
