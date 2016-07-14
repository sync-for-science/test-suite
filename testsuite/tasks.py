# pylint: disable=missing-docstring
import io

from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.runner import Runner
from celery import Celery
import flask_socketio


app = Celery()
app.config_from_object('testsuite.celeryconfig')
socketio = flask_socketio.SocketIO(message_queue='redis://')


@app.task
def run_tests(room, vendor, tags, override):

    def on_snapshot(snapshot, plan):
        event = {
            'snapshot': snapshot,
            'plan': plan,
        }
        socketio.emit('snapshot', event, room=room)

    try:
        output = io.StringIO()
        output_stream = StreamOpener(stream=output)
        config = Configuration(
            outputs=[output_stream],
            format=['json.chunked'],
            on_snapshot=on_snapshot,
            vendor=vendor,
            override=override,
            command_args=[],
            tags=[','.join(tags)],
        )
        runner = Runner(config)

        runner.run()
    except Exception as err:  # pylint: disable=broad-except
        socketio.emit('global_error', str(err), room=room)
    finally:
        socketio.emit('tests_complete', room=room)
