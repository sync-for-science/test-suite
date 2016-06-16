"""
features.steps.utils
~~~~~~~~~~~~~~~~~~~~

This module contains useful functions that don't really fit anywhere in
particular.
"""
import jinja2
import requests


def bad_response_assert(response, message, **kwargs):
    with open('features/steps/response.jinja2') as handle:
        template = jinja2.Template(handle.read())

    return template.render(response=response,
                           message=message.format(**kwargs))


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
    if resource.startswith(('http://', 'https://')):
        url = resource
    else:
        url = "{url}{resource}".format(url=context.vendor_config['api']['url'],
                                       resource=resource)
    headers = {
        'Authorization': 'Bearer {0}'.format(context.oauth.access_token),
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate,sdch',
    }

    response = requests.get(url, headers=headers)

    return response


def find_references(resource, found=None):
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
    if found is None:
        found = []

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
    elif isinstance(resource, float):
        pass
    else:
        raise ValueError("I've missed something.", resource)

    return found
