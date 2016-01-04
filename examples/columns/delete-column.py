import smartsheet

#
# Delete a Column from an existing Sheet.
#
# Dependencies: example.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')

for col in sheet.columns:
    if col.title == 'Status':
        column_id = col.id
result = sheet.delete_column(column_id)
print(result)
