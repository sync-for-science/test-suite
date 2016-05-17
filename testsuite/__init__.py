# pylint: disable=missing-docstring
from flask import Flask, render_template, request
app = Flask(__name__)  # pylint: disable=invalid-name


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/tests.json', methods=['POST'])
def tests():
    from behave.configuration import Configuration
    from behave.formatter.base import StreamOpener
    from behave.runner import Runner
    import io

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
    from flask import jsonify, session, redirect
    from testsuite.fhir import get_oauth_uris
    from testsuite import config_reader
    import requests
    from testsuite.oauth import RefreshTokenStrategy

    config = config_reader.get_config(session['vendor'])
    uris = get_oauth_uris(config['api']['url'])
    strategy = RefreshTokenStrategy(
        client_id=config['auth']['client_id'],
        client_secret=config['auth']['client_secret'],
        redirect_uri=config['auth']['redirect_uri'],
        urls=uris,
        refresh_token=config['auth']['refresh_token'],
        basic=config['auth'].get('basic', False)
    )
    strategy.upgrade_authorization_code(request.args.get('code'))

    session['refresh_token'] = strategy.refresh_token

    return redirect('/')


@app.route('/authorize/', methods=['POST'])
def authorize():
    from flask import redirect, jsonify, session
    from urllib.parse import urlencode
    import uuid

    from testsuite.fhir import get_oauth_uris
    from testsuite import config_reader

    config = config_reader.get_config()
    uris = get_oauth_uris(config['api']['url'])
    state = uuid.uuid4()

    params = {
        'response_type': 'code',
        'client_id': config['auth']['client_id'],
        'redirect_uri': config['auth']['redirect_uri'],
        'scope': config['auth']['scope'],
        'state': state,
        'aud': config['api']['url'],
    }
    if config['auth']['launch']:
        params['launch'] = config['auth']['launch']
    authorize_url = uris['authorize'] + '?' + urlencode(params)
    print(authorize_url)

    session['vendor'] = request.form['vendor']
    session['state'] = state

    return redirect(authorize_url)


@app.route('/launch/', methods=['POST', 'GET'])
def launch():
    return render_template('launch.html')


@app.route('/launch/epic/', methods=['POST', 'GET'])
def launch_epic():
    from testsuite import config_reader

    config = config_reader.get_config('epic')
    return render_template('launch.html', config=config)


@app.route('/launch/cerner/', methods=['POST', 'GET'])
def launch_cerner():
    from testsuite import config_reader
    config = config_reader.get_config('cerner')
    return render_template('launch.html', config=config)

app.secret_key = 'ssssssssssh'
app.config['FLASK_LOG_LEVEL'] = 'DEBUG'
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
