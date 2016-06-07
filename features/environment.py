# pylint: disable=missing-docstring,unused-argument
from testsuite.config_reader import get_config


def before_all(context):
    config = get_config()

    context.config = config


def before_feature(context, feature):
    """ Configure Feature scope.

    Some features need feature-level resources so that we don't need to
    make a bunch of API requests and slow things down.
    """

    if 'patient' in feature.tags:
        steps = [
            'Given I am authorized',
            'And I am logged in',
            'When I request Patient demographics',
        ]
        context.execute_steps('\n'.join(steps))
