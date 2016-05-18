# pylint: disable=missing-docstring
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

    return config
