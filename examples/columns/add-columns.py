import smartsheet

#
# Add Column(s)
#
# Note the use of the `sheet.add_columns()` "convenience method" on
# the Sheet model instance returned by smart.Sheets.get_by_name().
#
# Dependencies: examples.home.create-sheet
#

smart = smartsheet.Smartsheet()
sheet = smart.Sheets.get_sheet_by_name('example_newsheet_python_sdk')

sheet = sheet.add_columns([
    smart.models.Column({
        'title': 'Director',
        'type': 'TEXT_NUMBER',
        'index': 1
    }),
    smart.models.Column({
        'title': 'Released',
        'type': 'TEXT_NUMBER',
        'index': 1
    })
])

print(sheet)