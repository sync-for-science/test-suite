# pylint: disable=missing-docstring
''' Tasks module.
'''
import io

from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.runner import Runner
from celery import Celery

from testsuite.application import create_app
from testsuite.extensions import db, socketio
from testsuite.models.testrun import TestRun


# Create and configure celery task runner
celery = Celery()
celery.config_from_object('testsuite.celeryconfig')


@celery.task
def run_tests(room, vendor, tags, override):
    app = create_app()
    with app.app_context():
        test_run = TestRun()
        db.session.add(test_run)
        db.session.commit()

        def on_snapshot(snapshot, plan):
            test_run.save_snapshot(snapshot, plan)
            socketio.emit('snapshot', test_run.event, room=room)

            db.session.commit()

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
            import traceback; traceback.print_exc()
            socketio.emit('global_error', str(err), room=room)
        finally:
            socketio.emit('tests_complete', room=room)
