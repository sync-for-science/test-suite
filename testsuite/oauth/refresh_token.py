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

    def __init__(self, client_id, client_secret, refresh_token, redirect_uri, urls, basic):
        self._config = {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'refresh_token': refresh_token,
            'basic': basic,
        }
        self._urls = urls

    def exchange_authorization_grant(self, grant):
        """ Exchange an authorization grant for an access token.

        Modifies
        --------
            * access_token
            * refresh_token
        """
        post_data = {
            'grant_type': 'authorization_code',
            'code': grant,
            'client_id': self._config['client_id'],
            'redirect_uri': self._config['redirect_uri'],
        }

        auth = None
        if self._config['basic']:
            auth = requests.auth.HTTPBasicAuth(
                self._config['client_id'],
                self._config['client_secret']
            )

        response = requests.post(self._urls['token'],
                                 auth=auth,
                                 data=post_data)

        import logging
        logging.info(response.request.headers)
        logging.info(response.request.body)

        assert int(response.status_code) == 200, \
            ERROR_TOKEN_REQUEST.format(status_code=response.status_code,
                                       text=response.text)
        token_json = response.json()

        self.access_token = token_json.get('access_token', None)
        self.refresh_token = token_json.get('refresh_token', None)

    def request_offline_access(self):
        """ Fetch a refresh token.

        Modifies
        ---------
            * access_token
            * refresh_token
        """
        self.refresh_token = self._config['refresh_token']
        self.refresh_access_token()

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
