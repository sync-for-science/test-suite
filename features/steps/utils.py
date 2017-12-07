# pylint: disable=missing-docstring
"""
features.steps.utils
~~~~~~~~~~~~~~~~~~~~

This module contains useful functions that don't really fit anywhere in
particular.
"""
import datetime
import json

import grequests
import jinja2
import requests

from functools import reduce


CONTENT_LENGTH_LIMIT = 1024 * 5000  # 5MB
ERROR_CONTENT_LENGTH = 'Content length "{}" exceeds expected content length limit of {}.'


def bad_response_assert(response, message, **kwargs):
    with open('features/steps/response.jinja2') as handle:
        template = jinja2.Template(handle.read())

    return template.render(response=response,
                           message=message.format(**kwargs))


def bad_redirect_assert(message, sent, received):
    with open('features/steps/redirect.jinja2') as handle:
        template = jinja2.Template(handle.read())

    return template.render(message=message,
                           sent=sent,
                           received=received)


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
        url = "{url}{resource}".format(url=context.vendor_config['versioned_api']['url'],
                                       resource=resource)
    headers = {
        'Authorization': 'Bearer {0}'.format(context.oauth.access_token),
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate,sdch',
    }

    response = make_request(context.cache, url, headers)

    try:
        payload = {
            'url': url,
            'method': 'GET',
            'status_code': response.status_code,
            'response': bad_response_assert(response, ''),
            'feature': context.feature.name,
        }
        context.config.on_payload(payload)
    except AttributeError:
        pass

    if context.config.es_url:
        log_requests_response(context.config.es_url, response)

    return response


def make_request(cache, url, headers):
    if url in cache:
        return cache[url]

    with requests.get(url, headers=headers, stream=True) as response:
        # Limit response size
        # First check the content-length header, if present.
        # This will prevent downloading overly large responses, assuming a well configured server.
        content_length = int(response.headers.get('content-length', 0))
        assert content_length < CONTENT_LENGTH_LIMIT, \
            ERROR_CONTENT_LENGTH.format(content_length, CONTENT_LENGTH_LIMIT)

        # Now, complete the download, and check the response size.
        content_length = len(response.content)
        assert content_length < CONTENT_LENGTH_LIMIT, \
            ERROR_CONTENT_LENGTH.format(content_length, CONTENT_LENGTH_LIMIT)

    cache[url] = response

    return response


def log_requests_response(es_url, response):
    """ Log the response from a FHIR query.

    Args:
        es_url (string): The ElasticSearch endpoint.
        response (requests.models.Response): The resposne to log.
    """
    payload = {
        'request': _clean(response.request),
        'response': _clean(response),
        'now': datetime.datetime.now().isoformat(),
    }

    # Use the asyncronous grequests library because we don't need a response.
    req = grequests.post(es_url, data=json.dumps(payload))
    grequests.send(req)


def _clean(loggable):
    """ Prepare request/response for logging.

    Limits objects to just a few fields and makes sure that they're
    json-serializable.

    Args:
        loggable: The requests request or response to clean.

    Returns:
        {
            body: ...
            headers: ...
            json: ...
            method: ...
            url: ...
        }
    """

    valid = ('body', 'headers', 'method', 'url')
    data = {k: v for k, v in vars(loggable).items() if k in valid}

    data['headers'] = dict(data['headers'])

    if hasattr(loggable, 'text'):
        data['body'] = loggable.text

    try:
        data['json'] = loggable.json()
    except:  # pylint: disable=bare-except
        pass

    return data


def traverse(resource, path):
    def walk(data, k):
        if isinstance(data, dict):
            return data.get(k)
        elif isinstance(data, list):
            return [reduce(walk, [k], el) for el in data]
        return None
    return reduce(walk, path, resource)


def has_one_of(resource, fields):
    """
    Explores a dictionary looking for the existence of fields, can take "."
     separated hierarchical representation of individual fields.
    :param resource: dict
            The resource to search for fields in.
    :param fields: iterable
            The fields to search for. Hierarchy for fields separated by "."
            e.g. ["Observation.component.valueQuantity.value", ..]
    :return: True if any of the fields are found in the resource.
    """
    return any([traverse(resource, field.split(".")) for field in fields])


def find_named_key(resource, named_key, found=None):
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
            if key == named_key:
                found.append(resource[named_key])
            else:
                find_named_key(resource[key], named_key, found)
    elif isinstance(resource, list):
        for value in resource:
            find_named_key(value, named_key, found)
    elif isinstance(resource, str):
        pass
    elif isinstance(resource, bool):
        pass
    elif isinstance(resource, int):
        pass
    elif isinstance(resource, float):
        pass
    elif resource is None:
        pass
    else:
        raise ValueError("I've missed something.", resource)

    return found
