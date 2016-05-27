""" The Client Credentials oAuth strategy. """
import requests


ERROR_TOKEN_REQUEST = """
Token request failed with status code "{status_code}".
{text}
"""


class ClientCredentialsStrategy(object):
    """ Implements the lib.oauth.Strategy interface. """

    access_token = None
    refresh_token = None

    def __init__(self, client_id, client_secret, token_url):
        self._config = {
            'client_id': client_id,
            'client_secret': client_secret,
        }
        self._urls = {
            'token': token_url,
        }

    def exchange_authorization_grant(self, grant):
        """ Exchange an authorization grant for an access token.
        """
        raise NotImplementedError

    def request_offline_access(self):
        """ Fetch a refresh token.

        Modifies
        ---------
            * access_token
            * refresh_token
        """
        post_data = {
            'grant_type': 'client_credentials',
        }
        auth = requests.auth.HTTPBasicAuth(
            self._config['client_id'],
            self._config['client_secret']
        )

        response = requests.post(self._urls['token'],
                                 auth=auth,
                                 data=post_data)

        assert int(response.status_code) == 200, \
            ERROR_TOKEN_REQUEST.format(status_code=response.status_code,
                                       text=response.text)
        token_json = response.json()

        self.access_token = token_json.get('access_token', None)
        self.refresh_token = token_json.get('refresh_token', None)


    def refresh_access_token(self):
        """ Request a new access token.

        Modifies
        ---------
            * access_token
            * refresh_token
        """
        self.request_offline_access()

    def authorization(self):
        """ Get an Authorization header value. """
        return 'Bearer {access_token}'.format(access_token=self.access_token)
