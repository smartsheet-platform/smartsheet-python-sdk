# Smartsheet Python SDK [![Build Status](https://travis-ci.org/smartsheet-platform/smartsheet-python-sdk.svg)](https://travis-ci.org/smartsheet-platform/smartsheet-python-sdk) [![Coverage Status](https://coveralls.io/repos/smartsheet-platform/smartsheet-python-sdk/badge.svg?branch=master&service=github)](https://coveralls.io/github/smartsheet-platform/smartsheet-python-sdk?branch=master) [![PyPI version](https://badge.fury.io/py/smartsheet-python-sdk.svg)](https://badge.fury.io/py/smartsheet-python-sdk)

This library is intended to simplify connecting to the [Smartsheet API](https://smartsheet.redoc.ly) from Python applications.

## System Requirements
The SDK currently supports Python 3.6, 3.7, 3.8, 3.9, pypy, and pypy3. Integrations built on previous versions may still function, but Smartsheet recommends staying current with the Python end-of-life guidelines. 
**Note:** Python version 3.6 or higher is required for Unicode support, for example, if your Smartsheet data includes non-ASCII characters.  

The following packages are required.

* [requests](https://pypi.python.org/pypi/requests)
* [requests-toolbelt](https://pypi.python.org/pypi/requests-toolbelt)
* [six](https://pypi.python.org/pypi/six)
* [certifi](https://pypi.python.org/pypi/certifi)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

### Smartsheet Will Require TLS 1.1 or Higher Post 5/22/2018
There are many security vulnerabilities in SSL and early TLS versions. To remain compliant with PCI standards, most companies are now removing support for TLS 1.0.

Smartsheet Python SDK versions earlier than 1.3.0 do not support TLS 1.1. Once Smartsheet disables support for TLS 1.0 on 5/22/2018, any user who is still using an earlier version of the Python SDK will receive a SSL handshake error. Please upgrade your Smartsheet Python SDK, preferably to 1.3.2 by 5/22/2018 to avoid any impact.

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

## Getting Started
Getting started with the Python SDK is easy:

1.  Set **SMARTSHEET_ACCESS_TOKEN** in your environment. Find out more about [Authentication and Access Tokens](https://smartsheet.redoc.ly/tag/tokenDescription) in the Smartsheet API Documentation.

2.  Install the Smartsheet Python SDK from the [Python Package Index](http://pypi.python.org/pypi/smartsheet-python-sdk), or by using "pip install smartsheet-python-sdk".

3.  Import the smartsheet module: `import smartsheet`

4.  Refer to the [Smartsheet API Documentation](https://smartsheet.redoc.ly) for Python SDK usage examples.

See a sample application here: https://github.com/smartsheet-samples/python-read-write-sheet

## Advanced Topics
For details about logging, testing, how to use a passthrough option, and how to override HTTP client behavior, 
see [Advanced Topics](ADVANCED.md).

## Documentation
The Smartsheet API is documented here: https://smartsheet.redoc.ly

The Python SDK documentation can be viewed here: [http://smartsheet-platform.github.io/smartsheet-python-sdk/](http://smartsheet-platform.github.io/smartsheet-python-sdk/).

## Contributing
If you would like to contribute a change to the SDK, please fork a branch and then submit a pull request.

## Version Numbers
Starting from the v2.68.0 release, Smartsheet SDKs will use a new versioning strategy. Since all users are on the 
Smartsheet API 2.0, the SDK version numbers will start with 2. The 2nd number will be an internal reference number. The 
3rd number is for incremental changes.

For example, v2.68.0 means that you are using our 2.0 version of the API, the API is synced internally to a tag of 68, 
and then if there are numbers after the last decimal, that will indicate a minor change.

## Support
If you have any questions or issues with this SDK please post on StackOverflow using the tag ["smartsheet-api"](http://stackoverflow.com/questions/tagged/smartsheet-api) or contact us directly at api@smartsheet.com.

## Release Notes
Each release with notes is available for download on the [Github Releases page](https://github.com/smartsheet-platform/smartsheet-python-sdk/releases).
