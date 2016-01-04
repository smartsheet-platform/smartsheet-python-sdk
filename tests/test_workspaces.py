import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestWorkspaces:
    a = None
    b = None
    c = None
    share = None

    def test_create_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.create_workspace(
            smart.models.Workspace({
                'name': 'pytest workspace A ' + smart_setup['now']
            })
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.a = action.result
        action = smart.Workspaces.create_workspace(
            smart.models.Workspace({
                'name': 'pytest workspace B ' + smart_setup['now']
            })
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.b = action.result

    def test_create_folder_in_workspace(self, smart_setup):
        smart = smart_setup['smart']
        folder = smart.models.Folder({
            'name': 'Bucket A'
        })
        action = smart.Workspaces.create_folder_in_workspace(
            TestWorkspaces.a.id, folder
        )
        assert action.message == 'SUCCESS'

    def test_list_folders(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.list_folders(TestWorkspaces.a.id)
        assert action.total_count > 0
        folders = action.result
        assert folders[0].name == 'Bucket A'

    def test_list_workspaces(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.list_workspaces()
        assert action.total_count > 0

    def test_create_sheet_from_template_in_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.create_sheet_in_workspace_from_template(
            TestWorkspaces.b.id,
            smart.models.Sheet({
                'name': 'My Blank Sheet From Template',
                'from_id': 7881304550205316  # Blank Sheet public template id
            })
        )
        assert action.message == 'SUCCESS'

    def test_get_workspace(self, smart_setup):
        smart = smart_setup['smart']
        workspace = smart.Workspaces.get_workspace(TestWorkspaces.b.id)
        assert isinstance(workspace, smart.models.workspace.Workspace)

    def test_copy_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.copy_workspace(
            TestWorkspaces.b.id,
            smart.models.ContainerDestination({
                'new_name': 'pytest workspace C ' + smart_setup['now']
            }),
            include='all'
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.c = action.result

    def test_create_sheet_in_workspace(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.models.Sheet({
            'name': 'pytest_workspace_sheet ' + smart_setup['now'],
            'columns': [{
                'title': 'Slackers',
                'primary': True,
                'type': 'TEXT_NUMBER'
            }]
        })
        action = smart.Workspaces.create_sheet_in_workspace(TestWorkspaces.c.id, sheet);
        sheet = action.result

    def test_share_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.share_workspace(
            TestWorkspaces.c.id,
            smart.models.Share({
                'access_level': 'EDITOR_SHARE',
                'email': smart_setup['users']['moe'].email
            })
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.share = action.result

    def test_list_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        shares = smart.Workspaces.list_shares(
            TestWorkspaces.c.id
        )
        assert shares.total_count > 0

    def test_get_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        ws = smart.Workspaces.get_share(
            TestWorkspaces.c.id,
            TestWorkspaces.share.id
        )
        assert isinstance(ws, smart.models.share.Share)

    def test_update_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.update_share(
            TestWorkspaces.c.id,
            TestWorkspaces.share.id,
            smart.models.Share({
                'access_level': 'ADMIN'
            })
        )
        assert action.message == 'SUCCESS'

    def test_delete_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.delete_share(
            TestWorkspaces.c.id,
            TestWorkspaces.share.id
        )
        assert action.message == 'SUCCESS'

    def test_update_workspace(self, smart_setup):
        smart = smart_setup['smart']
        TestWorkspaces.c.name = 'Nincompoops'
        action = smart.Workspaces.update_workspace(
            TestWorkspaces.c.id,
            TestWorkspaces.c
        )
        assert action.message == 'SUCCESS'

    def test_delete_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.delete_workspace(TestWorkspaces.a.id)
        assert action.message == 'SUCCESS'
        action = smart.Workspaces.delete_workspace(TestWorkspaces.b.id)
        assert action.message == 'SUCCESS'
        action = smart.Workspaces.delete_workspace(TestWorkspaces.c.id)
        assert action.message == 'SUCCESS'
