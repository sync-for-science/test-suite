# pylint: disable=missing-docstring,unused-variable
import glob
import os

from flask import jsonify, render_template, request, session
from werkzeug import exceptions
import flask_socketio

from testsuite.application import app
from testsuite.extensions import db, socketio
from testsuite.models.testrun import TestRun
from testsuite import tasks


@app.route('/')
def index():
    configs = glob.glob('./config/*.yml')
    names = []
    for config in configs:
        name, ext = os.path.splitext(os.path.basename(config))
        names.append(name.capitalize())

    return render_template('index.html', names=sorted(names))


@app.route('/load-report/<test_run_id>', methods=['POST'])
def report(test_run_id):
    room = request.form['room']
    run = TestRun.query.get(test_run_id)

    try:
        event = run.event
        socketio.emit('snapshot', event, room=room)

        return jsonify(event)
    except AttributeError:
        resp = jsonify({'error': 'Test run {} not found.'.format(test_run_id)})
        resp.status_code = 404

        return resp


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
    tasks.run_tests.delay(room=session['room'],
                          vendor=data.get('vendor'),
                          tags=data.get('tags'),
                          override=data.get('override'))


@app.cli.command()
def initdb():
    ''' Initialize the database.
    '''
    db.create_all()
