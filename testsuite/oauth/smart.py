""" The SMART oAuth strategy. """
import requests


ERROR_AUTH_REQUEST = """
Authenticated POST to {url} returned {status_code}.
{text}
"""


class SmartStrategy(object):
    """ Implements the lib.oauth.Strategy interface. """

    access_token = None
    refresh_token = None

    # TODO: There really are too many arguments here. There's probably some
    # natural grouping between client_id/username/password, urls, and auth,
    # but maybe that's just forcing things.
    # This is usally a sign that a class is doing too much, but all of these
    # seem pretty integral.
    def __init__(self, client_id, username, password, token_url, revoke_url, auth=None):  # noqa pylint: disable=too-many-arguments
        self._config = {
            'client_id': client_id,
            'username': username,
            'password': password,
            'token_url': token_url,
            'revoke_url': revoke_url,
            'auth': auth,
        }

    def request_offline_access(self):
        """ Fetch a refresh token.

        Modifies
        ---------
            * access_token
            * refresh_token
        """
        post_data = {
            'username': self._config['username'],
            'password': self._config['password'],
            'grant_type': 'password',
            'scope': 'smart/portal offline_access',
            'client_id': self._config['client_id'],
        }
        response = requests.post(self._config['token_url'],
                                 auth=self._config['auth'],
                                 data=post_data)

        assert int(response.status_code) == 200, \
            ERROR_AUTH_REQUEST.format(url=self._config['token_url'],
                                      status_code=response.status_code,
                                      text=response.text)
        token_json = response.json()

        self.access_token = token_json['access_token']
        self.refresh_token = token_json['refresh_token']

    def revoke_access_token(self):
        """ Request that the oAuth server revoke stored access token.

        Doesn't unset our currently stored data.
        """
        post_data = {
            'token': self.access_token,
        }
        response = requests.post(self._config['revoke_url'],
                                 auth=self._config['auth'],
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
            'client_id': self._config['client_id'],
        }
        response = requests.post(self._config['token_url'],
                                 auth=self._config['auth'],
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
