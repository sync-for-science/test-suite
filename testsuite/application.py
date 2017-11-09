''' The application.
'''
import os

from flask import Flask

ASYNC_MODE = 'threading'
PING_INTERVAL = 59


# Create and configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['API_SERVER_DSTU2'] = os.getenv('API_SERVER_DSTU2')
app.config['API_SERVER_STU3'] = os.getenv('API_SERVER_STU3')


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
