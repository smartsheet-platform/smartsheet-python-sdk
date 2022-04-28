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

If there is an API feature that is not yet supported by the Python SDK, there is a passthrough option that allows you to pass and receive raw JSON objects.

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

### Integration Tests
1. Follow the instructions [here](tests/integration/README.md)
2. Run `pytest tests/integration`

### Mock API Tests
**NOTE:** the mock API tests will fail unless the mock server is running.
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
The following sample demonstrates best practices for consuming the event stream from the Smartsheet Event Reporting 
feature.

The sample uses the `smartsheet_client.Events.list_events` method to request a list of events from the stream. The first
request sets the `since` parameter with the point in time (i.e. event occurrence datetime) in the stream from which to 
start consuming events. The `since` parameter can be set with a datetime value that is either formatted as ISO 8601 
(e.g. 2010-01-01T00:00:00Z) or as UNIX epoch (in which case the `numeric_dates` parameter must also be set to `True`.
By default the `numeric_dates` parameter is set to `False`).
 
To consume the next list of events after the initial list of events is returned, set the `stream_position` parameter 
with the `next_stream_position` property obtained from the previous request and don't set the `since` parameter with 
any values. This is because when using the `list_events` method, either the `since` parameter or the `stream_position`
parameter should be set, but never both.

Note that the `more_available` property in a response indicates whether more events are immediately available for 
consumption. If events are not immediately available, they may still be generating so subsequent requests should keep
using the same `stream_position` value until the next list of events is retrieved.

Many events have additional information available as a part of the event. That information can be accessed using 
the Python dictionary stored in the `additional_details` property (Note that values of the `additional_details` 
dictionary use camelCase/JSON names, e.g. `sheetName` not `sheet_name`). Information about the additional details 
provided can be found [here.](https://smartsheet.redoc.ly/tag/eventsDescription) 

```python
# this example is looking specifically for new sheet events
def print_new_sheet_events_in_list(events_list):
    # enumerate all events in the list of returned events
    for event in events_list.data:
        # find all created sheets
        if event.object_type == smartsheet.models.enums.EventObjectType.SHEET and event.action == smartsheet.models.enums.EventAction.CREATE:
            # additional details are available for some events, they can be accessed as a Python dictionary
            # in the additional_details attribute
            print(event.additional_details['sheetName'])


smartsheet_client = smartsheet.Smartsheet()
smartsheet_client.errors_as_exceptions()

# begin listing events in the stream starting with the `since` parameter
last_week = datetime.now() - timedelta(days=7)
# this example looks at the previous 7 days of events by providing a `since` argument set to last week's date in ISO format
events_list = smartsheet_client.Events.list_events(since=last_week.isoformat(), max_count=1000)
print_new_sheet_events_in_list(events_list)

# continue listing events in the stream by using the stream_position, if the previous response indicates that more 
# data is available.
while events_list.more_available:
    events_list = smartsheet_client.Events.list_events(stream_position=events_list.next_stream_position, max_count=10000,
                                        numeric_dates=True)
    print_new_sheet_events_in_list(events_list)
```

## Working with Smartsheetgov.com Accounts

If you need to access Smartsheetgov you will need to specify the Smartsheetgov API URI as the base URI during creation 
of the Smartsheet client object. Smartsheetgov uses a base URI of https://api.smartsheetgov.com/2.0/. The base URI is 
defined as a constant (`smartsheet.__gov_base__`).

You can create a client using the Smartsheetgov.com URI using the api_base parameter:
```python
client = smartsheet.Smartsheet(api_base=smartsheet.__gov_base__)
```

## Working With Smartsheet Regions Europe Accounts

If you need to access Smartsheet Regions Europe you will need to specify the Smartsheet.eu API URI as the base URI during creation of the Smartsheet client object. Smartsheet.eu uses a base URI of https://api.smartsheet.eu/2.0/. The base URI is defined as a constant (`smartsheet._eu_base_`).

You can create a client using the Smartsheet.eu URI using the api_base parameter:
```python
client = smartsheet.Smartsheet(api_base=smartsheet._eu_base_)
```