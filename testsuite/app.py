# pylint: disable=missing-docstring
from flask import Flask, render_template, request
app = Flask(__name__)  # pylint: disable=invalid-name


@app.route("/")
def index():
    dist = 'behave.ini.dist'
    if 'vendor' in request.args:
        dist = dist + '-' + request.args['vendor']

    try:
        with open(dist, 'r') as handle:
            defaults = handle.read()
    except FileNotFoundError:
        defaults = ''

    return render_template('index.html', defaults=defaults)


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
    from flask import jsonify
    return jsonify(request.args)

@app.route('/launch/')
def launch():
    return render_template('launch.html')

if __name__ == "__main__":
    app.config['FLASK_LOG_LEVEL'] = 'DEBUG'
    app.run(host='0.0.0.0')
