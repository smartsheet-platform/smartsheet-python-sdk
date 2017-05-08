[![Build Status](https://travis-ci.org/smartsheet-platform/smartsheet-python-sdk.svg)](https://travis-ci.org/smartsheet-platform/smartsheet-python-sdk) [![Coverage Status](https://coveralls.io/repos/smartsheet-platform/smartsheet-python-sdk/badge.svg?branch=master&service=github)](https://coveralls.io/github/smartsheet-platform/smartsheet-python-sdk?branch=master)

# Smartsheet Python SDK
This library is intended to simplify connecting to the [Smartsheet API](http://smartsheet-platform.github.io/api-docs/) from Python applications.

## System Requirements
The SDK currently supports Python 2.7, 3.3, 3.4, 3.5, 3.6, pypy, and pypy3.
The following packages are required.

* [requests](https://pypi.python.org/pypi/requests)
* [requests-toolbelt](https://pypi.python.org/pypi/requests-toolbelt)
* [six](https://pypi.python.org/pypi/six)
* [certifi](https://pypi.python.org/pypi/certifi)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

## Installation
The SDK can be installed by using a package manager (pip) or manually by downloading the SDK directly from Git. These two steps are outlined below.

### Install with pip
If unfamiliar with pip, please review the [pip documentation](http://www.pip-installer.org/).

This SDK's Python package is called **smartsheet-python-sdk**. To install using pip:

`$ pip install smartsheet-python-sdk`

### Install manually
To install this SDK manually, download the source code from [GitHub](https://github.com/smartsheet-platform/smartsheet-python-sdk) and then run:

`$ python setup.py install`

## Documentation
The Smartsheet API is documented here: http://smartsheet-platform.github.io/api-docs/

The Python SDK documentation can be viewed here: [http://smartsheet-platform.github.io/smartsheet-python-sdk/](http://smartsheet-platform.github.io/smartsheet-python-sdk/).

## Getting Started
Getting started with the Python SDK is easy:

1.  Set **SMARTSHEET_ACCESS_TOKEN** in your environment. Find out more about getting [direct API access](https://smartsheet-platform.github.io/api-docs/index.html#direct-api-access) in the Smartsheet API Documentation.

2.  Install the Smartsheet Python SDK from the [Python Package Index](http://pypi.python.org/pypi/smartsheet-python-sdk), or by using "pip install smartsheet-python-sdk".

3.  Import the smartsheet module: `import smartsheet`

4.  Refer to the [Smartsheet API Documentation](https://smartsheet-platform.github.io/api-docs/?python#python-sample-code) for Python SDK usage examples.

See a sample application here: https://github.com/smartsheet-samples/python-read-write-sheet

## Support
If you have any questions or issues with this SDK please post on StackOverflow using the tag ["smartsheet-api"](http://stackoverflow.com/questions/tagged/smartsheet-api) or contact us directly at api@smartsheet.com.

## Contributing
If you would like to contribute a change to the SDK, please fork a branch and then submit a pull request.

## Release Notes
Each release with notes is available for download on the [Github Releases page](https://github.com/smartsheet-platform/smartsheet-python-sdk/releases).
