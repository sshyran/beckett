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
        methods = (
            'get',
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

| Attribute            | Required | Type             | Description                                                                                                                                                                                                              |
|:---------------------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`               | Yes      | String           | The name of this resource instance. Usually a singular noun.                                                                                                                                                             |
| `resource_name`      | No       | String           | The name of this resource used in the url. Usually a plural noun. If not set, we'll attempt to make a pluralised version of the `name` attribute.                                                                        |
| `identifier`         | Yes      | Int/String       | The key attribute that can be used to identify this attribute. Used when referring to related resources.                                                                                                                 |
| `attributes`         | Yes      | Tuple of Strings | A tuple list of strings, referring to the key attributes that you want to populate the resource instances with. You can use this for whitelisting and versioning changes in your API.                                    |
| `valid_status_codes` | No       | Tuple of Ints    | A tuple list of integers, referring to the HTTP status codes that are considered "acceptable" when communicating with this resource. If a status code is received that does not match this set, an error will be raised. |
| `methods`            | No       | Tuple of Strings | A tuple list of strings, referring to the HTTP methods that can be used with this resource. For each method, a python method will be generated on the client that registers this resource.                               |
| `pagination_key`     | No       | String           | The key used to look up paginated responses. The value of this key in an API response will be rendered into instances of this resource. See [Pagination](/advanced/#pagination) for more help.                           |

### - URL generation

Beckett attempts to auto generate URLs based on good RESTful style URI schemes. If you do nothing to manipulate the URLs, Beckett will call the following URLs for the related HTTP Methods:

| Method | URI Structure                                      | Example                            |
|:-------|:---------------------------------------------------|:-----------------------------------|
| GET    | Client.Meta.base_url/Resource.Meta.plural_name/uid | `http://myapi.com/api/products/1/` |
| PUT    | Client.Meta.base_url/Resource.Meta.plural_name/uid | `http://myapi.com/api/products/1/` |
| POST   | Client.Meta.base_url/Resource.Meta.plural_name     | `http://myapi.com/api/products`    |
| PATCH  | Client.Meta.base_url/Resource.Meta.plural_name/uid | `http://myapi.com/api/products/1/` |
| DELETE | Client.Meta.base_url/Resource.Meta.plural_name/uid | `http://myapi.com/api/products/1/` |

URL structures can be completely modified by subclassing the `get_single_resource_url` method on Resources. See [customising resource urls](advanced/#customising-resource-urls) for more information.

## class HypermediaResource

A simple representation of a resource that supports hypermedia links to related resources.

**Example:**
```python
# myresources.py
from beckett.resources import HypermediaResource

class Designer(HypermediaResource):
    class Meta(HypermediaResource.Meta):
        name = 'Designer'
        identifier = 'slug'
        attributes = (
            'slug',
            'name',
        )
        methods = (
            'get',
        )
        # Additional required attributes
        base_url = 'http://myapi.com/api'
        related_resources = ()


class Product(HypermediaResource):

    class Meta(HypermediaResource.Meta):
        name = 'Product'
        identifier = 'slug'
        attributes = (
            'slug',
            'name',
            'price',
            'discount'
        )
        methods = (
            'get',
        )
        # Additional required attributes
        base_url = 'http://myapi.com/api'
        related_resources = (
            Designer,
        )

```
**Usage:**
```bash
# Note: Data will usually come straight from the client method
>>> data = {'name': 'Tasty product', 'slug': 'sluggy', 'designer': 'http://myapi.com/api/designers/some-designer'}
>>> product = Product(**data)
>>> product.get_designer(uid='some-designer')
<Designer | Some Designer>
```

### - Meta Attributes

HypermediaResource has two additional, required, attributes that are essential for making hypermedia work

| Attribute           | Required | Type             | Description                                                                                                     |
|:--------------------|:---------|:-----------------|:----------------------------------------------------------------------------------------------------------------|
| `base_url`          | Yes      | String           | The base url of this resource                                                                                   |
| `related_resources` | Yes      | Tuple of classes | A tuple of classes that are related to this resource, and should be expected in the JSON response from the API. |
