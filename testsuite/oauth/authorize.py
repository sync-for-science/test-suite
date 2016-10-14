""" Authorize the SMART API.
"""
import itertools
import logging
from urllib import parse
import uuid

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.ui import WebDriverWait


AUTHORIZE_TIMEOUT = 15
CONNECTION_TIMEOUT = 60
VISIBILITY_TIMEOUT = 10


class StepRunner(object):
    """ I know how to run steps!
    """
    def __init__(self):
        self.browser = None

    def open(self):
        """ Connect to the selenium webdriver.
        """
        self.browser = self._browser()

        return self.browser

    def close(self):
        """ Close the virtual browser.
        """
        self.browser.quit()

        return None

    def get(self, url):
        """ Tell the browser to load a URL.
        """
        self.browser.get(url)

    def execute_step(self, step):
        """ Execute a provided step.
        """
        try:
            elem = self.browser.find_element_by_css_selector(step['element'])
        except NoSuchElementException as err:
            if step.get('optional'):
                return
            raise ElementNotFoundException(str(err), self.browser)

        # Make sure the element exists before we continue
        try:
            wait = WebDriverWait(self.browser, VISIBILITY_TIMEOUT)
            wait.until(visibility_of(elem))
        except TimeoutException:
            if not elem.is_displayed() and step.get('optional'):
                return
            elif not elem.is_displayed():
                msg = 'Element is hidden: {0}'.format(step['element'])
                raise ElementNotFoundException(msg, self.browser)

        # Apply the action to the matched element.
        # Only one action can be applied per step.
        if 'send_keys' in step:
            elem.send_keys(step['send_keys'])
        elif 'click' in step:
            elem.click()
        elif 'execute_script' in step:
            self.browser.execute_script(step['execute_script'])
        else:
            raise NoStepCommandException(step, self.browser)

    def get_query(self, base_url=None):
        """ Get a parsed query from the current URL.

        If base_url is provided, wait until the current URL matches it.
        """
        if base_url:
            # Only return the query if the base_url is what we expect it to be.
            try:
                wait = WebDriverWait(self.browser, AUTHORIZE_TIMEOUT)
                wait.until(CurrentUrlContains(base_url))
            except TimeoutException:
                raise AuthorizationException('Authorization timed out.', self.browser)

        url = parse.urlparse(self.browser.current_url)
        return parse.parse_qs(url.query)

    @property
    def current_url(self):
        return self.browser.current_url

    def _browser(self):
        """ Initialize a Firefox webdriver.
        """
        RemoteConnection.set_timeout(CONNECTION_TIMEOUT)

        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')  # noqa
        driver = webdriver.Firefox(profile)
        driver.implicitly_wait(1)

        return driver


class Authorizer(object):
    """ Orchestrate the authorization path.

    Attributes:
        config (dict): The oauth config for this vendor.
        authorize_url (string): The vendor's authorize endpoint.

    Example:
        Implements the context manager methods.

            authorizer = Authorizer()
            with authorizer:
                token = authorizer.authorize()

        Is equivalent to:

            authorizer = Authorizer()
            try:
                authorizer.runner.open()
                token = authorizer.authorize()
            finally:
                authorizer.runner.close()
    """
    authorize_url = None
    config = None
    runner = None
    _state = None

    def __init__(self, config, authorize_url, step_runner=None):
        self.config = config
        self.authorize_url = authorize_url
        self.runner = step_runner
        self.log = logging.getLogger(__name__)

        if not self.runner:
            self.runner = StepRunner()

    def authorize(self):
        """ The actual authorization method.
        """
        if not self.runner.browser:
            raise Exception('Webdriver must be connected first.')

        parameters = self.launch_params

        self.ask_for_authorization(parameters)
        response = self.provide_user_input()

        try:
            self._validate_state(response)
            self._validate_code(response)
        except AssertionError as err:
            raise ValidationErrorException(str(err), self.runner.browser)

        return response['code'][0]

    def ask_for_authorization(self, parameters):
        """ Ask for authorization.

        Step 1 of the SMART authorization process.
        """
        self.log.info('Ask for authorization')

        # Store the "state" parameter so that we can validate it later
        self._state = parameters['state']
        self.log.info('STATE: %s', self._state)

        authorize_url = self.authorize_url + '?' + parse.urlencode(parameters)
        self.log.info('AUTHORIZE URL: %s', authorize_url)

        self.runner.get(authorize_url)

    def provide_user_input(self):
        """ Provide end-user input to EHR.

        Step 2 of the SMART authorization process. Usually this would include
        logging in and clicking an "authorize" button.
        """
        self.log.info('Provide user input')

        steps = itertools.chain(self.config.get('sign_in_steps', []),
                                self.config.get('authorize_steps', []))

        for step in steps:
            self.runner.execute_step(step)

        base_url = self.config['redirect_uri'].replace('http://', '')
        query = self.runner.get_query(base_url=base_url)
        self.log.info('REDIRECT URI: %s', self.runner.current_url)

        if 'error' in query:
            raise ReturnedErrorException(query['error'],
                                         query.get('error_descriptoin'),
                                         self.runner.browser)

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

    def __enter__(self):
        self.runner.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.runner.close()

    def _validate_state(self, query):
        assert 'state' in query, 'Missing state parameter.'

        assert len(query['state']) == 1, 'Too many state parameters.'

        assert query['state'][0] == self._state, \
            'Returned state parameter does not match sent state.'

    def _validate_code(self, query):
        assert 'code' in query, 'Missing code parameter.'

        assert len(query['code']) == 1, 'Too many code parameters.'


class AuthorizationRevoker(object):
    """ Orchestrate the revoke authorization path.

    Attributes:
        config (dict): The oauth config for this vendor.

    Example:
        Implements the context manager methods.

            revoker = AuthorizationRevoker()
            with revoker:
                token = revoker.revoke_authorization()
    """
    def __init__(self, config, step_runner=None):
        self.config = config
        self.runner = step_runner

        if not self.runner:
            self.runner = StepRunner()

    def revoke_authorization(self):
        """ The actual revoke authorization method.
        """
        if not self.runner.browser:
            raise Exception('Webdriver must be connected first.')

        self.runner.get(self.config.get('revoke_url'))

        steps = itertools.chain(self.config.get('sign_in_steps', []),
                                self.config.get('revoke_steps', []))
        for step in steps:
            self.runner.execute_step(step)

    def __enter__(self):
        self.runner.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.runner.close()


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

        super().__init__(message,
                         path.replace('testsuite', ''),
                         browser.current_url)


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
