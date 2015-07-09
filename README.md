Smartsheet Python SDK
=====================

Python client library for version 1.1 of the Smartsheet API.
The Smartsheet API is documented at:
https://www.smartsheet.com/developers/api-documentation

**NOTE: Please note that this SDK is pre-alpha.  It is incomplete, has not been rigorously tested, and is a work in progress.  See below for known issues, feature gaps, and a rough roadmap.  If you need a missing feature urgently, you are strongly encouraged to build it and submit a pull request.  If you need a feature and can't or don't want to build it, please create an issue for it.  Thanks for understanding.**

# What Works

Some of the Smartsheet API is accessible via this library.  Presently,
the list of what works is much shorter than the list of what doesn't
work yet.  Hopefully that will change.  Here's what currently works:

* Convenience wrapper around raw requests
* Fetch the information about a specific user
* Fetch the list of sheets available
* Fetch a Sheet (by its permalink or ID)
  * Specify whether or not to include discussions, attachments, formats, or filters in the returned Sheet
* Read/write access to the Cells in the Sheet
* The Sheet can be treated as a 2-dimensional array:
  * Read access: `print sheet[rowNumber][columnIndex]`
  * Write access: `sheet[rowNumber][columnIndex] = "Some value"`
* Add Rows (one at a time or multiple-at-a-time) to a Sheet.
* Delete Rows (one at a time)
* Create and Delete Sheets
* Download attachments (from the sheet, rows, or discussion comments)
* Upload a new version of an existing attachment
  * This is distinct from replacing the existing attachment
* Fetch the history of a Cell
* Operate in read-only mode
  * Prevents any changes from being made to the Sheet on the server

The tests in the `tests/` directory are starting to become a decent set of
examples of how the library can be used.

# What Doesn't Work (that might surprise you)

Basically, if a feature of the API is not listed above, it probably 
hasn't been implemented yet.  However, there are some surprising gaps
that are covered here.

* When fetching a Sheet, pagination isn't supported
* Moving Rows
* Replacing an attachment doesn't work, only uploading a new version
* Can't issue HEAD requests on the S3 link used to download attachments
  * These result in a 403 error even thought the S3 docs say that GET and HEAD use the same permissions object

# TODO

* Add more test cases
  * There are some empty test cases as placeholders
* Continue adding support for more of the version 1.1 API
  * Move Rows (individually or a contigous block)
  * Change Row indentation (individually or in a group)
  * Bare minimum support for Workspaces and Folders
  * Bare minimum support for Reports
  * Bare minimum support for Search
  * Administrative operations
    * Manage users and groups
    * Backup sheets
  * Formats
  * Filters
  * Discussions
  * Discussion Comments
  * Lots more
* Make sheet.save() save any local changes to the server
* Add mechanism to tune the aggressiveness of cached reads.
  * Right now, a Row read will fetch only that Row.
    * That's the least aggressive policy.
    * The most aggressive would be to fetch all of the Rows in the Sheet
  * Refetching the entire Sheet when doing cache refills is probably the way to go
    * Maybe only when caching is enabled

# Roadmap

Eventually, the client should provide something of a relaxed ActiveRecord-like
interface.  In this model, changes could be made to a local copy of the
Sheet, and then synchronized with the Smartsheet servers by calling
a .save() method on either the Sheet or whatever object was changed. In
this model, calling .save() on the Sheet (or any object that can contain
other objects) would result in the saving of changes to any "contained" objects.
There are scenarios where it would be preferable to have all changes immediately
applied to the Sheet on the Smartsheet servers (instead of waiting until .save()
is called).  At present, certain operations (such as Sheet.addRow() are applied
to the on-server Sheet immediately, while others remain local until saved).

That's the goal, it may take a while to get there.

# Code Guidelines

In general, follow PEP 8 (https://www.python.org/dev/peps/pep-0008/),
the Python Style Guide.  Try valiantly to limit lines to 80 characters
or less.

There's really only one hard rule:  do not use tabs for indentation.

# Caching

It might be tempting to skip over this section.  _Don't._  Making sense of
how the SDK handles caching is going to influence the way you use the SDK.

When working with the Smartsheet API, the authoratative data for the Sheet
resides on a remote server accessed via calls to the API server.  To greater
or lesser extents, this SDK attemts to insulate its users from that reality.
It does so by fetching the Sheet from the server and letting you work with the
Sheet locally.  For read-only access to a Sheet, that works pretty well --
provided you are willing to accept that the Sheet data you are reading might
have been changed on the server since it was fetched.

Where caching becomes something tricky is when writing to the Sheet -- either
by adding Columns, or Rows, or by changing the values of Cells.  Each of these
changes can result in a change to the structure (order and number of Rows and
Columns) of the Sheet.  Changes to Cells that are referenced by formulas can
result in the autoratative Sheet (on the server) having changed Cells on Rows
that your change did not touch.  As a result, in the current SDK, when a write
is done to the Sheet, the cached sheet data is discarded.

The SDK provides two distinct interfaces to the Sheet data.  The first is a
straightforward OO approach where methods are used to access the consitituent
members (Rows, Columns, Cells, etc.) of the Sheet.  The second is a more
"Pythonic" approach where the Sheet can be treated as a two-dimensional array.

When using the OO interface to the Sheet, no caching is done by the SDK.  Each
read of data from the Sheet will fetch the latest data for the corresponding
object from the API server.

When using the pythonic, 2-d array interface to the Sheet, the SDK uses
caching to avoid typically unnecessary queries to the API server.

You can manually override the caching policy on a Sheet-by-Sheet basis so
that, for example, the OO interface will use caching and the 2-d array
interface will not use caching.


# Examples

Please see the test cases in `tests/` for more examples.

## Connect to the API

These few lines should appear in nearly any client you write.  They connect
your client to the server and validate the connection by issuing a request
for the `/user/me` API endpoint -- getting the information about the user
you have connected as (a `smartsheetclient.UserProfile` object).
Subsequent examples will assume that `client` is a connected
`SmartsheetClient` instance unless otherwise noted.  The use of logging is,
of course, optional, but recommended.  Logging at the DEBUG level will
capture the requests and responses between your client and the API server.

```
import smartsheetclient
import logging
logging.basicConfig(filename='client.debug.log', level=logging.DEBUG)
client_logger = logging.getLogger()
my_token = 'TOKEN TO USE FOR DIRECT ACCESS'
client = smartsheetclient.SmartsheetClient(my_token, logger=client_logger)
client.connect()
print client
```

## List and Load Sheets

These few lines list the Sheets available to the your client.  In the
listing, each Sheet is represented by a `smartsheetclient.SheetInfo`
object.  Specific SheetInfo objects can be fetched by name (which may match
multiple Sheets) or permalink (which will match at most one Sheet).  Once
the Sheet you are interested in has been found, it can be fetched, either
directly from its corresponding `SheetInfo` object, or directly via the
client.  Both methods are show below.

```
# Full list of available Sheets.
sheet_list = client.fetchSheetList()

# Find SheetInfo objects by name
matching_sheet_info_list = client.fetchSheetInfoByName('Test Sheet 1')
print matching_sheet_info_list
# [<SheetInfo id:7703071930247044, name: u'Test Sheet 1', accessLevel: u'OWNER', permalink:u'https://app.smartsheet.com/b/home?lx=8LBckEZmSx8n6a1om0WXKw'>]

# Find SheetInfo objects by permalink.
sheet_info = client.fetchSheetInfoByPermalink('https://app.smartsheet.com/b/home?lx=8LBckEZmSx8n6a1om0WXKw')

# Load Sheet by ID.
sheet = client.fetchSheetById(sheet_info.id)

# Load Sheet by permalink.
sheet = client.fetchSheetByPermalink(sheet_info.permalink)

# Load Sheet from SheetInfo object.
sheet = sheet_info.loadSheet()
```


## Access the Rows and Cells in a Sheet

This example assumes that you are working with a fetched Sheet.  The Rows
of a Sheet are available by treating the Sheet as a list, or via `sheet.rows`.
You can access the Cells of a Sheet as if the Sheet were a 2-dimensional array.
When doing so, it is important to remember that Rows start at 1 and Columns
start at 0.

Unless otherwise noted, each of these examples shows both the 2-d list
interface and OO interface mechanism to accomplish the stated intent.

```
# Print the value of the top, left-hand Cell of a Sheet:
print sheet.getRowByRowNumber(1).getCellByIndex(0).value

print sheet[1][0]

# Assign "blue" to the top, left-hand Cell of a Sheet:
sheet.getRowByRowNumber(1).getCellByIndex(0).assign("blue")
cell = sheet.getRowByRowNumber(1).getCellByIndex(0)
cell.assign("blue")
sheet[1][0] = "blue"

# Save the change, by saving the Row, which stores any changed Cells on the Row.
# If other Rows have been changed but not saved, they will be lost, because a
# save of any Row on the Sheet discards the local Row cache.
sheet.getRowByRowNumber(1).save()
sheet[1].save()
```

Saving the change to a specific Cell can be done by calling `save()` on the
Cell instance.  However, by default, save on a Cell will also save any changes
made to other Cells on the same Row.  If you have changed multiple Cells on a
Row, but only want the changes to a specific Cell to be applied to the Row
on the Server, then pass `propagate=False` to the Cell's `save()` method.
This is shown in the examples below.  The SDK does not presently provide a
mechanism to explicitly save more than one, but less than all, of the changed
Cells on a Row.

```
# This discards any other Cell changes that may have been made on the Row, in
# addition to any Cell changes made on  other Rows.

sheet.getRowByRowNumber(1).getCellByIndex(0).save(propagate=False)

# There is no purely list-oriented way to save a specific Cell instead of the Row
sheet[1].getCellByIndex(0).save(propagate=False)
```


The Rows of a Sheet are available by treating the Sheet as a Python list,
or directly at Sheet.rows:

```
# Print the value of the second Column of each Row in the Sheet.
# Remember that Columns are zero-indexed (the second Column has index=1).

for row in sheet.rows:
    print row.getCellByIndex(1).value
    print row[1]
```


The value of all of the Cells in a Row can be gotten conveinently using the
list-style interface:

```
# All the Cells on Row 1.
values = list(sheet.getRowByRowNumber(1))
values = list(sheet[1])
```


A new Row can be created from the Sheet directly, or using a RowWrapper
created by the Sheet.  New Rows are not attached to the Sheet until they
have been added to it via the `addRow()` or `addRows()` method of the Sheet.
New Rows can be created empty, or with a list of values that will be used
as the values for the Cells in the Row.  See the examples below:

```
# Make an empty Row from the Sheet
row = sheet.makeRow()

# Make a Row with three Cells.
row = sheet.makeRow("one", "two", "three")
row = sheet.makeRow(["one", two", "three"])
# Or, the same thing from a generator.
row = sheet.makeRow((x for x in "one two three".split()))

# Do the same thing using a RowWrapper.
rw = sheet.makeRowWrapper()
row = rw.makeRow("one", "two", "three")
row = rw.makeRow(["one", two", "three"])
row = rw.makeRow((x for x in "one two three".split()))

# The result is such that:
row[0] == "one"

# Add the Row to the Sheet.
sheet.addRow(row)

# NOTE:  After adding to a Sheet, the Row object is discarded.
# Access to the newly added Row is through the Sheet.
# Assuming the Sheet has only the added Row:
sheet[1][0] == "one"
sheet[1][2] == "three"
```


The number of Rows in a Sheet is available in the normal list-like way, or as
an attribute of the Sheet.  Note that the number of Rows in a Sheet is not
necessarily the same thing as the number of Rows of the Sheet that were
fetched -- the Sheet can be fetched with a subset of the Rows.

```
print "Number of Rows in Sheet:", sheet.totalRowCount
print "Number of Rows in Sheet:", len(sheet)
print "Number of Rows fetched locally:", len(sheet.rows)
```

The number of Columns on a Row is available in the normal list-like way as
well, or as the length of the `columns` attribute of the Row.  The number
of Columns in the Sheet will typically be the same as the number of Columns
on the Row.  But, if the Sheet or Row were fetched with a subset of
Columns, then it will differ.

```
print "Number of Columns on Row 1:", len(sheet.getRowByRowNumber(1).columns)
print "Number of Columns on Row 1:", len(sheet[1])
print "Number of Columns on Sheet:", len(sheet.columns)
```


The list-like syntax is clearly simpler for scenarios where you only
need access (read or write) to the value of the Cells.  The object-oriented
interface, on the other hand, allows much richer access.

For example, in order to assign a Hyperlink to a Cell, the Cell object
must be accessed explicitly (not implicitly via the list-like syntax).

```
cell = sheet[1].getCellByIndex(0)
link = CellHyperlink(url="http://www.smartsheet.com")
cell.assign("Home", hyperlink=link)

print cell.value            # "Home"
print cell.hyperlink.url    # "http://www.smartsheet.com"
print sheet[1][0]           # "Home"
print sheet[1].getCellByIndex(0).hyperlink.url  # "http://www.smartsheet.com"

# Update the Sheet on the API servers.
cell.save()
```


## Add Rows to a Sheet.

This example assumes you are working with a fetched Sheet.

To add a Row to a Sheet, first create the Row from the Sheet, and then 
add it to the Sheet.  The Row may have values set in its Cells prior to
adding it to the Sheet:

```
# Add a Row to the bottom of the Sheet (the default position).
row_1 = sheet.makeRow()
sheet.addRow(row_1)

# Add a Row to the top of the Sheet.
row_2 = sheet.makeRow()
sheet.addRow(row_2, position='toTop')

# Add a Row to the bottom of the sheet with Cells in Columns 0 and 3 set.
# Columns are indexed starting at 0 - these are the first and fourth Columns.
row_3 = sheet.makeRow()
row_3[0] = "blue"
row_3[3] = 42.0
sheet.addRow(row_3, position='toBottom')
```

## Fetch the History of a Cell

The full history of each Cell can be fetched.  Note that this operation is
expensive (from a rate limiting perspective) and the API currently does not
support pagination of Cell history records.

```
for cell_version in sheet[1][0].fetchHistory():
    print cell_version
```

