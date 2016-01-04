# How to Run Examples

Simply set your Smartsheet Access Token as an environment variable, then call each example as a module.

    $ export SMARTSHEET_ACCESS_TOKEN=blahblahblah
	$ python -m examples.home.list-all-contents

## Verbose Examples

If you'd like to run the examples with log output, set the `LOG_CFG` environment variable to one of `INFO`, `DEBUG` or a file path to a [JSON configuration file](https://docs.python.org/2/library/logging.config.html). 

## Suggested Sequence

If you'd like to follow a natural flow of creating a sheet, adding some rows, manipulating other aspects of the sheet, run these examples in order:

    $ python -m examples.home.create-sheet
    $ python -m examples.home.list-all-contents
    $ python -m examples.rows.add-rows
    $ python -m examples.sheets.delete-sheet
