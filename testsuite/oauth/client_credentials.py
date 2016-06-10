""" Client Credentials

The client credentials (or other forms of client authentication) can
be used as an authorization grant when the authorization scope is
limited to the protected resources under the control of the client,
or to protected resources previously arranged with the authorization
server.

@see: https://tools.ietf.org/html/rfc6749#section-1.3.4
"""
import requests

from . import authorization_grant


class ClientCredentialsStrategy(authorization_grant.AuthorizationGrant):
    """ Client credentials Strategy.

    Args:
        client_id (string): The client id.
        client_secret (string): The client secret.
        token_url (string): The token endpoint.

    Attributes:
        access_token (string): The access token.
        refresh_token (string): The refresh token.
    """

    access_token = None
    refresh_token = None

    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

    def authorize(self):
        """ Authorize.

        Follows the steps defined in the OAuth spec to generate an access
        token.

        @see: https://tools.ietf.org/html/rfc6749#section-4.4
        """
        post_data = {
            'grant_type': 'client_credentials',
        }

        response = self._token_request(post_data)

        self.access_token = response['access_token']

        # optional response parameters
        if response.get('refresh_token'):
            self.refresh_token = response['refresh_token']

    def _token_request(self, post_data):
        """ Make a token request.
        """
        auth = requests.auth.HTTPBasicAuth(
            self.client_id,
            self.client_secret,
        )

        response = requests.post(self.token_url,
                                 auth=auth,
                                 data=post_data)

        assert int(response.status_code) == 200, response

        return response.json()
