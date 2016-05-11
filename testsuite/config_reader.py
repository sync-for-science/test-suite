# pylint: disable=missing-docstring
import configparser
from flask import request


def get_config():
    config = configparser.ConfigParser()

    try:
        config.read_string(request.form['config'])
    except RuntimeError:
        config.read('behave.ini')

    return config
