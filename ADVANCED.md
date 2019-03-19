# Advanced Topics for the Smartsheet SDK for Python

## Logging
There are three log levels currently supported by the Smartsheet Python SDK (in increasing order of verbosity):

**ERROR** - messages related to API or JSON serialization errors

**INFO** - messages about the API resources being requested

**DEBUG** - API request and response bodies and messages regarding object attributes that are changed by the SDK due to the nature of the API call being made

Use the logging facility's [basicConfig](https://docs.python.org/2/library/logging.html#logging.basicConfig) method to set your logging properties:

    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)

## Passthrough Option

If there is an API Feature that is not yet supported by the Python SDK, there is a passthrough option that allows you to pass and receive raw JSON objects.

To invoke the passthrough, your code can call one of the following four methods:

`response = client.Passthrough.get(endpoint, query_params)`

`response = client.Passthrough.post(endpoint, payload, query_params)`

`response = client.Passthrough.put(endpoint, payload, query_parameters)`

`response = client.Passthrough.delete(endpoint)`

* `endpoint`: The specific API endpoint you wish to invoke. The client object base URL gets prepended to the caller’s endpoint URL argument, so in the above `get` example, if endpoint is `'/sheets'` an HTTP GET is requested from the URL `https://api.smartsheet.com/2.0/sheets`
* `payload`: The data to be passed through, can be either a dictionary or string.
* `query_params`: An optional dictionary of query parameters.

All calls to passthrough methods return a JSON result. The `data` attribute contains the JSON result as a dictionary. For example, after a PUT operation the API's result message will be contained in `response.data['message']`. If you prefer raw JSON instead of a dictionary, you can use the `to_json()` method, for example `response.to_json()`. 

### Passthrough Example

The following example shows how to POST data to `https://api.smartsheet.com/2.0/sheets` using the passthrough method and a dictionary:

```python
payload = {"name": "my new sheet",
            "columns": [
              {"title": "Favorite", "type": "CHECKBOX", "symbol": "STAR"},
              {"title": "Primary Column", "primary": True, "type": "TEXT_NUMBER"}
            ]
          }

response = client.Passthrough.post('/sheets', payload)
```

## Testing

### All
1. Run `pytest`. Note, the integration and mock API tests will fail unless the mock server is running. See [Mock API Tests](#mock-api-tests) and [Integration Tests](#integration-tests)

### Integration Tests
1. Follow the instructions [here](tests/integration/README.md)
2. Run `pytest tests/integration`

### Mock API Tests
1. Clone the [Smartsheet SDK tests](https://github.com/smartsheet-platform/smartsheet-sdk-tests) repo and follow the instructions from the README to start the mock server
2. Run `pytest tests/mock_api`

## HTTP Proxy
The following example shows how to enable a proxy by providing a `proxies` argument when initializing the Smartsheet 
client.
 
```python
# Initialize client
proxies = {
    'https': 'http://127.0.0.1:8888'
}

smartsheet_client = smartsheet.Smartsheet(proxies=proxies)
```
## Working with Smartsheetgov.com Accounts
If you need to access Smartsheetgov you will need to specify the Smartsheetgov API URI as the base URI during creation 
of the Smartsheet client object. Smartsheetgov uses a base URI of https://api.smartsheetgov.com/2.0/. The base URI is 
defined as a constant (`smartsheet.__gov_base__`).

You can create a client using the Smartsheetgov.com URI using the api_base parameter:
```python
client = smartsheet.Smartsheet(api_base=smartsheet.__gov_base__)
```
