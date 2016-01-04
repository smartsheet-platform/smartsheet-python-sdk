import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestHome:

    def test_list_all_contents(self, smart_setup):
        smart = smart_setup['smart']
        contents = smart.Home.list_all_contents()
        assert isinstance(contents, smartsheet.models.home.Home)

    def test_create_sheet(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.models.Sheet({
            'name': 'example_newsheet_python_sdk_' + smart_setup['now'],
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
        assert action.message == 'SUCCESS'
        # clean up
        action = smart.Sheets.delete_sheet(sheet.id)
        assert action.message == 'SUCCESS'
    
    def test_create_sheet_from_dict(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Home.create_sheet({
            'name': 'example_newsheet_python_sdk_' + smart_setup['now'],
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
        sheet = action.result
        assert action.message == 'SUCCESS'
        action = smart.Sheets.delete_sheet(sheet.id)
        assert action.message == 'SUCCESS'
    
    def test_list_folders(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Home.list_folders(include_all=True)
        folders = action.result
        assert action.page_number == 1

    def test_create_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Home.create_folder(
            'Python SDK Test ' + smart_setup['now']
        )
        folder = action.result
        assert action.message == 'SUCCESS'
        # clean up
        action = smart.Folders.delete_folder(folder.id)
        assert action.message == 'SUCCESS'

    def test_create_sheet_from_template(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Home.create_sheet_from_template(
            smart.models.Sheet({
                'name': 'My Blank Sheet From Template',
                'from_id': 7881304550205316  # Blank Sheet public template id
            })
        )
        sheet = action.result
        assert action.message == 'SUCCESS'
        # clean up
        action = smart.Sheets.delete_sheet(sheet.id)
        assert action.message == 'SUCCESS'