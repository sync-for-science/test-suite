""" The SMART oAuth strategy. """
import requests


ERROR_TOKEN_REQUEST = """
Token request failed with status code "{status_code}".
{text}
"""


class RefreshTokenStrategy(object):
    """ Implements the lib.oauth.Strategy interface. """

    access_token = None
    refresh_token = None

    def __init__(self, client_id, client_secret, refresh_token, urls):
        self._config = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }
        self._urls = urls

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
        response = requests.delete(self._urls['token'],
                                   data=post_data)

        assert int(response.status_code) == 200, \
            ERROR_TOKEN_REQUEST.format(status_code=response.status_code,
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
        }
        if self._config['client_secret']:
            post_data['client_id'] = self._config['client_id']
            post_data['client_secret'] = self._config['client_secret']
        response = requests.post(self._urls['token'],
                                 data=post_data)

        assert int(response.status_code) == 200, \
            ERROR_TOKEN_REQUEST.format(status_code=response.status_code,
                                       text=response.text)
        token_json = response.json()

        self.access_token = token_json.get('access_token', None)
        self.refresh_token = token_json.get('refresh_token', self.refresh_token)

    def authorization(self):
        """ Get an Authorization header value. """
        return 'Bearer {access_token}'.format(access_token=self.access_token)
