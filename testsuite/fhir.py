""" FHIR Adapter """
import requests


OAUTH_URIS_DEFINITION = 'http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris'


def get_oauth_uris(base_url):
    """ Conformance statement should define a set of oauth uris.
    See: http://fhir-docs.smarthealthit.org/argonaut-dev/specification/#5
    Params
    ------
    provider : researchapp.models.providers.Provider
    Return
    ------
    dict :
        authorize : string
        token : string
    """
    url = '{url}metadata'.format(url=base_url)
    headers = {
        'Accept': 'application/json+fhir',
    }
    response = requests.get(url, headers=headers)

    try:
        conformance = response.json()
    except ValueError as error:
        error.response = response
        raise

    rest = [rest for rest in conformance['rest']][0]
    extensions = [ext for ext in rest['security']['extension']
                  if ext.get('url') == OAUTH_URIS_DEFINITION]
    extension = extensions[0]

    return {ext['url']: ext['valueUri'] for ext in extension['extension']}
