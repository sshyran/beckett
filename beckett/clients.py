# -*- coding: utf-8 -*-

import types

import inflect

import requests

from .exceptions import InvalidStatusCodeError

HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_PATCH = 'PATCH'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'

VALID_METHODS = (
    HTTP_GET,
    HTTP_POST,
    HTTP_PATCH,
    HTTP_PUT,
    HTTP_DELETE
)


class BaseClient(object):

    class Meta:
        # The name of this client.
        name = NotImplemented
        # The base_url for the API of this client.
        base_url = NotImplemented
        # A list of registered resources.
        resources = NotImplemented

    def __init__(self, *args, **kwargs):
        self.assign_resources(self.Meta.resources)
        self.resources = self.Meta.resources
        self.session = requests.Session()

    def assign_resources(self, resource_class_list):
        """
        Given a tuple of Resource classes, parse their Meta.methods
        attributes and  client methods for communicating with those resources.

        Subclass this method to control how resources are assigned.
        """
        for resource in resource_class_list:
            self.assign_methods(resource)

    def assign_methods(self, resource_class):
        """
        Given a resource_class and it's Meta.methods tuple,
        assign methods for communicating with that resource.
        """
        assert all([
            x.upper() in VALID_METHODS for x in resource_class.Meta.methods])
        for method in resource_class.Meta.methods:
            method_name = '{}_{}'.format(
                method.lower(), resource_class.Meta.name)
            p = inflect.engine()
            plural_name = p.plural(resource_class.Meta.name.lower())
            full_url = '{}/{}'.format(
                self.Meta.base_url, plural_name)
            self._assign_method(
                method.upper(),
                method_name,
                full_url,
                resource_class.Meta.acceptable_status_codes
            )

    def call_api(self, method_type, method_name,
                 full_url, valid_status_codes, data={}, id=None):
        """
        Does the actual HTTP API calls.
        """
        if method_type in [HTTP_GET, HTTP_PUT, HTTP_PATCH, HTTP_DELETE] and id:
            full_url = '{}/{}'.format(full_url, str(id))
        headers = {
            'X-CLIENT': self.Meta.name,
            'X-METHOD': method_name,
            'content-type': 'application/json'
        }
        params = {
            'headers': headers,
            'url': full_url
        }
        if method_type in ['POST', 'PUT', 'PATCH'] and isinstance(data, dict):
            params.update(json=data)
        prepared_request = self.session.prepare_request(
            requests.Request(method=method_type, **params)
        )
        response = self.session.send(prepared_request)
        return self._handle_response(response, valid_status_codes)

    def _assign_method(self, method_type, method_name,
                       full_url, valid_status_codes):
        """
        Using reflection, assigns a new method to this class.
        """

        """
        If we assigned the same method to each method, it's the same
        method in memory, so we need one for each acceptable HTTP method.
        """
        def get(self, method_type=method_type, method_name=method_name,
                full_url=full_url, valid_status_codes=valid_status_codes,
                data=None, id=None):
            return self.call_api(method_type, method_name,
                                 full_url, valid_status_codes, data, id=id)

        def put(self, method_type=method_type, method_name=method_name,
                full_url=full_url, valid_status_codes=valid_status_codes,
                data={}, id=None):
            return self.call_api(method_type, method_name,
                                 full_url, valid_status_codes, data, id=id)

        def post(self, method_type=method_type, method_name=method_name,
                 full_url=full_url, valid_status_codes=valid_status_codes,
                 data={}):
            return self.call_api(method_type, method_name,
                                 full_url, valid_status_codes, data)

        def patch(self, method_type=method_type, method_name=method_name,
                  full_url=full_url, valid_status_codes=valid_status_codes,
                  data={}, id=None):
            return self.call_api(method_type, method_name,
                                 full_url, valid_status_codes, data, id=id)

        def delete(self, method_type=method_type, method_name=method_name,
                   full_url=full_url, valid_status_codes=valid_status_codes,
                   data=None, id=id):
            return self.call_api(method_type, method_name,
                                 full_url, valid_status_codes, data, id=id)

        method_map = {
            'GET': get,
            'PUT': put,
            'POST': post,
            'PATCH': patch,
            'DELETE': delete
        }

        setattr(
            self, method_name.lower(),
            types.MethodType(method_map[method_type], self)
        )

    def _handle_response(self, response, valid_status_codes):
        """
        Handles Response objects
        """
        if response.status_code not in valid_status_codes:
                raise InvalidStatusCodeError
        return response.json()
