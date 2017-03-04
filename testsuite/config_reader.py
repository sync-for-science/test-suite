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


def get_config(vendor, override=''):
    vendor_file = os.path.basename(vendor + '.yml')
    vendor_path = os.path.join('config', vendor_file)
    with open(vendor_path) as handle:
        config = yaml.load(handle)

    if override:
        config = deep_merge(config, yaml.safe_load(override))

    host = os.getenv('BASE_URL')
    config['auth']['redirect_uri'] = config['host'] + '/authorized/'

    return config
