import smartsheet

#
# Get Column
#
# Dependencies: examples.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')

# get the column object
for idx, col in enumerate(sheet.columns):
    if col.primary:
        break

# make adjustments
col.index = 0
col.title = 'Film Title'

# update the column on the server, and update our
# local representation of the column in the sheet
action = smart.Sheets.update_column(sheet.id, col.id, col)
column = action.result
sheet.columns[idx] = column
print(column)