# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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