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

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
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
