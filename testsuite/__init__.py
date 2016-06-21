# pylint: disable=missing-docstring
""" Test suite module.
"""
from flask import Flask
import flask_socketio

from testsuite import views


ASYNC_MODE = 'threading'
PING_INTERVAL = 59


def main():
    app = Flask(__name__)
    socketio = flask_socketio.SocketIO(
        app,
        async_mode=ASYNC_MODE,
        ping_interval=PING_INTERVAL,
        message_queue='redis://'
    )

    views.configure_views(app=app, socketio=socketio)

    app.secret_key = 'ssssssssssh'
    app.config['FLASK_LOG_LEVEL'] = 'DEBUG'

    return app, socketio
