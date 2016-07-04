Clients are models that wrap the interaction with an API service.

## class BaseClients

A simple HTTP API client.

**Example:**
```python
# clients.py
from beckett.clients import BaseClient
from .resources import ProductResource

class MyClient(BaseClient):

    class Meta(BaseClient.Meta):
        base_url = 'http://myapi.com/api'
        resources = (
            ProductResource,
        )

```
**Usage:**
```bash
# Note: Data will usually come straight from the client method
>>> client = MyClient()
# get_, post_, put_, delete_, patch_ methods are auto generated for resources
>>> product = client.get_product(uid='product_slug')
>>> product.name
'Tasty product'
```

### Generated Methods

A number of methods are generated on the client when resources are registered.

Based on the `methods` in a [Resource](/resources), the following methods are created:

| Method   | HTTP method | Arguments* | Example        |
|:---------|:------------|:-----------|:---------------|
| `get`    | GET         | uid        | get_product    |
| `post`   | POST        | data       | post_product   |
| `put`    | PUT         | uid, data  | put_product    |
| `patch`  | PATCH       | uid, data  | patch_product  |
| `delete` | DELETE      | uid        | delete_product |

Additional keyword arguments can be passed and will appear in the following methods were applicable:

```
BaseResource.get_url
HTTPClient.get_http_headers
HTTPClient.prepare_http_request
HypermediaResource.get_http_headers
HypermediaResource.prepare_http_request
```

This allows for some flexibility when customising these methods.

### Method arguments

| Argument | Type          | Example                                    |
|:---------|:--------------|:-------------------------------------------|
| `uid`    | string or int | `1` or `'some_slug'`                       |
| `data`   | dictionary    | `{'name': 'product', 'slug': 'some_slug'}` |

### - Meta Attributes

| Attribute   | Required | Type                      | Description                                                                         |
|:------------|:---------|:--------------------------|:------------------------------------------------------------------------------------|
| `base_url`  | Yes      | String                    | The Base URL for the HTTP API Service.                                              |
| `resources` | Yes      | Tuple of Resource objects | A tuple of [Resource](/resource) classes that you want to register with this client |
