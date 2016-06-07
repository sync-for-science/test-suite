""" Authorize the Cerner API.
"""
import json


class CernerAuthorizer(object):
    """ Orchestrate the Cerner authorization path.

    Args:
        browser (selenium.webdriver.remote.webdriver.WebDriver)
        url (string): The authorization URL.

    Attributes:
        browser (selenium.webdriver.remote.webdriver.WebDriver)
        url (string): The authorization URL.
    """

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def authorize(self):
        """ The actual authorization method.
        """
        try:
            self.browser.get('http://tests.dev.syncfor.science:9003/')
            self.find('#vendor option[data-vendor=Cerner]').click()
            self.find('#authorize').click()

            self.find('#j_username').send_keys('ARGONAUT')
            self.find('#j_password').send_keys('sprinttest')
            self.find('#loginButton').click()

            self.browser.get('http://tests.dev.syncfor.science:9003/session')
            session = json.loads(self.find('body').text)

            return session.get('authorizations', {}).get('cerner', {})
        finally:
            self.browser.quit()

    def find(self, selector):
        return self.browser.find_element_by_css_selector(selector)
