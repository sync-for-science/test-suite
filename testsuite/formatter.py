""" Custom Behave formatter.
"""
from behave.formatter.json import PrettyJSONFormatter
import six


class ChunkedJsonFormatter(PrettyJSONFormatter):
    """ Return JSON in chunks so we can use it with websockets.
    """
    split_text_into_lines = False

    def __init__(self, a, b):
        super(ChunkedJsonFormatter, self).__init__(a, b)
        self.snapshot = []
        self.plan = None

    def update_status_data(self):
        super(ChunkedJsonFormatter, self).update_status_data()

        if self.plan is None:
            self.plan = self.config.plan

        # Make sure that tags are strings, behave.model.Tag can break
        # serialization downstream.
        current_feature = self.current_feature_data
        current_feature['tags'] = [str(tag) for tag in current_feature['tags']]

        # Skip reasons must be checked after the tests have run
        element = None
        for element in current_feature['elements']:
            element['tags'] = [str(tag) for tag in element['tags']]
            if 'skip_reason' in element:
                element['skip_reason'] = element['skip_reason']()
            if 'systems' in element:
                element['systems'] = element['systems']()

        # If the entire feature has been skipped, populate the skip_reason
        if current_feature['status'] == 'skipped' and element:
            current_feature['skip_reason'] = element['skip_reason']

        self.snapshot.append(current_feature)
        self.config.on_snapshot(self.snapshot, self.plan)

    def scenario(self, scenario):
        element = self.add_feature_element({
            'type': 'scenario',
            'keyword': scenario.keyword,
            'name': scenario.name,
            'tags': scenario.tags,
            'location': six.text_type(scenario.location),
            'steps': [],
            'skip_reason': lambda: getattr(scenario, 'skip_reason'),
            'systems': lambda: getattr(scenario, 'systems', []),
        })
        if scenario.description:
            element['description'] = scenario.description
        self._step_index = 0
