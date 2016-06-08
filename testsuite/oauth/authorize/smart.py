""" Authorize the SMART API.
"""
from . import base


class SmartAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the SMART authorization path.

    Args:
        host (string): The testing site host.
        vendor (string): The vendor we're authorizing.
    """
    def __init__(self, host, vendor='SMART'):
        self.host = host
        self.vendor = vendor
