# pylint: disable=missing-docstring,unused-variable
from flask import render_template, session
from werkzeug import exceptions
import flask_socketio

from testsuite import tasks


def configure_views(app, socketio):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/authorized/')
    def authorized():
        exceptions.abort(500)

    @socketio.on('connect')
    def cb_handle_connect():
        flask_socketio.send('connected')

    @socketio.on('message')
    def cb_handle_message(message):
        flask_socketio.send('message received!')

    @socketio.on('join')
    def cb_handle_join(room):
        session['room'] = room
        flask_socketio.join_room(room)

    @socketio.on('begin_tests')
    def cb_handle_begin_tests(data):
        async = tasks.run_tests.delay(room=session['room'],
                                      vendor=data.get('vendor'),
                                      tags=data.get('tags'),
                                      override=data.get('override'))
