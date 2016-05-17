# pylint: disable=missing-docstring
import configparser
from flask import request, session


def get_config(default='smart'):
    config = configparser.ConfigParser()

    try:
        vendor = request.form.get('vendor', default).lower()
        config.read('behave.ini.dist-' + vendor)

        config['auth']['refresh_token'] = session.get('refresh_token', '')
    except RuntimeError:
        config.read('behave.ini')

    return config
