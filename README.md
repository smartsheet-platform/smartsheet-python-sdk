Smartsheet Python SDK
=====================

Python client library for version 1.1 of the Smartsheet API.
The Smartsheet API is documented at:
https://www.smartsheet.com/developers/api-documentation

**NOTE: Please note that this SDK is a pre-alpha.  It is incomplete, has not been rigorously tested, and is a work in progress.  See below for known issues, feature gaps, and a rough roadmap.  If you need a missing feature urgently, you are strongly encouraged to build it and submit a pull request.  Thanks for understanding.**

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
  * Add Rows (one at a time) to a Sheet.
* Row.save() to save any changes made to the Row
* Create new Sheets
* Refetch a Sheet
  * Needed because the SDK doesn't currently renumber the Rows of a Sheet after adding a Row
  * The Sheet is refetched using the same parameters it was fetched with originally
* Download attachments (from the sheet, rows, or discussion comments)
* Upload a new version of an existing attachment
  * This is distinct from replacing the existing attachment
* Fetch the history of a Cell
* Operate in read-only mode
  * Prevents any changes from being made to the Sheet on the server

# What Doesn't Work (that might surprise you)

Basically, if a feature of the API is not listed above, it probably 
hasn't been implemented yet.  However, there are some surprising gaps
that are covered here.

* When fetching a Sheet, pagination isn't supported
* Replacing an attachment doesn't work, only uploading a new version
* Adding a Row above any other rows requires refetching the Sheet
  * Because the local Rows don't get renumbered
* Deletion of Rows, Columns, Cells, or Sheets
* Can't issue HEAD requests on the S3 link used to download attachments
  * These result in a 403 error even thought the S3 docs say that GET and HEAD use the same permissions object

# TODO

* Add more test cases
  * There are some empty test cases as placeholders
* Continue adding support for more of the version 1.1 API
  * Delete Rows from a Sheet
  * Delete Cells
    * This can effectively be done today by assigning None
  * Add/Delete Columns to/from a Sheet
  * Delete Sheets
  * Bare minimum support for Workspaces and Folders
  * Bare minimum support for Reports
  * Bare minimum support for Search
  * Administrative operations
    * Manage users and groups
    * Backup sheets
  * Lots more
* Make sheet.save() save any local changes to the server
* Reorder and renumber the local Rows after certain (add, move, delete) changes to the Rows of a Sheet
  * This will make Sheet.refresh() less necessary

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

# Examples

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

These few lines list the sheets available to the your client.  In the
listing, each sheet is represented by a `smartsheetclient.SheetInfo`
object.  Specific SheetInfo objects can be fetched by name (which may match
multiple sheets) or permalink (which will match at most one sheet).  Once
the sheet you are interested in has been found, it can be fetched, either
directly from its corresponding `SheetInfo` object, or directly via the
client.  Both methods are show below.

```
# Full list of available sheets.
sheet_list = client.fetchSheetList()

# Find SheetInfo objects by name
matching_sheet_info_list = client.fetchSheetInfoByName('Test Sheet 1')
print matching_sheet_info_list
# [<SheetInfo id:7703071930247044, name: u'Test Sheet 1', accessLevel: u'OWNER', permalink:u'https://app.smartsheet.com/b/home?lx=8LBckEZmSx8n6a1om0WXKw'>]

# Find SheetInfo objects by permalink.
sheet_info = client.fetchSheetInfoByPermalink('https://app.smartsheet.com/b/home?lx=8LBckEZmSx8n6a1om0WXKw')

# Load Sheet by ID.
sheet = client.fetchSheetByID(sheet_info.id)

# Load Sheet by permalink.
sheet = client.fetchSheetByPermalink(sheet_info.permalink)

# Load Sheet from SheetInfo object.
sheet = sheet_info.loadSheet()
```

## Access the Rows and Cells in a Sheet

This example assumes that you are working with a fetched sheet.  The Rows
of a Sheet are available by treating the Sheet as a list, or via `sheet.rows`.
You can access the Cells of a Sheet as if the Sheet were a 2-dimensional array.
When doing so, it is important to remember that Rows start at 1 and Columns
start at 0.

```
# Print the value of the top, left-hand Cell of a Sheet:
print sheet[1][0]

# Assign "blue" to the top, left-hand Cell of a Sheet:
sheet[1][0] = "blue"

# Save the change, either by saving the Row, which will store any changed
# Cells on the Row.
sheet[1].save()

# Or, save the change by saving the specific Cell.
sheet[1].getCellByIndex(0).save()
```

The Rows of a Sheet are available by treating the Sheet as a Python list,
or directly at Sheet.rows:

```
# Print the value of the second Column of each Row in the Sheet.
# Remember that Columns are zero-indexed (the second Column has index=1).

for row in sheet.rows:
    print row[1]

# Or,
for row in sheet:
    print row[1]
```

The number of Rows in a Sheet and the number of Columns on a Row are 
available in the normal list-like way:

```
print "Number of Rows in Sheet:", len(sheet)
print "Number of Columns on Row 1:", len(sheet[1])
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
expensive (from a rate limiting perspective).

```
for cell_version in sheet[1][0].fetchHistory():
    print cell_version
```

