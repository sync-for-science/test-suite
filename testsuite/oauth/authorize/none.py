""" Do nothing.
"""
from . import base


class NoneAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the No-op authorization path.
    """
    def __init__(self):
        super().__init__(None, None)

    def _launch_step(self):
        pass

    def _vendor_step(self):
        pass

    def _get_authorization(self):
        pass

    def _browser(self):
        return True

    def open(self):
        self.browser = self._browser()

    def close(self):
        self.browser = None
