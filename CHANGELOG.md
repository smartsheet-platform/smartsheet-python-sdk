# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2018-2-21

## Pre-release SDK version 1.3

###Changed 
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

## [1.2.4] - 2018-2-21

### Fixed

- There is a race condition which exists in the window between when the API servers disconnect an idle connection and when the client receives notification 
of the disconnection. If a request is made during that window, the client reads a blank status line and issues an error indicating that the session was 
terminated without a response (UnexpectedRequestError). This release is made to address that issue by implementing appropriate retries in the SDK.
 
## [1.2.3] - 2017-12-11

### Fixed

- Safe defaults for mock api test name and module name
## [1.2.2] - 2017-12-7
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