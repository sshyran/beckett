Getting Started
---------------

Beckett can be installed using [pip](https://pypi.python.org/pypi/pip/):

```bash
pip install beckett
```

A Basic Client
--------------

Let's get to grips with Beckett by writing a basic client for communicating with [Swapi](https://swapi.co), the Star Wars API.

### Resources

The first thing we'll need to do is declare a [Resource][resources]. Swapi has [many resources](http://swapi.co/documentation), but let's create a resource for just [People](http://swapi.co/documentation#people):

```python
# my_resources.py
from beckett import resources


class PersonResource(resources.BaseResource):
    class Meta:
        name = 'Person'
        resource_name = 'people'
        identifier = 'url'
        attributes = (
            'name',
            'birth_year',
            'eye_color',
            'gender',
            'height',
            'mass',
            'url',
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )
```

Everything in Beckett is defined using Python classes and Meta classes. The definitions are then used by Beckett to construct the interface for communicating with the HTTP API for you. This is what we mean when we say Beckett is _"convention-based"_ - it understands RESTful HTTP APIs by default and will adapt the definitions you write to fit within it.

In the example above we've defined a series of properties for this resource. Let's talk about each of them now to understand what they mean:

* **name**: This string will be used by Beckett in Python `__repr__` and `__unicode__` methods.
* **resource_name**: Sometimes the resource name differs slightly because the plural of a resource is different from the singular. RESTful HTTP APIs conventionally use plural names in URIs. This property is not required and Beckett will try to guess the plural name of the **name** property. In this case it will guess `persons`, which doesn't fit with our API. Luckily, the **resource_name** attribute is provided so we can avoid this behaviour if we want.
* **identifier**: This attribute is used to determine the unique identifying attribute of the resource. It will be used in Python `__repr__` and `__unicode__` methods.
* **attributes**: This is a tuple of strings, declaring the attributes you want to see from the resource when it is generated. If you look at [an example API response](http://swapi.co/api/people/1/) from Swapi, you will see these attributes listed. You can read more about [Resource attributes here](resources/#resource-properties). You can use this to white-list specific attributes.
* **valid_status_codes**: This is a tuple of integers, declaring the HTTP response codes you consider "valid". Some HTTP APIs behave differently and certain responses are expected, such as `202` or `404`. If an HTTP response code is received that is not in the list, Beckett will raise an exception.
* **methods**: This is a tuple of strings, declaring the HTTP methods that can be used with this resource. Beckett will use this tuple to generate python methods.

You can read more about resources on the [Resources][resources] page.

### Client

Now that we've got our Resource created, let's build a Client to start using it.

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

Just like the Resource, we can declare a bunch of properties on our Client:

* **name** - This property will be used in HTTP headers as well as in `__repr__` and `__unicode__` methods.
* **base_url** - This is the base url for the API. Beckett will use this to construct the URL when making HTTP requests.
* **resources** - This is a tuple of `Resource` classes that you want the client to communicate with.

You can read more about clients on the [Clients][clients] page.

### Make HTTP calls!

We can now start calling the API!

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

Beckett has generated a `get_person` method because it has read the `PersonResource` and seen which HTTP methods it wants. This method conventionally takes a single parameter `uid`. These generated methods also except arbitrary keyword arguments for customisation. You can read more about this in the [advanced][advanced] section.

The response is a list of `PersonResource` instances. Beckett infers the JSON response and transforms the JSON values into attributes on each instance, so we can query `person.name`.


### Further reading

This guide has demonstrated the basics of Beckett, using most of the conventionally-based stuff. However, most HTTP APIs are not always perfectly RESTful. Luckily, Beckett is designed to be flexible enough to provide ways to support other HTTP APIs, we recommend reading the [advanced][advanced] guide if you're looking to modify Beckett's behaviour.

[resources]: /resources
[clients]: /clients
[advanced]: /advanced
