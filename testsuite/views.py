# pylint: disable=missing-docstring,unused-variable
import glob
import os

from flask import jsonify, render_template, request, session, current_app
from werkzeug import exceptions
import flask_socketio

import click

from testsuite.application import app
from testsuite.extensions import db, socketio
from testsuite.models.testrun import TestRun
from testsuite import tasks

import requests
import os.path

BLOOM_FILE = './data/codes.bf'

ALL_TAGS = ["allergies-and-intolerances", "immunizations",
            "lab-results", "medication-administrations",
            "medication-dispensations", "medication-requests",
            "medication-orders",
            "medication-statements", "patient-documents",
            "patient-demographics", "problems", "procedures",
            "smoking-status", "vital-signs", "s4s", "smart",
            "ask-authorization", "evaluate-request", "exchange-code",
            "use-refresh-token", "revoke-authorization"]


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


@app.route('/load-text-report/<test_run_id>', methods=['GET'])
def text_report(test_run_id):
    run = TestRun.query.get(test_run_id)

    return render_template('individual_report.txt', run=run), {'Content-Type': 'text/plain'}


@app.route('/begin-tests')
def headless_begin():
    vendors = get_names()
    for vendor in vendors:
        print("Testing %s" % vendor)
        tasks.run_tests.delay(room='headless-room',
                              vendor=vendor,
                              tags=ALL_TAGS,
                              override='')

    return jsonify({
        'testing': True,
        'targets': vendors
    })


@app.route('/begin-test/<single_vendor>', methods=['GET'])
def headless_begin_single(single_vendor):

    print("Testing %s" % single_vendor)
    tasks.run_tests.delay(room='headless-room',
                          vendor=single_vendor,
                          tags=ALL_TAGS,
                          override='')

    return jsonify({
        'testing': True,
        'target': single_vendor
    })


@app.route('/authorized/')
def authorized():
    exceptions.abort(500)


@app.route('/health_summary')
def health_summary():

    latest_results = {}
    vendors = get_names()

    for vendor in vendors:
        last_test = TestRun.query.filter_by(vendor=vendor)\
            .order_by(TestRun.date_ran.desc()).first()
        if last_test is not None:
            latest_results[vendor] = last_test.summary
        else:
            latest_results[vendor] = None

    return render_template('health_summary.html', vendors=vendors, latest_results=latest_results)


@app.route('/update_bloom_filter', methods=['POST'])
def update_bloom_filter_endpoint():
    return jsonify(update_bloom_filter())


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


def update_bloom_filter():
    bloom_file_status = {}

    try:
        r = requests.get(current_app.config['BLOOM_FILTER_URL'])
        r.raise_for_status()

        with open(BLOOM_FILE, 'wb') as f:
            f.write(r.content)

    except requests.exceptions.RequestException as e:
        bloom_file_status['error'] = "Error requesting Bloom Filter -- %s" % str(e)
    except IOError as e:
        bloom_file_status['error'] = "Error writing Bloom Filter File -- %s" % str(e)

    bloom_file_status['bloom_in_place'] = os.path.isfile(BLOOM_FILE)

    return bloom_file_status


@app.cli.command(help='Download the Bloom filter (does not overwrite by default)')
@click.option('--force', '-f', is_flag=True, help='overwrite existing Bloom filter')
def get_bloom_filter(force):
    if force or not os.path.isfile(BLOOM_FILE):
        update_bloom_filter()
