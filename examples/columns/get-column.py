import smartsheet

#
# Get Column
#
# Dependencies: examples.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')

# get the column id from sheet we have
for col in sheet.columns:
    if col.primary:
        column_id = col.id

# fetch the column from the server
column = sheet.get_column(col.id)
print(column)