""" Authorize the SMART API.
"""
from abc import ABCMeta
import json

from selenium import webdriver


class AbstractAuthorizer(metaclass=ABCMeta):
    """ Orchestrate the authorization path.

    Attributes:
        host (string): The testing site host.
        browser (webdriver.remote.webdriver.Webdriver): The selenium webdriver.
        vendor (string): The vendor we're authorizing.

    Example:
        Implements the context manager methods.

            authorizer = SmartAuthorizer()
            with authorizer as browser:
                token = authorizer.authorize()

        Is equivalent to:

            authorizer = SmartAuthorizer()
            try:
                authorizer.open()
                token = authorizer.authorize()
            finally:
                authorizer.close()
    """
    host = None
    browser = None
    vendor = None

    def authorize(self):
        """ The actual authorization method.
        """
        if self.browser is None:
            raise 'Webdriver must be connected first.'

        self._launch_step()
        self._vendor_step()

        return self._get_authorization()

    def _launch_step(self):
        """ Launch Step skeleton method.

        Override this if a vendor needs to begin the authorize process in a
        non-standard way.
        """
        self.browser.get(self.launch_url)

        selector = '#vendor option[data-vendor={vendor}]'
        self.find(selector.format(vendor=self.vendor)).click()

        self.find('#authorize').click()

    def _vendor_step(self):
        """ Vendor Step skeleton method.

        Override this if a vendor requires additional actions in order to
        authorize. Usually this would include logging in and clicking an
        "authorize" button.
        """

    def _get_authorization(self):
        """ Get Authorization skeleton method.

        Override this if a vendor's authorization will not be stored in the
        standard session location.
        """
        self.browser.get(self.session_url)
        session = json.loads(self.find('body').text)

        return session.get('authorizations', {}).get(self.vendor_key, {})

    def _browser(self):
        """ Browser Factory skeleton method.

        Override this if a vendor cannot be authorized with the standard
        PhantomJS webdriver, or if the webriver is being provided by an
        external service instead of created here.
        """
        return webdriver.PhantomJS()

    @property
    def launch_url(self):
        """ Properly formatted launch URL.
        """
        return self.host.rstrip('/') + '/'

    @property
    def session_url(self):
        """ Properly formatted session URL.
        """
        return self.host.rstrip('/') + '/session'

    @property
    def vendor_key(self):
        """ Derive the vendor key from the vendor.
        """
        return self.vendor.lower()

    def open(self):
        """ Connect to the selenium webdriver.
        """
        self.browser = self._browser()

    def close(self):
        """ Close the selenium webdriver.
        """
        self.browser.quit()

    def __enter__(self):
        self.open()
        return self.browser

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def find(self, selector):
        """ Shorthand for jQuery style element selecting.
        """
        return self.browser.find_element_by_css_selector(selector)
