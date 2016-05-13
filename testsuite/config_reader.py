# pylint: disable=missing-docstring
import configparser
from flask import request


def get_config(ini_file):
    config = configparser.ConfigParser()

    try:
        config.read_string(ini_file)
    except RuntimeError:
        config.read('behave.ini')

    return config
