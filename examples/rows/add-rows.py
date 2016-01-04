import smartsheet

#
# Add Row(s)
#
# Note the use of the `sheet.add_rows()` "convenience method" on
# the Sheet model instance returned by smart.Sheets.get_by_name().
#
# Dependencies: examples.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')

row = smart.models.Row()

row.to_top = True
for col in sheet.columns:
    if col.title == 'Favorite':
        row.cells.append({
            'column_id': col.id,
            'value': True
        })
    if col.title == 'Primary Column':
        row.cells.append({
            'column_id': col.id,
            'value': 'A New Hope'
        })
    if col.title == 'Status':
        row.cells.append({
            'column_id': col.id,
            'value': 'Completed'
        })

# returns updated Sheet
sheet = sheet.add_rows([row])
