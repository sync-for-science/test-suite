''' The application.
'''
import os

from flask import Flask
import grequests
import requests



ASYNC_MODE = 'gevent'
PING_INTERVAL = 59


# Create and configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def create_app():
    ''' The application factory.
    '''
    from testsuite import (
        extensions,
        views,
    )

    # Init extensions
    extensions.db.init_app(app)
    extensions.socketio.init_app(
        app,
        async_mode=ASYNC_MODE,
        ping_interval=PING_INTERVAL,
        message_queue='redis://'
    )

    return app
