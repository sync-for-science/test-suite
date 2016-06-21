# pylint: disable=missing-docstring, unused-variable
from flask import render_template, request
from werkzeug import exceptions
import flask_socketio

from testsuite import tasks


def configure_views(app, socketio):

    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('connect')
    def got_connect():
        flask_socketio.send('connected')

    @socketio.on('message')
    def cb_handle_message(message):
        flask_socketio.send('message received!')

    @socketio.on('begin_tests')
    def tests(data):
        async = tasks.run_tests.delay(request.sid, data.get('vendor'))

    @app.route('/authorized/')
    def authorized():
        exceptions.abort(500)
