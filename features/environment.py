# pylint: disable=missing-docstring,unused-argument
import copy
import logging
import os
import pickle
import uuid

import redis

from features.steps import oauth, utils
from testsuite import fhir
from testsuite.config_reader import get_config
from testsuite.oauth import authorize, factory


CACHE_TTL = 60 * 60  # 1 hour
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
    override = getattr(context.config, 'override', os.getenv('CONFIG_OVERRIDE', ''))
    vendor_config = get_config(vendor.lower(), override)
    vendor_config['auth']['aud'] = vendor_config['api']['url']
    context.vendor_config = copy.deepcopy(vendor_config)

    # Filter out any tagged vendor config steps
    steps = vendor_config['auth'].get('steps', [])
    steps = [step for step in steps if 'when' not in step]
    vendor_config['auth']['steps'] = steps

    # Set the ElasticSearch logging endpoint
    context.config.es_url = os.getenv('ES_URL')

    # Authorize against the vendor FHIR server.
    try:
        context.oauth = factory(vendor_config)
        context.oauth.authorize()
        if getattr(context.oauth, 'patient', None) is not None:
            context.vendor_config['api']['patient'] = context.oauth.patient
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
        context.conformance = fhir.get_conformance_statement(vendor_config['api']['url'])
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
