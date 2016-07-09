### BadURLException

An Invalid URL was parsed.

This usually happens when customising the `get_url` method.


### InvalidStatusCodeError

An invalid status code was returned for this resource.

The valid_status_codes tuple defined on resources determines which status codes are deemed "valid" when talking to the API.


### MissingUidException

A uid attribute was missing!

If no `uid` attribute is supplied, this exception will raise.
