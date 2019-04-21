import functools
from urllib.parse import urlunparse, ParseResult
import requests


class ApiHost(object):
    def __init__(self, netloc, **kwargs):
        self._urlparts = {
            'netloc': netloc,
            'scheme': kwargs.get('scheme', 'https'),
            'params': kwargs.get('params', ''),
            'query': kwargs.get('query', ''),
            'fragment': kwargs.get('fragment', ''),
        }

    def __call__(self, path):
        return urlunparse(ParseResult(path=path, **self._urlparts))


class JsonRequests(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __getattr__(self, name):
        attr = getattr(requests, name)
        if not callable(attr):
            return attr
        @functools.wraps(attr)
        def wrapper(*args, **kwargs):
            raw = kwargs.pop('raw', False)
            result = attr(*args, **{ **self._kwargs, **kwargs })
            if not isinstance(result, requests.Response):
                return result
            result.raise_for_status()
            return result.text if raw else result.json()
        return wrapper
