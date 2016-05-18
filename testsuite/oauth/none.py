""" None strategy for accessing unprotected servers. """


class NoneStrategy(object):
    """ Implements the lib.oauth.Strategy interface. """
    access_token = None
    refresh_token = None

    def exchange_authorization_grant(self, grant):
        """ Exchange an authorization grant for an access token. """
        pass

    def request_offline_access(self):
        """ Fetch a refresh token. """
        pass

    def refresh_access_token(self):
        """ Request a new access token. """
        pass

    def authorization(self):
        """ Get an Authorization header value. """
        return None
