### BadURLException

An Invalid URL was parsed.

This usually happens when customising the `get_url` method.


### InvalidStatusCodeError

An invalid status code was returned for this resource.

The valid_status_codes tuple defined on resources determines which status codes are deemed "valid" when talking to the API.

InvalidStatusCodeError exceptions provide the following attributes:

`status_code` - the received status_code
`expected_status_codes` - a tuple of the status codes that were expected

These can be used to determine actions based on the status code response:

```python
try:
    client.get_resource(uid=1234)
except InvalidStatusCodeError as error:
    if error.status_code == 404:
        # Handle 404 responses
    elif error.status_code == 400:
        # Handle 400 responses
```


### MissingUidException

A uid attribute was missing!

If no `uid` attribute is supplied, this exception will raise.
