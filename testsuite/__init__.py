# pylint: disable=missing-docstring
from urllib.parse import urlencode
import io
import uuid

from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.runner import Runner
from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug import exceptions
import requests

from testsuite import config_reader, fhir, oauth


app = Flask(__name__)  # pylint: disable=invalid-name


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/tests.json', methods=['POST'])
def tests():
    output = io.StringIO()
    output_stream = StreamOpener(stream=output)
    config = Configuration(outputs=[output_stream], format=['json.pretty'])
    runner = Runner(config)

    runner.run()

    headers = {
        'Content-type': 'application/json',
    }

    return output.getvalue(), 200, headers


@app.route('/authorized/')
def authorized():
    exceptions.abort(500)


@app.route('/launch/', methods=['POST', 'GET'])
def launch():
    return render_template('launch.html')


@app.route('/launch/epic/', methods=['POST', 'GET'])
def launch_epic():
    config = config_reader.get_config('epic')
    return render_template('launch.html', config=config)


@app.route('/launch/cerner/', methods=['POST', 'GET'])
def launch_cerner():
    config = config_reader.get_config('cerner')
    return render_template('launch.html', config=config)

app.secret_key = 'ssssssssssh'
app.config['FLASK_LOG_LEVEL'] = 'DEBUG'
app.debug = True
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
