""" Authorize the Epic API.
"""
from . import base


class EpicAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the Epic authorization path.

    Args:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.
    """
    def __init__(self, config, authorize_url):
        self.config = config
        self.authorize_url = authorize_url

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Epic requires credentials.
        Username and password are intentionally included.
        """
        self.find('#txtUsername').send_keys('ARGONAUT')
        self.find('#txtPassword').send_keys('ARGONAUT')
        self.find('#cmdLogin').click()
