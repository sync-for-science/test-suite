""" Authorize the SMART API.
"""
from abc import ABCMeta
from urllib import parse
import uuid

from selenium import webdriver


class AbstractAuthorizer(metaclass=ABCMeta):
    """ Orchestrate the authorization path.

    Attributes:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.

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
    browser = None
    config = None
    authorize_url = None

    _state = None

    def authorize(self):
        """ The actual authorization method.
        """
        if self.browser is None:
            raise Exception('Webdriver must be connected first.')

        self._launch_step()
        self._vendor_step()

        return self._get_authorization()

    def _launch_step(self):
        """ Launch Step skeleton method.

        Override this if a vendor needs to begin the authorize process in a
        non-standard way.
        """
        launch_url = '?'.join([
            self.authorize_url,
            parse.urlencode(self.launch_params)
        ])
        self.browser.get(launch_url)

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
        redirect_uri = parse.urlparse(self.browser.current_url)
        query = parse.parse_qs(redirect_uri.query)
        self._check_state(''.join(query['state']))

        return ''.join(query['code'])

    def _browser(self):
        """ Browser Factory skeleton method.

        Override this if a vendor cannot be authorized with the standard
        PhantomJS webdriver, or if the webriver is being provided by an
        external service instead of created here.
        """
        return webdriver.PhantomJS()

    def _generate_state(self):
        """ Generates a state token.
        """
        self._state = str(uuid.uuid4())
        return self._state

    def _check_state(self, state):
        """ Checks and destroys a state token.
        """
        try:
            if self._state != state:
                raise Exception('Invalid state.', self._state, state)
        finally:
            self._state = None

    @property
    def launch_params(self):
        """ The params to send to the authorize url.
        """
        state = self._generate_state()
        params = {
            'response_type': 'code',
            'client_id': self.config['client_id'],
            'redirect_uri': self.config['redirect_uri'],
            'scope': self.config['scope'],
            'state': state,
            'aud': self.config['aud'],
        }

        return params

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
