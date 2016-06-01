# -*- coding: utf-8 -*-


class BaseModel(object):
    """
    A simple representation of a resource.

    Usage:

        from beckett.models import BaseModel

        class Product(BaseModel):

            class Meta:
                name = 'Product'
                identified = 'slug'
                attributes = (
                    'slug',
                    'name',
                    'price',
                    'discount'
                )

        # Data will usually come straight from the client method
        >>> data = {'name': 'Tasty product'}
        >>> product = Product(**data)
        >>> product.name
        'Tasty product'

    """

    class Meta:
        name = 'Resource'
        identifier = 'id'
        attributes = (identifier,)

    def __init__(self, *args, **kwargs):
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                setattr(self, field, value)

    def __str__(self):
        return '<{} | {}>'.format(
            self.Meta.name, getattr(self, self.Meta.identifier))
