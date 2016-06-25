# -*- coding: utf-8 -*-

import sys
import types

import inflect

from .clients import HTTPClient
from .constants import DEFAULT_VALID_STATUS_CODES
from .exceptions import BadURLException, MissingUidException

if sys.version_info[0] == 3:
    # Py3
    from urllib.parse import urlparse
else:
    # Py2
    from urlparse import urlparse


class BaseResource(object):
    """
    A simple representation of a resource.

    Usage:

        from beckett.resources import BaseResource

        class Product(BaseResource):

            class Meta:
                name = 'Product'
                identifier = 'slug'
                attributes = (
                    'slug',
                    'name',
                    'price',
                    'discount'
                )

        # Data will usually come straight from the client method
        >>> data = {'name': 'Tasty product', 'slug': 'sluggy'}
        >>> product = Product(**data)
        <Product | sluggy>
        >>> product.name
        'Tasty product'

    """

    class Meta:
        # The name of this resource, used in __str__ methods.
        name = 'Resource'
        # The name of the resource used in the URL, i.e. 'resources'
        resource_name = None
        # The key with which you uniquely identify this resource.
        identifier = 'id'
        # Acceptable attributes that you want to display in this resource.
        attributes = (identifier,)
        # HTTP status codes that are considered "acceptable"
        # when calling this resource
        valid_status_codes = DEFAULT_VALID_STATUS_CODES
        # HTTP Methods that work on this resource
        methods = (
            'get',
        )
        # When receiving paginated results, use this key to render instances.
        pagination_key = 'results'

    def __init__(self, *args, **kwargs):
        self.set_attributes(**kwargs)

    def __str__(self):
        """
        Returns a string representation based on the `self.Meta.name`
        and `self.Meta.identifier` attribute value.
        """
        return '<{} | {}>'.format(
            self.Meta.name, getattr(self, self.Meta.identifier))

    def set_attributes(self, **kwargs):
        """
        Set the resource attributes from the kwargs.
        Only sets items in the `self.Meta.attributes` white list.

        Subclass this method to customise attributes.

        Args:
            kwargs: Keyword arguements passed into the init of this class
        """
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                setattr(self, field, value)

    @classmethod
    def get_resource_url(cls, resource, base_url):
        """
        Construct the URL for talking to this resource.

        i.e.:

        http://myapi.com/api/resource

        Note that this is NOT the method for calling individual instances i.e.

        http://myapi.com/api/resource/1

        Args:
            resource: The resource class instance
            base_url: The Base URL of this API service.
        returns:
            resource_url: The URL for this resource
        """
        if resource.Meta.resource_name:
            url = '{}/{}'.format(base_url, resource.Meta.resource_name)
        else:
            p = inflect.engine()
            plural_name = p.plural(resource.Meta.name.lower())
            url = '{}/{}'.format(base_url, plural_name)
        return cls._parse_url_and_validate(url)

    @classmethod
    def get_single_resource_url(cls, url, uid, **kwargs):
        """
        Construct the URL for talking to an individual resource.

        http://myapi.com/api/resource/1

        Args:
            url: The url for this resource
            uid: The unique identifier for an individual resource
            kwargs: Additional keyword argueents
        returns:
            final_url: The URL for this individual resource
        """

        if uid is None:
            raise MissingUidException
        url = '{}/{}'.format(url, uid)
        return cls._parse_url_and_validate(url)

    @staticmethod
    def get_method_name(resource, method_type):
        """
        Generate a method name for this resource based on the method type.
        """
        return '{}_{}'.format(method_type.lower(), resource.Meta.name.lower())

    @classmethod
    def _parse_url_and_validate(cls, url):
        """
        Recieves a URL string and validates it using urlparse.

        Args:
            url: A URL string
        Returns:
            parsed_url: A validated URL
        Raises:
            BadURLException
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            final_url = parsed_url.geturl()
        else:
            raise BadURLException
        return final_url


class HypermediaResource(BaseResource, HTTPClient):
    """
    A HypermediaResource is similar to a BaseResource except
    it understands relationships between attributes that
    are URLs to related registered resources.
    """
    class Meta(BaseResource.Meta):
        # HypermediaResource requires a base_url attribute
        base_url = NotImplemented
        related_resources = ()

    def set_related_method(self, resource, value, base_url):
        """
        Using reflection, generate the related method and return it.
        """
        method_name = self.get_method_name(resource, 'get')

        url = resource.get_resource_url(
            resource, base_url=base_url
        )

        def get(self, method_type='get', method_name=method_name,
                url=url, valid_status_codes=self.Meta.valid_status_codes,
                resource=resource, data=None, uid=None, **kwargs):
            return self.call_api(
                method_type, method_name,
                url, valid_status_codes, resource,
                data, uid=uid, **kwargs)

        setattr(
            self, method_name,
            types.MethodType(get, self)
        )

    def match_url(self, resource, value):
        """
        Determine if an attribute is a url, and then
        determine if it matches any related resources.
        """
        # TODO obviously make this better
        if 'http://' in value:
            return True
        return False

    def set_attributes(self, **kwargs):
        """
        Similar to BaseResource.set_attributes except
        it will attempt to match URL strings with registered
        related resources, and build their get_* method and
        attach it to this resource.
        """
        if not self.Meta.related_resources:
            super(HypermediaResource, self).set_attributes(**kwargs)
        for field, value in kwargs.items():
            for resource in self.Meta.related_resources:
                if self.match_url(resource, value):
                    self.set_related_method(
                        resource, value, resource.Meta.base_url)
                elif field in self.Meta.attributes:
                    setattr(self, field, value)
