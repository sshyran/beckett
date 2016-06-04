Introduction
------------

Beckett is a framework for developing **flexible API Clients for HTTP API services**.

Beckett provides the base tools for creating resources and specifying how they should look, how their API acts, and
what attributes are valid. Beckett lets you provide **typed stateless instances** of your resources and control the changes
that are made to them.

Beckett also helps you quickly create a client that understands what response codes are valid, how to paginate resources
and also what response formats to expect.

Beckett works best with **hypermedia** response formats such as [HAL](http://stateless.co/hal_specification.html) and [JSONAPI](http://jsonapi.org), and will automagically transform hypermedia links into **methods** for communicating with related resources, as well as CRUD actions on the resources it gets.

Concepts
--------

Beckett has two key base models that you'll need to configure in order to get started: **Resources** and **Clients**.

### Resources

A **Resource** object represents a single resource in your API service:

```python
# resources.py
from beckett import resources

class PokemonResource(resources.BaseResource):
    class Meta:
        name = 'Pokemon'
        identifier = 'id'
        attributes = (
            'id',
            'name',
        )
```

Resources have a series of attributes in their `Meta` class. These define the attributes of a resource.

In this instance, we are naming our resource with the `name` attribute. Defining unique `identifier`
attribute to use when querying this resource, and setting a white list of `attributes` that we want to display on this resource.

A full list of available attributes can be found on the [Resources](/resources) page.

### Clients

A typical Beckett-based API client only needs one **Client** instance. Here we define the base url of our API:

```python
# clients.py
from beckett import clients
from .resources import PokemonResource

class PokemonClient(clients.BaseClient):
    class Meta:
        base_url = 'https://pokeapi.co/api/v1/'
        resources = (
            PokemonResource,
        )
```

Clients can be configured using `Meta` class attributes, and inherits the defaults from the `BaseClient`.

In this instance we're setting the `base_url` of the API, as well as a list of `resources` that this API supports.

A list of available attributes can be found on the [Clients](/clients) page.

### Example Usage

We can now start calling the API!

```python
from clients import PokemonClient
from resources import PokemonResource

my_client = PokemonClient()
result = my_client.get_pokemon(1)

isinstance(result, PokemonResource)
>>> True
result.name
'Bulbasaur'
```

Our client generates a collection of methods for every registered resource and understands how to properly call each method.

A lot of stuff is automatically generated here for us, so let's break it down and go through it line by line:

```python
my_client.get_pokemon(1)
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
