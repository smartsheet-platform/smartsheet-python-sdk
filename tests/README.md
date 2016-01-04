# smartsheet-python-sdk-2 unit tests

## Setup

From the root directory of this repository:

    $ python setup.py develop

## Running the tests

Again, from the root directory of this repository:

    $ python setup.py test


## Requirements 

Some tests carry requirements. We're testing the real service here, not just using mocks. In order to do that, some configuration is necessary for some tests.

SMARTSHEET_FIXTURE_USERIDS=0000000000,1111111111111,2222222222

