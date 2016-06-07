""" Authorize the Allscripts API.
"""
import json

from selenium.webdriver.common.keys import Keys


class AllscriptsAuthorizer(object):
    """ Orchestrate the Allscripts authorization path.

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

        self.browser.set_window_size(1124, 850)

    def authorize(self):
        """ The actual authorization method.
        """
        try:
            self.browser.get('http://tests.dev.syncfor.science:9003/')
            self.find('#vendor option[data-vendor=Allscripts]').click()
            self.find('#authorize').click()

            self.find('#UserName').send_keys('s4s_5-5-16')
            self.find('#Password').send_keys('s4s!2345')
            self.find('[translate="Login_LogIn"]').click()

            self.browser.get('http://tests.dev.syncfor.science:9003/session')
            session = json.loads(self.find('body').text)
            print(session)

            return session.get('authorizations', {}).get('allscripts', {})
        finally:
            self.browser.quit()

    def find(self, selector):
        return self.browser.find_element_by_css_selector(selector)
