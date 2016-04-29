"""
features.steps.utils
~~~~~~~~~~~~~~~~~~~~

This module contains useful functions that don't really fit anywhere in
particular.
"""
import requests

ERROR_AUTH_REQUEST = """
Authenticated POST to {endpoint} returned {status_code}.

{text}
"""

def auth_request(context, endpoint, post_data):
    """ Send an authenticated request.

    Parameters
    ----------
    context : behave.runner.Context
    context.auth : dict
        Authentication details.
    endpoint : str
        Endpoint to post to, probably "/token" or "/revoke".
    post_data : dict
        POST data.

    Returns
    -------
    requests.models.Response
        The returned response object.
    """
    client_auth = requests.auth.HTTPBasicAuth(context.auth['client_id'],
                                              context.auth['client_secret'])

    response = requests.post(context.auth['url'] + endpoint,
                         auth=client_auth,
                         data=post_data)

    assert int(response.status_code) == 200, \
            ERROR_AUTH_REQUEST.format(endpoint=endpoint,
                                      status_code=response.status_code,
                                      text=response.text)

    return response

def get_resource(context, resource):
    """ GET a provided FHIR API resource.

    Parameters
    ----------
    context : behave.runner.Context
    context.api_url : str
        The API base URL to build requests from.
    context.authorization : str
        Probably in the format "Bearer ...".
    resource : str
        The actual endpoint to query. Valid formats include:
         - Patient/123
         - Observation?patient=123

    Returns
    -------
    requests.models.Response
        The returned response object.
    """
    url = "{url}{resource}".format(url=context.api_url,
                                   resource=resource)
    headers = {
        'Authorization': context.authorization,
        'Accept': 'application/json',
    }

    return requests.get(url, headers=headers)

def find_references(resource, found=[]):
    """ Find references to other resources.

    Look for key-value pairs in the form:
        {"reference": "..."}

    Parameters
    ----------
    resource : dict
        The Resource to search for references in.
    found : str[]
        Recursively build up this list of references.

    Returns
    -------
    str[]
        All of the found references.
    """
    if isinstance(resource, dict):
        for key in resource:
            if key == 'reference':
                found.append(resource['reference'])
            else:
                find_references(resource[key], found)
    elif isinstance(resource, list):
        for value in resource:
            find_references(value, found)
    elif isinstance(resource, str):
        pass
    elif isinstance(resource, bool):
        pass
    elif isinstance(resource, int):
        pass
    else:
        raise ValueError("I've missed something.", resource)

    return found
