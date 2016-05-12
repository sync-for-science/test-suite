""" The SMART oAuth strategy. """
import requests


ERROR_AUTH_REQUEST = """
Authenticated POST to {url} returned {status_code}.
{text}
"""


class RefreshTokenStrategy(object):
    """ Implements the lib.oauth.Strategy interface. """

    access_token = None
    refresh_token = None

    # TODO: There really are too many arguments here. There's probably some
    # natural grouping between client_id/username/password, urls, and auth,
    # but maybe that's just forcing things.
    # This is usally a sign that a class is doing too much, but all of these
    # seem pretty integral.
    def __init__(self, client_id, client_secret, refresh_token, token_url):
        self._config = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'token_url': token_url,
        }

    def request_offline_access(self):
        """ Fetch a refresh token.

        Modifies
        ---------
            * access_token
            * refresh_token
        """
        self.refresh_token = self._config['refresh_token']
        self.refresh_access_token()

    def revoke_access_token(self):
        """ Request that the oAuth server revoke stored access token.

        Doesn't unset our currently stored data.
        """
        post_data = {
            'token': self.access_token,
        }
        response = requests.delete(self._config['token_url'],
                                   data=post_data)

        assert int(response.status_code) == 200, \
            ERROR_AUTH_REQUEST.format(url=self._config['revoke_url'],
                                      status_code=response.status_code,
                                      text=response.text)

    def refresh_access_token(self):
        """ Request a new access token.

        Modifies
        ---------
            * access_token
            * refresh_token
        """
        post_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'scope': 'launch/patient patient/*.read',
            'client_id': self._config['client_id'],
            'client_secret': self._config['client_secret'],
        }
        response = requests.post(self._config['token_url'],
                                 data=post_data)

        assert int(response.status_code) == 200, \
            ERROR_AUTH_REQUEST.format(url=self._config['token_url'],
                                      status_code=response.status_code,
                                      text=response.text)
        token_json = response.json()

        self.access_token = token_json['access_token']
        self.refresh_token = token_json['refresh_token']

    def authorization(self):
        """ Get an Authorization header value. """
        return 'Bearer {access_token}'.format(access_token=self.access_token)
