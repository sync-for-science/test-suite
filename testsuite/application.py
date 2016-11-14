''' The application.
'''
import os

from flask import Flask
from flask_socketio import SocketIO

ASYNC_MODE = 'threading'
PING_INTERVAL = 59


# Create and configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


def create_app():
    ''' The application factory.
    '''
    from testsuite.extensions import socketio
    socketio.init_app(
        app,
        async_mode=ASYNC_MODE,
        ping_interval=PING_INTERVAL,
        message_queue='redis://'
    )

    from testsuite import views

    return app
