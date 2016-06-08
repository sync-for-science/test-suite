# pylint: disable=missing-docstring,unused-argument
from testsuite.config_reader import get_config


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
    config = get_config()

    context.config = config


def before_feature(context, feature):
    """ Configure Feature scope.

    Some features need feature-level resources so that we don't need to
    make a bunch of API requests and slow things down.
    """
    tags = list(CCDS_TAGS.intersection(feature.tags))

    if len(tags) > 1:
        raise Exception('Too many tags', tags)

    if len(tags) == 1:
        ccds_type = tags[0].capitalize().replace('-', ' ')
        steps = [
            'Given I am authorized',
            'And I am logged in',
            'When I request {ccds_type}'.format(ccds_type=ccds_type),
        ]
        try:
            context.execute_steps('\n'.join(steps))
        except AssertionError as error:
            feature.skip(error.args[0])
