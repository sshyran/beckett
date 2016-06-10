Resources are models relating to individual resources in an HTTP API.

## class BaseResource

A simple representation of a resource.

**Example:**
```python
# myresources.py
from beckett.resources import BaseResource

class Product(BaseResource):

    class Meta(BaseResource.Meta):
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

### - Meta Attributes

| Attribute                 | Required | Type             | Description                                                                                                                                                                                                              |
|:--------------------------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`                    | Yes      | String           | The name of this resource instance. Usually a singular noun.                                                                                                                                                             |
| `resource_name`           | No       | String           | The name of this resource used in the url. Usually a plural noun. If not set, we'll attempt to make a pluralised version of the `name` attribute.                                                                        |
| `identifier`              | Yes      | Int/String       | The key attribute that can be used to identify this attribute. Used when referring to related resources.                                                                                                                 |
| `attributes`              | Yes      | Tuple of Strings | A tuple list of strings, referring to the key attributes that you want to populate the resource instances with. You can use this for whitelisting and versioning changes in your API.                                    |
| `acceptable_status_codes` | No       | Tuple of Ints    | A tuple list of integers, referring to the HTTP status codes that are considered "acceptable" when communicating with this resource. If a status code is received that does not match this set, an error will be raised. |
| `methods`                 | No       | Tuple of Strings | A tuple list of strings, referring to the HTTP methods that can be used with this resource. For each method, a python method will be generated on the client that registers this resource.                               |
