Smartsheet Python SDK
=====================

Python client library for version 1.1 of the Smartsheet API.
The Smartsheet API is documented at:
https://www.smartsheet.com/developers/api-documentation

**NOTE: This library is frightenlying, terribly, and horribly incomplete at the moment.**

# What Works

Some of the Smartsheet API is accessible via this library.  Presently,
the list of what works is much shorter than the list of what doesn't
work yet.  Hopefully that will change.  Here's what currently works:

* Convenience wrapper around raw requests
* Fetch the information about a specific user
* Fetch the list of sheets available
* Fetch a Sheet (by its permalink or ID)
  * Specify whether or not to include discussions, attachments, formats, or filters in the returned Sheet
  * Access cell data in the returned Sheet
* Download attachments (from the sheet, rows, or discussion comments)
* Upload a new version of an existing attachment
  * This is distinct from replacing the existing attachment

# What Doesn't Work (that might surprise you)

Basically, if a feature of the API is not listed above, it probably 
hasn't been implemented yet.  However, there are some surprising gaps
that are covered here.

* When fetching a Sheet, pagination isn't supported
* Replacing an attachment doesn't work, only uploading a new version
* Adding new data (other than new attachment versions) to a Sheet
* Can't issue HEAD requests on the S3 link used to download attachments
  * These result in a 403 error even thought the S3 docs say that GET and HEAD use the same permissions object

# TODO

* Add unit tests
  * Probably using the unittest standard library
* Continue adding support for more of the version 1.1 API
  * Change Cell content
  * Add Rows (including new content in their Cells)
  * Add Columns (including new content in their Cells)
  * Bare minimum support for Workspaces and Folders
  * Bare minimum support for Reports
  * Bare minimum support for Search
  * Administrative operations
    * Manage users and groups
    * Backup sheets
  * Lots more
* Add the ability to operate in read-only mode
  * This would prevent any changes from being made to the Sheet

# Roadmap

Eventually, the client should provide something of an ActiveRecord-like
interface.  In this model, changes could be made to a local copy of the
Sheet, and then synchronized with the Smartsheet servers by calling
a .save() method on either the Sheet or whatever object was changed. In
this model, calling .save() on the Sheet (or any object that can contain
other objects) would result in the saving of any "contained" objects.

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
of a Sheet are available via `sheet.rows`.  In addition, the Sheet supports
certain list-style access patterns.  In particular, you can access the Cells
of the Sheet as if the Sheet were a 2-dimensional array.  When doing so, it
is important to remember that Rows start at 1, and Columns start at 0.

```
# Print the value of the top left-hand Cell of a sheet:
print sheet[1][0].value

# This 2-dimensional access pattern is also available via `sheet.rows`:
# This is equivalent ot the prior print statement.
print sheet.rows[1][0]
```

The rows of a sheet can be iterated over as if they were a normal Python
list:
```
# Print the value of the second Column of each Row in the Sheet.
# Remember that Columns are zero-indexed (the second Column has index=1).
for row in sheet.rows:
    print row[1]
```

