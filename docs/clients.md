Clients are models that wrap the interaction with an API service.

## class BaseClients

A simple HTTP API client.

**Example:**
```python
# my_client.py

from .my_resources import PersonResource

class StarWarsClient(clients.BaseClient):
    class Meta:
        name = 'Star Wars API Client'
        base_url = 'https://swapi.co/api/'
        resources = (
            PersonResource,
        )
```
**Usage:**
```bash
from .my_resources import PersonResource
from .my_client import StarWarsClient

swapi = StarWarsClient()
results_list = swapi.get_person(uid=1)

person = results_list[0]

isinstance(result, PersonResource)
>>> True
person.name
'Luke Skywalker'
```

### Meta Attributes

| Attribute   | Required | Type                      | Description                                                                         |
|:------------|:---------|:--------------------------|:------------------------------------------------------------------------------------|
| `base_url`  | Yes      | String                    | The Base URL for the HTTP API Service.                                              |
| `name`      | Yes      | String                    | The name of this client.                                                            |
| `resources` | Yes      | Tuple of Resource objects | A tuple of [Resource](/resource) classes that you want to register with this client |

### Generated Methods

A number of methods are generated on the client for each resource that is registered.

Based on the `methods` in a [Resource](/resources), the following python methods are created:

| Method   | HTTP method | Required Arguments | Example        |
|:---------|:------------|:-------------------|:---------------|
| `get`    | GET         | uid                | get_product    |
| `post`   | POST        | data               | post_product   |
| `put`    | PUT         | uid, data          | put_product    |
| `patch`  | PATCH       | uid, data          | patch_product  |
| `delete` | DELETE      | uid                | delete_product |

Each method has it's own required arguments:

| Argument | Type          | Example                                    |
|:---------|:--------------|:-------------------------------------------|
| `uid`    | string or int | `1` or `'some_slug'`                       |
| `data`   | dictionary    | `{'name': 'product', 'slug': 'some_slug'}` |

### Customisable Methods

The BaseClient has methods that can be subclassed and customised:

* [BaseClient.get_http_headers](/advanced/#customise-http-headers)
* [BaseClient.prepare_http_request](/advanced/#modify-http-request)


### Passing additional keyword arguments

Additional keyword arguments can be passed into the auto-generated methods and will appear in the following methods were applicable:

```
BaseResource.get_url
BaseClient.get_http_headers
BaseClient.prepare_http_request
HypermediaResource.get_http_headers
HypermediaResource.prepare_http_request
```

For example:

```python
client.get_product(product_id=123, product_country='US')
```

This allows for some flexibility when customising these methods. For more information on how to customise these methods, please read the [advanced](/advanced) guide.
