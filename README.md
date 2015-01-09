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

