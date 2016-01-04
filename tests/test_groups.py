import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestGroups:
    group = None
    members = None

    def test_create_group(self, smart_setup):
        smart = smart_setup['smart']
        group = smart.models.Group({
            'name': 'Knuckleheads',
            'description': 'Why, I oughta...',
            'members': [
                smart.models.GroupMember({
                    'email': smart_setup['users']['moe'].email
                })
            ]
        })
        action = smart.Groups.create_group(group)
        assert action.message == 'SUCCESS'
        TestGroups.group = action.result

    def test_list_groups(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Groups.list_groups(include_all=True)
        # TestGroups.group = action.result[0]
        assert action.total_count > 0
        groups = action.result
        for group in groups:
            if group.name == 'Knuckleheads':
                TestGroups.group = group
        assert isinstance(action.result[0], smart.models.Group)

    def test_get_group(self, smart_setup):
        smart = smart_setup['smart']
        group = smart.Groups.get_group(TestGroups.group.id)
        assert isinstance(group, smart.models.Group)

    def test_update_group(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Groups.update_group(
            TestGroups.group.id,
            smart.models.Group({
                'description': 'Hey fellas!'
            })
        )
        assert action.message == 'SUCCESS'

    def test_add_members(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Groups.add_members(
            TestGroups.group.id,
            [
                smart.models.GroupMember({
                    'email': smart_setup['users']['larry'].email
                }),
                smart.models.GroupMember({
                    'email': smart_setup['users']['curly'].email
                })
            ]
        )
        assert action.message == 'SUCCESS'
        TestGroups.members = action.result

    def test_remove_member(self, smart_setup):
        smart = smart_setup['smart']
        bye_id = 0
        for member in TestGroups.members:
            if member.email == smart_setup['users']['curly'].email:
                bye_id = member.id
        if bye_id > 0:
            action = smart.Groups.remove_member(
                TestGroups.group.id,
                bye_id
            )
            assert action.message == 'SUCCESS'
        else:
            pytest.runner.skip('could not find Curly')

    def test_delete_group(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Groups.delete_group(
            TestGroups.group.id
        )
        assert action.message == 'SUCCESS'






