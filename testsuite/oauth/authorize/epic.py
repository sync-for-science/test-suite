""" Authorize the Epic API.
"""
from . import base


class EpicAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the Epic authorization path.

    Args:
        host (string): The testing site host.
        vendor (string): The vendor we're authorizing.
    """
    def __init__(self, host, vendor='Epic'):
        self.host = host
        self.vendor = vendor

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Epic requires credentials.
        Username and password are intentionally included.
        """
        self.find('#txtUsername').send_keys('ARGONAUT')
        self.find('#txtPassword').send_keys('ARGONAUT')
        self.find('#cmdLogin').click()
