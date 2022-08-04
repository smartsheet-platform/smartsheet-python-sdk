# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.177.0] - 2022-08-03
### Added
- add support for commenter permissions
- add base URL for smartsheet.eu
- add `level` parameter to get_row

### Changed
- pull updates for Python 3.10 compatibility
- update setup and readme for Python version 3.7 - 3.10
- update EnumeratedValue `__eq__` method to handle comparisons to NoneType

### Fixed
- separate `DatetimeObjectValue` from `DateObjectValue` to fix Sheet Summary Field serialization

## [2.105.1] - 2020-10-15
### Fixed
- don't add time offset to date types when serializing

## [2.105.0] - 2020-10-07
### Added
- add column formulas
- add filterId to get_sheets
- Adding rowsModifiedSince parameter to sheet.get_sheet
- add `rules` and `ruleRecipients` to create sheet from template
  inclusion

## [2.101.0] - 2020-08-01
### Changed
- #144 bumped missing property message to debug.
- Model Profile Image as different object from Image

### Added
- Webhooks for Columns

## [2.86.0] - 2019-11-12
### Added
- type and object definitions to support multi-picklist columns

### Changed
- additions to CellDataItem widget contents to support METRIC widgets
  containing sheet summary fields
- dashboards widget model to support widgets that are in an error state
- get_columns needs level support
- update doc to indicate format and objectValue are valid for cell
  history includes
- continue to support level 0 widget type names

### Other
- Make INFO+ level logging return either strings or well-formed json for
  log parsing

## [2.83.0] - 2019-08-14
### Added
- add support for sheet summary

## [2.77.0] - 2019-08-08
### Added
- column descriptions
- additional date formats

### Changed
- enable Coveralls
- cleaned up include/exclude flags on copy sheet/folder/workspace
- Significant overhaul of Sights

### Fixed
- Fix logging to use existing module logger instead of a new logger'util'

## [2.68.3] - 2019-06-14
### Changed
- automated doc updates should be ignored in changelist

### Fixed
- bug-21961 sendEmail is hardcoded to true in share_sheet api

### Other
- doc: update CHANGELOG.md
- doc: build 2.68.2 final docs

## [2.68.2] - 2019-06-14
### Changed
- install dependencies for sphinx
- automated doc updates should be ignored in changelist

## [2.68.1] - 2019-06-14
### Fixed
- fix arguments for current versions of pytest

## [2.68.0] - 2019-05-09
### Added
- Event Reporting functionality

## [1.5.0] - 2019-03-19
### Added 
- WEBCONTENT sight widget type
- Add Workspace to sheet model
- Support for groups in get_current_user
- Multi-contact feature support

### Fixed
- Fixed setter for modified_at attribute in row model
 
## [1.4.0] - 2019-02-19
### Added
- Added BASE URI definition for Smartsheetgov
 
### Changed
- Remove [enum34](https://pypi.python.org/pypi/enum34) as a dependency for versions of Python after 3.4 

## [1.3.3] - 2018-04-19

### Added
- XLSX and CSV import endpoints for workspaces, folders and sheets
- Rudimentary support Sight chart objects (chart contents read into JSON strings) 
- Exclude `permalinks` option to Home.list_all_contents
- backgroundColor to Sight object

### Fixed
- [Improper format strings in Types](https://github.com/smartsheet-platform/smartsheet-python-sdk/issues/92)

## [1.3.2] - 2018-03-15

### Fixed
- String representations for EnumeratedValue should contain just their `name` not `class_name.name`
[(SO reported)](https://stackoverflow.com/questions/49256434/writing-column-type-now-has-columntype-option-instead-of-option).

## [1.3.1] - 2018-03-01

### Added
- Implemented [cross-sheet References](http://smartsheet-platform.github.io/api-docs/?shell#cross-sheet-references)
- Updated UserProfile and added support for profile images
- Added an argument to the client constructor method to externally set the API base URI
- Implemented [Automation Rules](http://smartsheet-platform.github.io/api-docs/?shell#automation-rules)
- Implemented row sort objects and [Sort Rows in Sheet](http://smartsheet-platform.github.io/api-docs/?shell#sort-rows-in-sheet) endpoint
- Added row filter properties to SheetFilter
- Added ifVersionAfter parameter to Sheet.get_sheet() method

### Changed
In our efforts to further streamline the SDK, enumerated properties have been changed from type String to type EnumeratedValue, which wraps Python Enum. 
In addition to allowing us to remove a number of redundant string arrays, this also provides the benefit of better code completion (in most IDEs) 
and provides for more programmatic clarity, for example:
 ```
sheet = smartsheet.Sheets.get_sheet(sheet_id)
if sheet.access_level == AccessLevel.OWNER:
    # perform some task for OWNER
    ...
```
However, string comparisons will continue to operate as they did previously. No change is required if your code uses comparisons such as:
```
sheet = smartsheet.Sheets.get_sheet(sheet_id)
if sheet.access_level == 'OWNER':
    # perform some task for OWNER
    ...
```
[enum34](https://pypi.python.org/pypi/enum34) has been added as a required package for the SDK  

## [1.3.0] - 2018-02-21

### Changed 

Several changes have been made to the SDK to improve both the maintainability of the SDK and the predictability/reliability of the results returned by the SDK. Some of these changes may be breaking to code that currently uses the SDK. The following changes should be reviewed:
* The JSON serializer has been changed to ignore `null` values and empty lists (`[]`). A new Smartsheet model, ExplicitNull, is provided for circumstances where there is a need to force the serialization of a null value. As an example, to clear a hyperlink value from a cell, you can perform the following operation:
```
        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "",
            "hyperlink": ExplicitNull()
        })

        response = self.client.Sheets.update_rows(1, [first_row])
```
* Property values are more strongly type checked on assignment and you will get a `ValueError` exception if you attempt to assign an incompatible object. Previously, there were a number of cases where assignment of incompatible types would have resulted in a silent failure by the SDK.
* In previous releases, property filters were executed prior to create or update operations on many models within the SDK. Unfortunately, those filters were sometimes at odds with the API and occasionally returned unpredictable results. For that reason those filters have been removed. Be aware that any property that is set in a model will be passed through to the API.
* Properties `id`, `format`, and `type` are accessible without the preceding underscore, e.g. `cell._format` has changed to `cell.format`. 

## [1.2.4] - 2018-02-21

### Fixed

- There is a race condition which exists in the window between when the API servers disconnect an idle connection and when the client receives notification 
of the disconnection. If a request is made during that window, the client reads a blank status line and issues an error indicating that the session was 
terminated without a response (UnexpectedRequestError). This release is made to address that issue by implementing appropriate retries in the SDK.
 
## [1.2.3] - 2017-12-11

### Fixed

- Safe defaults for mock api test name and module name
## [1.2.2] - 2017-12-07
### Added
- Support for column validation
- New `Passthrough` object supports `get`, `post`, `put`, or `delete` with arbitrary json payload. Use this for access to any API feature that isn't yet modeled in the API. Requests still benefit from error retry and logging.

- `add_image_to_cell` & `attach_file_to_cell`: Now support `override_validation` and `alt_text` parameters
- `copy_folder`, `copy_workspace` and `copy_sheet`: Additional options for `include`, `skip_remap`, and `omit` parameters
- Support for `include=sheetVersion` for several endpoints that return a list of sheets
- Support for reading sheet filters
- More flags when publishing Sheets or Reports as HTML
- Search
  - Results include favorite information
  - Limit search scope

### Changed
- Mock tests
- Improved logging

### Fixed
- Sight widget column property name



## Previous releases
- Documented as [Github releases](https://github.com/smartsheet-platform/smartsheet-python-sdk/releases)
