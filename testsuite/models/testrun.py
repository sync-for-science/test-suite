''' Test run module.
'''
import json
import uuid
import datetime

from testsuite.extensions import db


class TestRun(db.Model):
    ''' The results of a single test run.
    '''
    _id = db.Column('id', db.String, primary_key=True)
    date_ran = db.Column('date_ran', db.Text)
    vendor = db.Column('vendor', db.Text)
    tags = db.Column('tags', db.Text)

    snapshot = db.relationship('Snapshot',
                               uselist=False,
                               cascade='all, delete, delete-orphan')
    plan = db.relationship('Plan',
                           uselist=False,
                           cascade='all, delete, delete-orphan')

    def __init__(self, vendor, tags):
        self._id = str(uuid.uuid4())
        self.date_ran = str(datetime.datetime.now())
        self.vendor = vendor
        self.tags = ",".join(tags)

    @property
    def event(self):
        ''' Properly formatted test run event.
        '''
        return {
            'report_id': self._id,
            'snapshot': self.snapshot.state,
            'plan': self.plan.state,
        }

    @property
    def summary(self):
        '''
        Get a summary of the run.
        :return: Dictionary representing snapshot of information about the test run.
        '''

        snapshot = None
        test_run = False

        if self.snapshot:
            snapshot = self.snapshot.state
            test_run = True

        return {
            'report_id': self._id,
            'vendor': self.vendor,
            'snapshot': snapshot,
            'test_run': test_run,
            'date_ran': self.date_ran,
            'tags': self.tags,
        }

    def save_snapshot(self, snapshot, plan):
        ''' Update the latest snapshot from the test run.
        '''
        self.snapshot = Snapshot(self, snapshot)
        self.plan = Plan(self, plan)


class JsonState():
    ''' Base class for objects with json-serialized state.
    '''
    def __init__(self, state):
        self._state = json.dumps(state)

    @property
    def state(self):
        ''' Return the snapshot's state.
        '''
        return json.loads(self._state)


class Snapshot(JsonState, db.Model):
    ''' A snapshot of a test run's current progress.
    '''
    _id = db.Column('id', db.Integer, primary_key=True)

    _test_run_id = db.Column('test_run_id',
                             db.Integer,
                             db.ForeignKey('test_run.id'))
    test_run = db.relationship('TestRun')

    _state = db.Column('state', db.Text)

    def __init__(self, test_run, state):
        self.test_run = test_run
        super().__init__(state)


class Plan(JsonState, db.Model):
    ''' The test run's plan.
    '''
    _id = db.Column('id', db.Integer, primary_key=True)

    _test_run_id = db.Column('test_run_id',
                             db.Integer,
                             db.ForeignKey('test_run.id'))
    test_run = db.relationship('TestRun')

    _state = db.Column('state', db.Text)

    def __init__(self, test_run, state):
        self.test_run = test_run
        super().__init__(state)
