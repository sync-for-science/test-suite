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


def get_names():
    configs = glob.glob('./config/*.yml')
    names = []
    for config in configs:
        name, ext = os.path.splitext(os.path.basename(config))
        if name == 'Other':
            continue
        names.append(name)

    names.sort(key=lambda x: x.lower())
    return names


@app.route('/')
def index():
    return render_template('index.html', names=get_names())


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


@app.route('/begin-tests')
def headless_begin():
    vendors = get_names()
    for vendor in vendors:
        print("Testing %s" % vendor)
        tasks.run_tests.delay(room='headless-room',
                              vendor=vendor,
                              tags=["allergies-and-intolerances", "immunizations",
                                    "lab-results", "medication-administrations",
                                    "medication-dispensations", "medication-orders",
                                    "medication-statements", "patient-documents",
                                    "patient-demographics", "problems", "procedures",
                                    "smoking-status", "vital-signs", "s4s", "smart",
                                    "ask-authorization", "evaluate-request", "exchange-code",
                                    "use-refresh-token", "revoke-authorization"],
                              override='')

    return jsonify({
        'testing': True,
        'targets': vendors
    })


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
