import smartsheet

#
# Get Columns
#
# Dependencies: examples.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')

columns = sheet.get_columns()
print(columns)