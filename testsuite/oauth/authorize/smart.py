""" Authorize the SMART API.
"""
from . import base


class SmartAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the SMART authorization path.

    Args:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.
    """
    def __init__(self, config, authorize_url):
        super().__init__(config, authorize_url)
