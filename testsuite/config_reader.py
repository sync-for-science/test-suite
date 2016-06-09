# pylint: disable=missing-docstring
import os

from flask import request, session
import yaml


def get_config(default='smart'):

    try:
        vendor = request.form.get('vendor', default).lower()
    except RuntimeError:
        vendor = os.getenv('VENDOR', 'smart')

    with open('config/' + vendor + '.yml') as handle:
        config = yaml.load(handle)

    try:
        authorization = session.get('authorizations', {}).get(vendor, {})
        config['api']['patient'] = authorization.get('patient', config['api'].get('patient'))
    except RuntimeError:
        pass

    host = os.getenv('LETSENCRYPT_HOST')
    if host is not None:
        config['host'] = 'https://' + host
    else:
        host = os.getenv('VIRTUAL_HOST', 'localhost:9003')
        config['host'] = 'http://' + host

    config['auth']['redirect_uri'] = config['host'] + '/authorized/'

    return config
