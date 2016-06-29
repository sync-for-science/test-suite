""" Authorize the SMART API.
"""
from urllib import parse
import uuid

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


AUTHORIZE_TIMEOUT = 15


class Authorizer(object):
    """ Orchestrate the authorization path.

    Attributes:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.

    Example:
        Implements the context manager methods.

            authorizer = Authorizer()
            with authorizer as browser:
                token = authorizer.authorize()

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

        parameters = self.launch_params

        self.ask_for_authorization(parameters)
        response = self.provide_user_input()

        try:
            self._validate_state(response)
            self._validate_code(response)
        except AssertionError as err:
            raise ValidationErrorException(str(err), self.browser)

        return response['code'][0]

    def ask_for_authorization(self, parameters):
        """ Ask for authorization.

        Step 1 of the SMART authorization process.
        """
        # Store the "state" parameter so that we can validate it later
        self._state = parameters['state']

        launch_url = self.authorize_url + '?' + parse.urlencode(parameters)
        self.browser.get(launch_url)

    def provide_user_input(self):
        """ Provide end-user input to EHR.

        Step 2 of the SMART authorization process. Usually this would include
        logging in and clicking an "authorize" button.
        """
        for step in self.config.get('steps', []):
            self._execute_step(step)

        # Some vendors implement an AJAX based login procedure.
        try:
            wait = WebDriverWait(self.browser, AUTHORIZE_TIMEOUT)
            wait.until(CurrentUrlContains(self.config['redirect_uri']))
        except TimeoutException:
            raise AuthorizationException('Authorization timed out.', self.browser)

        redirect_uri = parse.urlparse(self.browser.current_url)
        query = parse.parse_qs(redirect_uri.query)

        if 'error' in query:
            raise ReturnedErrorException(query['error'],
                                         query.get('error_descriptoin'),
                                         self.browser)

        return query

    @property
    def launch_params(self):
        """ The params to send to the authorize url.
        """
        state = str(uuid.uuid4())
        params = {
            'response_type': 'code',
            'client_id': self.config['client_id'],
            'redirect_uri': self.config['redirect_uri'],
            'scope': self.config['scope'],
            'state': state,
            'aud': self.config['aud'],
        }
        if 'extra_launch_params' in self.config:
            params.update(self.config['extra_launch_params'])

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

    def _browser(self):
        """ Initialize a Chrome webdriver.
        """
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        options = Options()
        options.add_argument("--no-sandbox")

        return webdriver.Chrome(chrome_options=options)

    def _execute_step(self, step):
        try:
            elem = self.browser.find_element_by_css_selector(step['element'])
        except NoSuchElementException as err:
            if step.get('optional'):
                return
            raise ElementNotFoundException(str(err), self.browser)

        # Make sure the element exists before we continue
        if not elem.is_displayed() and step.get('optional'):
            return
        elif not elem.is_displayed():
            raise ElementNotFoundException('Element is hidden', self.browser)

        # Apply the action to the matched element.
        # Only one action can be applied per step.
        if 'send_keys' in step:
            elem.send_keys(step['send_keys'])
        elif 'click' in step:
            elem.click()
        else:
            raise NoStepCommandException(step, self.browser)

    def _validate_state(self, query):
        assert 'state' in query, 'Missing state parameter.'

        assert len(query['state']) == 1, 'Too many state parameters.'

        assert query['state'][0] == self._state, \
            'Returned state parameter does not match sent state.'

    def _validate_code(self, query):
        assert 'code' in query, 'Missing code parameter.'

        assert len(query['code']) == 1, 'Too many code parameters.'


class CurrentUrlContains(object):
    """ An expectation that the browser's current url contains a
    case-sensitive substring.

    @see: http://selenium-python.readthedocs.io/waits.html

    Returns:
        True when the URL matches, False otherwise
    """
    def __init__(self, substring):
        self.substring = substring

    def __call__(self, driver):
        return self.substring in driver.current_url


class AuthorizationException(Exception):
    """ An Error occured during the authorization process.
    """
    def __init__(self, message, browser):
        # Save a screenshot so we can see what's up
        path = 'testsuite/static/screenshots/{0}.png'.format(uuid.uuid4())
        browser.save_screenshot(path)

        super().__init__(message, path.replace('testsuite', ''))


class ValidationErrorException(AuthorizationException):
    """ An error occurred validating the response.
    """


class ReturnedErrorException(AuthorizationException):
    """ The redirect URI contained an "error" parameter.
    """
    def __init__(self, error, description, browser):
        message = 'Error: {0}\nDescription: {1}'.format(error, description)
        super().__init__(message, browser)


class ElementNotFoundException(AuthorizationException):
    """ An element could not be found for a step.
    """


class NoStepCommandException(AuthorizationException):
    """ A step was provided without an action.
    """
    def __init__(self, step, browser):
        message = 'No command was provided for step: {0}'.format(step)
        super().__init__(message, browser)
