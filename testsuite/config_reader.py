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
        config['auth']['refresh_token'] = authorization.get('refresh_token')
        config['api']['patient'] = authorization.get('patient', config['api']['patient'])
    except RuntimeError:
        pass

    host = os.getenv('LETSENCRYPT_HOST')
    if host is not None:
        config['auth']['redirect_uri'] = 'https://' + host + '/authorized/'
    else:
        host = os.getenv('VIRTUAL_HOST', 'localhost:9003')
        config['auth']['redirect_uri'] = 'http://' + host + '/authorized/'

    return config
