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
## Event Reporting
The following sample demonstrates 'best' practices for enumerating events using the Smartsheet Event Reporting feature. 
All enumerations must begin using the `since` parameter to the `list_events` method. Specify `0` as an argument 
(i.e. `since=0`) if you wish to begin enumeration at the beginning of stored event history. A more common scenario 
would be to enumerate events over a certain time frame by providing an ISO 8601 formatted or numerical (UNIX epoch) 
date as an argument to `list_events`. In this sample, events for the previous 7 days are enumerated.

After the initial list of events is returned, you should only continue to enumerate events if the `more_available` flag
in the previous response indicates that more data is available. To continue the enumeration, supply an argument to the
`stream_position` parameter to the `list_events` method (`since` must be unset or `None`). The `stream_position` 
argument you supply was provided by the `next_stream_position` attribute of the previous response.

Many events have additional information available as a part of the event. That information can be accessed using 
the Python dictionary stored in the `additional_details` attribute (Note that attributes of the `additional_details` 
dictionary use camelCase/JSON names, e.g. `sheetName` not `sheet_name`). An example is provided for `sheetName` 
below. Information about the additional details provided can be found [here.](https://smartsheet-platform.github.io/event-reporting-docs/) 

```python
# this example is looking specifically for new sheet events
def find_new_sheet_events_in_list(events_list):
    # enumerate all events in the list of returned events
    for event in events_list.data:
        # find all created sheets
        if event.object_type == smartsheet.models.enums.EventObjectType.SHEET and event.action == smartsheet.models.enums.EventAction.CREATE:
            # additional details are available for some events, they can be accessed as a Python dictionary
            # in the additional_details attribute
            print(event.additional_details['sheetName'])


smartsheet_client = smartsheet.Smartsheet()
smartsheet_client.errors_as_exceptions()

# all event enumerations start by using the `since` parameter
last_week = datetime.now() - timedelta(days=7)
# this example looks at the previous 7 days of events by providing a `since` argument set to last week's date in ISO format
events_list = smartsheet_client.Events.list_events(since=last_week.isoformat(), max_count=1000)
find_new_sheet_events_in_list(events_list)

# continue enumeration using the stream_position, if the previous response indicates that more data is available.
while events_list.more_available:
    events_list = smartsheet_client.Events.list_events(stream_position=events_list.next_stream_position, max_count=10000,
                                        numeric_dates=True)
    find_new_sheet_events_in_list(events_list)
```
## Working with Smartsheetgov.com Accounts
If you need to access Smartsheetgov you will need to specify the Smartsheetgov API URI as the base URI during creation 
of the Smartsheet client object. Smartsheetgov uses a base URI of https://api.smartsheetgov.com/2.0/. The base URI is 
defined as a constant (`smartsheet.__gov_base__`).

You can create a client using the Smartsheetgov.com URI using the api_base parameter:
```python
client = smartsheet.Smartsheet(api_base=smartsheet.__gov_base__)
```
