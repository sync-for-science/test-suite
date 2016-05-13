# pylint: disable=missing-docstring
from flask import Flask, render_template, request
import json
from flask_socketio import SocketIO
from behave.formatter.base import Formatter
from behave.formatter.json import PrettyJSONFormatter
from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.runner import Runner
import io
import time
import flask_socketio
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading

# Use web sockets:
# from gevent import monkey
# monkey.patch_all()
# async_mode = 'gevent'

# Use long polling
async_mode = 'threading'

app = Flask(__name__)  # pylint: disable=invalid-name
socketio = SocketIO(app, async_mode=async_mode)

@socketio.on('connect')
def got_connect():
    print("Got client connect")
    socketio.emit("did connect")


@socketio.on('testme')
def test_connect(json):
    room = json['room']
    join_room(room)
    config = Configuration(
        update_interval = 0.25,
        on_snapshot=lambda s: flask_socketio.emit('result', s, room=room),
        ini_file=json['ini'],
        outputs=[StreamOpener(stream=io.StringIO())],
        format=['json.chunked'])
    runner = Runner(config)
    runner.run()
    leave_room(room)

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


class ChunkedJsonFormatter(PrettyJSONFormatter):
    def __init__(self, a, b):
        super(ChunkedJsonFormatter, self).__init__(a,b)
        self.snapshot = []
        self.last_update_time = 0
        self.update_interval = 0.2
        if 'update_interval' in self.config.defaults:
            self.update_interval = self.config.defaults['update_interval']
    def result(self, result):
        if len(self.snapshot) > 0 and \
            self.snapshot[-1]['name'] == self.current_feature_data['name']:
            self.snapshot[-1] = self.current_feature_data
        else:
            self.snapshot.append(self.current_feature_data)
        now = time.time()
        if (now - self.last_update_time) > self.update_interval:
            self.config.defaults['on_snapshot'](self.snapshot)
            self.last_update_time = now
        super(ChunkedJsonFormatter, self).result(result)

@app.route('/authorized/')
def authorized():
    from flask import jsonify
    return jsonify(request.args)

@app.route('/launch/')
def launch():
    return render_template('launch.html')

if __name__ == "__main__":
    app.config['FLASK_LOG_LEVEL'] = 'DEBUG'
    socketio.run(app, host='0.0.0.0')
