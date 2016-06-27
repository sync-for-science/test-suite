""" Authorize the SMART API.
"""
import time
from urllib import parse
import uuid

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Authorizer:
    """ Orchestrate the authorization path.

    Attributes:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.

    Example:
        Implements the context manager methods.

            authorizer = Authorizer()
            with authorizer as browser:
                token = browser.authorize()

        Is equivalent to:

            authorizer = Authorizer()
            try:
                authorizer.open()
                token = authorizer.authorize()
            finally:
                authorizer.close()
    """
    browser = None
    config = None
    authorize_url = None
    display = None
    _state = None

    def __init__(self, config, authorize_url):
        self.config = config
        self.authorize_url = authorize_url


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
        elt = None
        for step in self.config.get('steps', []):
            if 'find' in step:
                elt = self.find(step['find'])
            elif 'type' in step:
                elt.send_keys(step['type'])
            elif 'click' in step:
                if not elt.is_displayed():
                    continue
                elt.click()

        time_spent = 0
        to_wait = 0.5
        while self.config['redirect_uri'] not in self.browser.current_url:
            time.sleep(to_wait)
            time_spent += to_wait
            assert time_spent < 15, "Timed out on authorize!"

    def _get_authorization(self):
        """ Get Authorization skeleton method.

        Override this if a vendor's authorization will not be stored in the
        standard session location.
        """
        redirect_uri = parse.urlparse(self.browser.current_url)
        query = parse.parse_qs(redirect_uri.query)
        self._check_state(''.join(query['state']))

        if 'error' in query:
            raise Exception(query['error'], query.get('error_description'))

        return ''.join(query['code'])

    def _browser(self):
        """ Browser Factory skeleton method.
        Initialize a Chrome webdriver
        """
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        options = Options()
        options.add_argument("--no-sandbox")

        return webdriver.Chrome(chrome_options=options)

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
        for k in self.config.get('extra_launch_params', {}):
            params[k] = self.config['extra_launch_params'][k]

        return params

    def open(self):
        """ Connect to the selenium webdriver.
        """
        self.browser = self._browser()

    def close(self):
        """ Close the virtual browser.
        """
        self.browser.quit()
        self.display.stop()

    def __enter__(self):
        self.open()
        return self.browser

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def find(self, selector):
        """ Shorthand for jQuery style element selecting.
        """
        return self.browser.find_element_by_css_selector(selector)
