""" Authorize the SMART API.
"""
import json


class SmartAuthorizer(object):
    """ Orchestrate the SMART authorization path.

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
            self.find('#vendor option:first-child').click()
            self.find('#authorize').click()

            self.browser.get('http://tests.dev.syncfor.science:9003/session')
            session = json.loads(self.find('body').text)

            return session.get('authorizations', {}).get('smart', {})
        finally:
            self.browser.quit()

    def find(self, selector):
        return self.browser.find_element_by_css_selector(selector)
