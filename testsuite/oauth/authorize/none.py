""" Do nothing.
"""


class NoneAuthorizer(object):
    """ Orchestrate the No-op authorization path.

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
        pass
