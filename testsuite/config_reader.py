# pylint: disable=missing-docstring
import os

from flask import request, session
import yaml


def get_config(default='smart'):

    try:
        vendor = request.form.get('vendor', default).lower()
    except RuntimeError:
        vendor = 'smart'

    with open('config/' + vendor + '.yml') as handle:
        config = yaml.load(handle)

    try:
        config['auth']['refresh_token'] = session.get('refresh_token', '')
    except RuntimeError:
        pass

    host = os.getenv('LETSENCRYPT_HOST')
    if host is not None:
        config['auth']['redirect_uri'] = 'https://' + host + '/authorized/'
    else:
        config['auth']['redirect_uri'] = 'http://' + os.getenv('VIRTUAL_HOST') + '/authorized/'

    return config
