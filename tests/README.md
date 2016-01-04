# smartsheet-python-sdk unit tests

## Setup

From the root directory of this repository:

    $ python setup.py develop

## Running the tests

Again, from the root directory of this repository:

    $ python setup.py test


## Requirements

Some tests carry requirements. We're testing the real service here, not just using mocks. In order to do that, some configuration is necessary for some tests.

The test suite expects these environment variables to be present:

```shell
export SMARTSHEET_ACCESS_TOKEN="SSSSSSSSSSSSSSSSSSSSSSSSSS"
export LOG_CFG="debug" # optional
export SMARTSHEET_FIXTURE_USERS='{"admin":{"id":9999999999999999},"larry":{"id":0000000000000000},"curly":{"id":1111111111111111},"moe":{"id":2222222222222222}}'
```

**Please note:** the user nicknames (admin, larry, curly, moe) are not essential. However, valid IDs of users within the Smartsheet organization the access token belongs to are required.

In addition, reports tests will be skipped unless there is a report within the organization. The report will not be modified or deleted, but must exist in order to acceptance-test the API methods pertaining to Reports.

The `admin` user needs at least one Contact.

Finally, the user corresponding to `moe` needs to be a Licensed User. `larry` and `curly` do not need to be Licensed Users.
