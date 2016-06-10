""" Authorize the Cerner API.
"""
from . import base


class CernerAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the Cerner authorization path.

    Args:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.
    """
    def __init__(self, config, authorize_url):
        self.config = config
        self.authorize_url = authorize_url

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Cerner requires credentials.
        Username and password are intentionally included.
        """
        self.find('#j_username').send_keys('ARGONAUT')
        self.find('#j_password').send_keys('sprinttest')
        self.find('#loginButton').click()

    @property
    def launch_params(self):
        """ The params to send to the authorize url.

        Cerner uses the EHR launch sequence and requires a launch code.
        """
        params = super().launch_params
        params['launch'] = self.config['launch']

        return params
