import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestFolders:
    folder_created_in_folder = None
    copied_folder = None

    def test_create_folder_in_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.create_folder_in_folder(
            smart_setup['folder'].id,
            'TestFolders create_folder_in_folder'
        )
        nested = action.result
        TestFolders.folder_created_in_folder = nested
        assert action.message == 'SUCCESS'
        assert isinstance(nested, smartsheet.models.folder.Folder)

    def test_list_folders(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.list_folders(smart_setup['folder'].id)
        assert action.total_count > 0

    def test_update_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.update_folder(
            TestFolders.folder_created_in_folder.id,
            'update_folder create_folder_in_folder'
        )
        updated = action.result
        assert action.message == 'SUCCESS'
        assert updated.name == 'update_folder create_folder_in_folder'

    def test_copy_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.copy_folder(
            TestFolders.folder_created_in_folder.id,
            smart.models.ContainerDestination({
                'destination_id': smart_setup['folder'].id,
                'destination_type': 'folder',
                'new_name': 'copy of updated folder'
            })
        )
        copy = action.result
        assert action.message == 'SUCCESS'
        assert copy.name == 'copy of updated folder'
        TestFolders.copied_folder = copy

    def test_move_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.move_folder(
            TestFolders.copied_folder.id,
            smart.models.ContainerDestination({
                'destination_id': TestFolders.folder_created_in_folder.id,
                'destination_type': 'folder',
                'new_name': TestFolders.copied_folder.name
            })
        )
        move = action.result
        assert action.message == 'SUCCESS'

    def test_get_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.get_folder(smart_setup['folder'].id)
        assert 'app.smartsheet.com' in action.permalink

    def test_delete_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.delete_folder(TestFolders.copied_folder.id)
        assert action.message == 'SUCCESS'

    def test_sheet_from_template_in_folder(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Folders.create_sheet_in_folder_from_template(
            smart_setup['folder'].id,
            smart.models.Sheet({
                'name': 'My Blank Sheet From Template',
                'from_id': 7881304550205316  # Blank Sheet public template id
            })
        )
        assert action.message == 'SUCCESS'
