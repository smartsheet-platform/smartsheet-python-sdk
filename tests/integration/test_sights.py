import pytest


@pytest.mark.usefixtures("smart_setup")
class TestSights:
    sights = None
    own_id = None
    new_sight = None

    def test_list_sights(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sights.list_sights()
        assert isinstance(action.data, list)
        TestSights.sights = action.data

    def test_get_sight(self, smart_setup):
        smart = smart_setup['smart']
        own_id = None
        for sight in TestSights.sights:
            if sight.access_level == 'OWNER':
                own_id = sight.id
                break

        if own_id:
            sight = smart.Sights.get_sight(own_id)
            assert isinstance(sight, smart.models.Sight)
            TestSights.own_id = own_id

    def test_copy_sight(self, smart_setup):
        smart = smart_setup['smart']
        if TestSights.own_id:
            dest = smart.models.ContainerDestination()
            dest.destination_type = 'folder'
            dest.destination_id = smart_setup['folder'].id
            dest.new_name = 'new sight'
            action = smart.Sights.copy_sight(TestSights.own_id, dest)
            assert action.message == 'SUCCESS'
            TestSights.new_sight = action.data

    def test_update_sight(self, smart_setup):
        smart = smart_setup['smart']
        if TestSights.new_sight:
            new_new_sight = smart.models.Sight()
            new_new_sight.name = 'new new sight'
            action = smart.Sights.update_sight(TestSights.new_sight.id, new_new_sight)
            assert action.message == 'SUCCESS'
            TestSights.new_sight = action.data

    def test_set_publish_status(self, smart_setup):
        smart = smart_setup['smart']
        if TestSights.new_sight:
            publish = smart.models.SightPublish()
            publish.read_only_full_enabled = True
            publish.read_only_full_accessible_by = 'ALL'
            action = smart.Sights.set_publish_status(TestSights.new_sight.id, publish)
            assert action.message == 'SUCCESS'

    def test_get_publish_status(self, smart_setup):
        smart = smart_setup['smart']
        if TestSights.new_sight:
            publish = smart.Sights.get_publish_status(TestSights.new_sight.id)
            assert isinstance(publish, smart.models.SightPublish)
            assert publish.read_only_full_enabled == True

    def test_delete_sight(self, smart_setup):
        smart = smart_setup['smart']
        if TestSights.new_sight:
            action = smart.Sights.delete_sight(TestSights.new_sight.id)
            assert action.message == 'SUCCESS'

