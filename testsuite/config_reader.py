# pylint: disable=missing-docstring
import os

import yaml


def get_config(vendor):
    vendor = os.getenv('VENDOR', vendor).lower()

    with open('config/' + vendor + '.yml') as handle:
        config = yaml.load(handle)

    host = os.getenv('LETSENCRYPT_HOST')
    if host is not None:
        config['host'] = 'https://' + host
    else:
        host = os.getenv('VIRTUAL_HOST', 'localhost:9003')
        config['host'] = 'http://' + host

    config['auth']['redirect_uri'] = config['host'] + '/authorized/'

    return config
