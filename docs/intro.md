Getting Started
---------------

Beckett can be installed using [pip](https://pypi.python.org/pypi/pip/):

```bash
pip install beckett
```

Once installed, use the [Resources][resources] and [Clients][clients] documentation, or read through the concepts tutorial below to familiarise yourself with how Beckett works.

Concepts
--------

Beckett has two key base models that you'll need to configure in order to get started: **Resources** and **Clients**.

We'll using the following snippet of code to explain the basics concepts of Beckett:

```python
# my_client.py
from beckett import clients, resources


class PokemonResource(resources.BaseResource):
    class Meta(resources.BaseResource.Meta):
        name = 'Pokemon'
        identifier = 'id'
        attributes = (
            'id',
            'name',
        )
        methods = (
            'get',
        )


class PokemonClient(clients.BaseClient):
    class Meta(clients.BaseClient.Meta):
        base_url = 'https://pokeapi.co/api/v1/'
        resources = (
            PokemonResource,
        )
```

### Resources

A **Resource** object represents a single resource in your API service:

Resources have a series of attributes in their `Meta` class. These define the attributes and behaviour of a resource.

In this instance, we are naming our resource with the `name` attribute. We're defining a unique `identifier`
attribute to use when querying this resource, and setting a white list of `attributes` that we want to display on this resource.

A full list of available attributes can be found on the [Resources][resources] page.

### Clients

A typical Beckett-based API client only needs one **Client** instance. However, many clients can be used for versioning.

Clients can be configured using `Meta` class attributes, and inherits the defaults from the `BaseClient`.

In this instance we're setting the `base_url` of the API, as well as a list of `resources` that this API supports.

A list of available attributes can be found on the [Clients](/clients) page.

### Example Usage

We can now start calling the API!

```python
from my_client import PokemonClient

my_client = PokemonClient()
result = my_client.get_pokemon(1)[0]

isinstance(result, PokemonResource)
>>> True
result.name
'Bulbasaur'
```

Our client generates a collection of methods for every registered resource and understands how to properly call each method.

A lot of stuff is automatically generated here for us, so let's break it down and go through it line by line:

```python
my_client.get_pokemon(uid=1)
```

The `PokemonClient` will look at `PokemonResource` `methods` attribute to determine what HTTP methods are available on it. The default is:

```python
methods = (
        'get'
    )
```

The `PokemonResource` will also set the resource name as the lower-case of the `name` attribute. However, if this resource is called something different in the API we can set it ourselves in `PokemonResource`:

```python
resource = 'pokemons'
```

The `1` will be used by the `identifier` attribute on `PokemonResource` to help construct the URL when making HTTP calls.


That's the basics! We recommend reading the [resources][resources] and [clients][clients] documentation to understand the full breadth of possibilties with Beckett, or read the [advanced][advanced] tips guide for some more exciting features.

[resources]: /resources
[clients]: /clients
[advanced]: /advanced
