""" Do nothing.
"""
from . import base


class NoneAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the No-op authorization path.
    """
    def _launch_step(self):
        pass

    def _vendor_step(self):
        pass

    def _get_authorization(self):
        pass

    def _browser(self):
        pass

    def open(self):
        pass

    def close(self):
        pass
