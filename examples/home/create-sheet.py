import smartsheet

#
# Create Sheet in "Sheets" folder
#

smart = smartsheet.Smartsheet()
sheet = smart.models.Sheet({
    'name': 'example_newsheet_python_sdk',
    'columns': [{
            'title': 'Favorite',
            'type': 'CHECKBOX',
            'symbol': 'STAR'
        }, {
            'title': 'Primary Column',
            'primary': True,
            'type': 'TEXT_NUMBER'
        }, {
            'title': 'Status',
            'type': 'PICKLIST',
            'options': [
                'Not Started',
                'Started',
                'Completed'
            ]
        }
    ]
})

action = smart.Home.create_sheet(sheet)
sheet = action.result
print(sheet)
