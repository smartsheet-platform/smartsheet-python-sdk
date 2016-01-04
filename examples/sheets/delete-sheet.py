import smartsheet

#
# Delete an existing Sheet
#
# Dependencies: examples.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')
result = smart.Sheets.delete_sheet(sheet.id)
print(result)
