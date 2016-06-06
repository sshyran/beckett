# -*- coding: utf-8 -*-

from .constants import DEFAULT_VALID_STATUS_CODES


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
        # The key with which you uniquely identify this resource.
        identifier = 'id'
        # Acceptable attributes that you want to display in this resource.
        attributes = (identifier,)
        # HTTP status codes that are considered "acceptable"
        # when calling this resource
        acceptable_status_codes = DEFAULT_VALID_STATUS_CODES

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
        """
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                setattr(self, field, value)
