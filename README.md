# Smartsheet Python SDK [![Build Status](https://travis-ci.org/smartsheet-platform/smartsheet-python-sdk.svg)](https://travis-ci.org/smartsheet-platform/smartsheet-python-sdk) [![Coverage Status](https://coveralls.io/repos/smartsheet-platform/smartsheet-python-sdk/badge.svg?branch=master&service=github)](https://coveralls.io/github/smartsheet-platform/smartsheet-python-sdk?branch=master) [![PyPI version](https://badge.fury.io/py/smartsheet-python-sdk.svg)](https://badge.fury.io/py/smartsheet-python-sdk)

This library is intended to simplify connecting to the [Smartsheet API](http://smartsheet-platform.github.io/api-docs/) from Python applications.

## System Requirements
The SDK currently supports Python 2.7, 3.4, 3.5, 3.6, pypy, and pypy3.  
**Note** that Python version 3.4 or higher is required for Unicode support. (E.g. if your Smartsheet data includes non-ASCII characters.)  

The following packages are required.

* [requests](https://pypi.python.org/pypi/requests)
* [requests-toolbelt](https://pypi.python.org/pypi/requests-toolbelt)
* [six](https://pypi.python.org/pypi/six)
* [certifi](https://pypi.python.org/pypi/certifi)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

### Smartsheet Will Require TLS 1.1 or Higher Post 5/22/2018
There are many security vulnerabilities in SSL and early TLS versions. To remain compliant with PCI standards, most companies are now removing support for TLS 1.0.

Smartsheet Python SDK versions earlier than 1.3.0 do not support TLS 1.1. Once Smartsheet disables support for TLS 1.0 on 5/22/2018 any user who is still using an earlier version of the Python SDK will receive a SSL handshake error. Please upgrade your Smartsheet Python SDK, preferably to 1.3.2 by 5/22/2018 to avoid any impact.

To upgrade a current installation using pip:

`$ pip install smartsheet-python-sdk --upgrade`

If this is your first time installing the Python SDK, follow the installation steps in the following section.

## Installation
The SDK can be installed by using a package manager (pip) or manually by downloading the SDK directly from Git. These two steps are outlined below.

### Install with pip
If unfamiliar with pip, please review the [pip documentation](http://www.pip-installer.org/).

This SDK's Python package is called **smartsheet-python-sdk**. To install using pip:

`$ pip install smartsheet-python-sdk`

### Install manually
To install this SDK manually, download the source code from [GitHub](https://github.com/smartsheet-platform/smartsheet-python-sdk) and then run:

`$ python setup.py install`

## Logging
There are three log levels currently supported by the Smartsheet Python SDK (in increasing order of verbosity):

**ERROR** - messages related to API or JSON serialization errors

**INFO** - messages about the API resources being requested

**DEBUG** - API request and response bodies and messages regarding object attributes that are changed by the SDK due to the nature of the API call being made

Use the logging facility's [basicConfig](https://docs.python.org/2/library/logging.html#logging.basicConfig) method to set your logging properties:

    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)

## Documentation
The Smartsheet API is documented here: http://smartsheet-platform.github.io/api-docs/

The Python SDK documentation can be viewed here: [http://smartsheet-platform.github.io/smartsheet-python-sdk/](http://smartsheet-platform.github.io/smartsheet-python-sdk/).

## Getting Started
Getting started with the Python SDK is easy:

1.  Set **SMARTSHEET_ACCESS_TOKEN** in your environment. Find out more about [Authentication and Access Tokens](https://smartsheet-platform.github.io/api-docs/index.html#authentication-and-access-tokens) in the Smartsheet API Documentation.

2.  Install the Smartsheet Python SDK from the [Python Package Index](http://pypi.python.org/pypi/smartsheet-python-sdk), or by using "pip install smartsheet-python-sdk".

3.  Import the smartsheet module: `import smartsheet`

4.  Refer to the [Smartsheet API Documentation](https://smartsheet-platform.github.io/api-docs/?python#python-sample-code) for Python SDK usage examples.

See a sample application here: https://github.com/smartsheet-samples/python-read-write-sheet

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

## Working with Smartsheetgov.com Accounts
If you need to access Smartsheetgov you will need to specify the Smartsheetgov API URI as the base URI during creation 
of the Smartsheet client object. Smartsheetgov uses a base URI of https://api.smartsheetgov.com/2.0/. The base URI is 
defined as a constant (`smartsheet.__gov_base__`).

You can create a client using the Smartsheetgov.com URI using the api_base parameter:
```python
client = smartsheet.Smartsheet(api_base=smartsheet.__gov_base__)
```

## Support
If you have any questions or issues with this SDK please post on StackOverflow using the tag ["smartsheet-api"](http://stackoverflow.com/questions/tagged/smartsheet-api) or contact us directly at api@smartsheet.com.

## Contributing
If you would like to contribute a change to the SDK, please fork a branch and then submit a pull request.

### Running the Tests
#### All
1. Run `pytest`. Note, the integration and mock API tests will fail unless the mock server is running. See [Mock API Tests](#mock-api-tests) and [Integration Tests](#integration-tests)

#### Integration Tests
1. Follow the instructions [here](tests/integration/README.md)
2. Run `pytest tests/integration`

#### Mock API Tests
1. Clone the [Smartsheet SDK tests](https://github.com/smartsheet-platform/smartsheet-sdk-tests) repo and follow the instructions from the README to start the mock server
2. Run `pytest tests/mock_api`

## Release Notes
Each release with notes is available for download on the [Github Releases page](https://github.com/smartsheet-platform/smartsheet-python-sdk/releases).
