""" FHIR Adapter """
import requests


OAUTH_URIS_DEFINITION = 'http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris'


def get_conformance_statement(base_url):
    """ Load an API's conformance statement.

    Args:
        base_url (str): URL in the form `http(s)://server{/path}`

    Returns:
        dict: The conformance statement.
    """
    url = '{url}metadata'.format(url=base_url)
    headers = {
        'Accept': 'application/json+fhir',
    }
    response = requests.get(url, headers=headers)

    try:
        return response.json()
    except ValueError as error:
        error.response = response
        raise


def get_oauth_uris(conformance):
    """ Use a conformance statement to determine a set of oauth uris.

    See:
        http://fhir-docs.smarthealthit.org/argonaut-dev/specification/#5

    Args:
        conformance (dict): A conformance statement.

    Returns:
        dict:
            authorize (str): The OAuth "authorize" endpoint.
            token (str): The OAuth "token" endpoint.
    """
    rest = [rest for rest in conformance['rest']][0]
    extensions = [ext for ext in rest['security']['extension']
                  if ext.get('url') == OAUTH_URIS_DEFINITION]
    extension = extensions[0]

    return {ext['url']: ext['valueUri'] for ext in extension['extension']}
