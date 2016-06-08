""" Authorize the Cerner API.
"""
from . import base


class CernerAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the Cerner authorization path.

    Args:
        host (string): The testing site host.
        vendor (string): The vendor we're authorizing.
    """
    def __init__(self, host, vendor='Cerner'):
        self.host = host
        self.vendor = vendor

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Cerner requires credentials.
        Username and password are intentionally included.
        """
        self.find('#j_username').send_keys('ARGONAUT')
        self.find('#j_password').send_keys('sprinttest')
        self.find('#loginButton').click()
