""" Authorize the SMART API.
"""


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
        self.browser.get('http://tests.dev.syncfor.science:9003/')
        self.browser.find_element_by_css_selector('#vendor option:first-child').click()
        self.browser.find_element_by_css_selector('#authorize').click()
        print(self.browser.page_source)
        print(self.browser.current_url)
        self.browser.quit()
        exit()
