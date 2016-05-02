from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    with open('behave.ini.dist', 'r') as handle:
        defaults = handle.read()

    return render_template('index.html', defaults=defaults)

@app.route('/tests.json', methods=['POST'])
def tests():
    from behave.configuration import Configuration
    from behave.formatter.base import StreamOpener
    from behave.runner import Runner
    import io

    output = io.StringIO()
    so = StreamOpener(stream=output)
    config = Configuration(outputs=[so], format=['json.pretty'])
    runner = Runner(config)

    failed = runner.run()

    headers = {
        'Content-type': 'application/json',
    }

    return output.getvalue(), 200, headers

if __name__ == "__main__":
    app.run(host='0.0.0.0')
