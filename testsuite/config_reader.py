# pylint: disable=missing-docstring
import os

import yaml


def deep_merge(orig, new):
    """ Recursively create a new dictionary from the values of orig and new.
    """
    if isinstance(orig, dict) and isinstance(new, dict):
        for key, val in new.items():
            if key not in orig:
                orig[key] = val
            else:
                orig[key] = deep_merge(orig[key], val)
        return orig
    else:
        return new


def get_vendor_config(vendor, override=''):
    vendor_file = os.path.basename(vendor + '.yml')
    vendor_path = os.path.join('config', vendor_file)
    with open(vendor_path) as handle:
        config = yaml.load(handle)

    if override:
        config = deep_merge(config, yaml.safe_load(override))

    config['host'] = os.getenv('BASE_URL', 'http://localhost:9003')
    config['auth']['redirect_uri'] = config['host'] + '/authorized/'
    config['auth']['redirect_uri'] = "http://referencestackdocker_tests_1:5000" + '/authorized/'

    return config


def get_env_config():
    """
    Get the environment variables response for which server we validate the FHIR Resources against.    
    :return: Dictionary with URI.
    """
    config = {
                "API_SERVER_DSTU2": os.getenv('API_SERVER_DSTU2'),
                "API_SERVER_STU3": os.getenv('API_SERVER_STU3')
             }

    return config
