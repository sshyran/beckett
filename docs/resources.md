Introduction
------------

Resources are models relating to individual resources in an HTTP API.

## BaseResource

A simple representation of a resource.

**Example:**
```python
# myresources.py
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

```
**Usage:**
```bash
# Note: Data will usually come straight from the client method
>>> data = {'name': 'Tasty product', 'slug': 'sluggy'}
>>> product = Product(**data)
<Product | sluggy>
>>> product.name
'Tasty product'
```

### - attributes

TODO
