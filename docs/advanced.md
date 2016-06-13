## Customising Resource URLs

If you have domain-specific URLs you can modify them individually per Resource.

If we have a resource that requires a URL structure like so:

```
https://myapi.com/api/v1/product?id=123&country=GB
```

Which would require:

* The URL to accept an `id` query parameter
* An additional `country` parameter

Then we can customise our `ProductResource` like so:

```python
class Product(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Product'
        identifier = 'slug'
        attributes = (
            'slug',
        )
        methods = (
            'get',
        )

    @classmethod
    def get_single_resource_url(cls, url, uid, **kwargs):
        """
        Our customised URL.
        """
        return '{}/products/?id={}&country={}'.format(
            url,
            uid,
            kwargs.get('country')
        )
```

When we go to use the resource in our client we simply call the `get_method` with additional parameters:

```python
client.get_product(uid=1, country='GB')
>>> <Product | 1>
```

## Response formats

TODO

## Pagination

Pagination is supported by Beckett. Because there are many forms of pagination, we recommend customising the `get_single_resource_url` method on your resource, similarly to the [example above](/advanced/#customising-resource-urls). Because all keyword arguments are passed to this method, you can call the page like so:

```python
resources = client.get_resource(page=2)
```

and format the URL in the code like so:

```python
@classmethod
def get_single_resource_url(cls, url, uid, **kwargs):
    if kwargs.get('page'):
        return '{}?page={}'.format(
            url,
            kwargs.get('page')
        )
```

When rendering responses into your resource instances, Beckett will perform the following steps:

1. Is the response a list? If yes - render each item in the list as a Resource.
2. Is the `pagination_key` value in this resource declared? If yes, look it up in the response object and render that list into resources.
3. Attempt to render the whole response as a single resource instance.

### pagination_key

In your Resource, declare a pagination_key attribute:

```python

```python
class Product(BaseResource):

    class Meta(BaseResource.Meta):
        ...
        pagination_key = 'objects'
```

To correspond with a paginated API response like so:

```json
{
    "next": "http://myapi.com/api/resources?page=2",
    "objects": [
        {
            "name": "Resource one"
        },
        {
            "name": "Resource two"
        }
    ]
}
```
