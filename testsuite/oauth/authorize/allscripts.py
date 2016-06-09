""" Authorize the Allscripts API.
"""
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        self.display = None

    def _browser(self):
        """ Browser Factory skeleton method.

        Allscripts doesn't work with PhantomJS. Initialize a Chrome webdriver
        instead.
        """
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        return webdriver.Chrome()

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Allscripts requires credentials.
        Username and password are intentionally included.
        """
        default_login_button = self.find('[translate="DEFAULT_LOGIN_BUTTON"]')
        if default_login_button.is_displayed():
            default_login_button.click()
        self.find('#UserName').send_keys('s4s_5-5-16')
        self.find('#Password').send_keys('s4s!2345')
        self.find('[translate="Login_LogIn"]').click()

        while 'Login/Home/Index' in self.browser.current_url:
            time.sleep(1)

    def close(self):
        """ Close the virtual display.
        """
        super().close()
        self.display.stop()
