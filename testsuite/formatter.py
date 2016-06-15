""" Custom Behave formatter.
"""
from behave.formatter.json import PrettyJSONFormatter


class ChunkedJsonFormatter(PrettyJSONFormatter):
    """ Return JSON in chunks so we can use it with websockets.
    """
    def __init__(self, a, b):
        super(ChunkedJsonFormatter, self).__init__(a, b)
        self.snapshot = []

    def update_status_data(self):
        super(ChunkedJsonFormatter, self).update_status_data()

        self.snapshot.append(self.current_feature_data)
        self.config.on_snapshot(self.snapshot)
