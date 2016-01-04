import smartsheet

#
# List all Sheets.
#

smart = smartsheet.Smartsheet()
sheets = smart.Sheets.list_sheets(include_all=True)
print(sheets)
