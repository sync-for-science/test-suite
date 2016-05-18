# pylint: disable=missing-docstring
from testsuite.config_reader import get_config


def before_all(context):
    config = get_config()

    context.config = config
