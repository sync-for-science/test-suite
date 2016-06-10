""" Authorization Code

The authorization code is obtained by using an authorization server
as an intermediary between the client and resource owner.

@see: https://tools.ietf.org/html/rfc6749#section-1.3.1
"""
import requests

from . import authorization_grant


class AuthorizationCodeStrategy(authorization_grant.AuthorizationGrant):
    """ Authorization Code Strategy.

    Args:
        config (dict): The OAuth config.
        urls (dict):
            authorize (string): The authorize endpoint.
            token (string): The token endpoint.
        authorizer (.authorize.base.AbstractAuthorizer): Handles the
            authorization server.

    Attributes:
        access_token (string): The access token.
        refresh_token (string): The refresh token.
        patient (string): The FHIR patient id.
    """

    access_token = None
    refresh_token = None
    patient = None

    def __init__(self, config, urls, authorizer):
        self._config = config
        self._urls = urls
        self._authorizer = authorizer

        self.refresh_token = config.get('refresh_token')

    def authorize(self):
        """ Authorize.

        Follows the steps defined in the SMART App Authorization Guide to
        generate an access token.

        @see: http://docs.smarthealthit.org/authorization/
        """
        code = self.request_authorization()
        self.exchange_authorization_code(code)

    def request_authorization(self):
        """ Request an authorization code from the authoriztion server.

        Handles steps 1 and 2 of the SMART authorization.
        """
        with self._authorizer:
            code = self._authorizer.authorize()

        return code

    def exchange_authorization_code(self, code):
        """ Exchange authorization code for access token.

        Handles step 3 of of the SMART authorization.
        """
        post_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self._config['client_id'],
            'redirect_uri': self._config['redirect_uri'],
        }

        response = self._token_request(post_data)

        self.access_token = response['access_token']

        # optional response parameters
        if response.get('refresh_token'):
            self.refresh_token = response['refresh_token']
        if response.get('patient'):
            self.patient = response['patient']

    def refresh_access_token(self):
        """ Use a refresh token to obtain a new access token.

        Handles step 5 of the SMART authorization.
        """
        post_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'redirect_uri': self._config['redirect_uri'],
        }

        response = self._token_request(post_data)

        self.access_token = response['access_token']

        # optional response parameters
        if response.get('refresh_token'):
            self.refresh_token = response['refresh_token']

    def _token_request(self, post_data):
        """ Make a token request.
        """
        auth = None
        if self._config.get('confidential_client'):
            auth = requests.auth.HTTPBasicAuth(
                self._config['client_id'],
                self._config['client_secret']
            )

        response = requests.post(self._urls['token'],
                                 auth=auth,
                                 data=post_data)

        assert int(response.status_code) == 200, response

        return response.json()
