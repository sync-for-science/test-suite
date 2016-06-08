""" Authorize the Allscripts API.
"""
from . import base


class AllscriptsAuthorizer(base.AbstractAuthorizer):
    """ Orchestrate the Allscripts authorization path.

    Args:
        host (string): The testing site host.
        vendor (string): The vendor we're authorizing.
    """
    def __init__(self, host, vendor='Allscripts'):
        self.host = host
        self.vendor = vendor

    def _browser(self):
        """ Browser Factory skeleton method.

        Allscripts doesn't work unless a browser window size is set.
        """
        browser = super()._browser()
        browser.set_window_size(1124, 850)

        return browser

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Allscripts requires credentials.
        Username and password are intentionally included.
        """
        self.find('#UserName').send_keys('s4s_5-5-16')
        self.find('#Password').send_keys('s4s!2345')
        self.find('[translate="Login_LogIn"]').click()
