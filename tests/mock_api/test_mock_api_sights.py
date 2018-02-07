# pylint: disable=C0103,W0232

import smartsheet
from mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockApiSheets(MockApiTestHelper):
    @clean_api_error
    def test_list_sights(self):
        self.client.as_test_scenario('List Sights')
        response = self.client.Sights.list_sights()
        assert isinstance(response.data, list)

    @clean_api_error
    def test_get_sight(self):
        self.client.as_test_scenario('Get Sight')
        response = self.client.Sights.get_sight(52)
        assert isinstance(response, smartsheet.models.Sight)

    @clean_api_error
    def test_copy_sight(self):
        self.client.as_test_scenario('Copy Sight')
        dest = smartsheet.models.ContainerDestination()
        dest.destination_type = 'folder'
        dest.destination_id = 484
        dest.new_name = 'new sight'
        response = self.client.Sights.copy_sight(52, dest)
        assert response.message == 'SUCCESS'

    @clean_api_error
    def test_update_sight(self):
        self.client.as_test_scenario('Update Sight')
        new_new_sight = smartsheet.models.Sight()
        new_new_sight.name = 'new new sight'
        response = self.client.Sights.update_sight(812, new_new_sight)
        assert response.message == 'SUCCESS'

    @clean_api_error
    def test_set_publish_status(self):
        self.client.as_test_scenario('Set Sight Publish Status')
        publish = smartsheet.models.SightPublish()
        publish.read_only_full_enabled = True
        publish.read_only_full_accessible_by = 'ALL'
        response = self.client.Sights.set_publish_status(812, publish)
        assert response.message == 'SUCCESS'

    @clean_api_error
    def test_get_publish_status(self):
        self.client.as_test_scenario('Get Sight Publish Status')
        response = self.client.Sights.get_publish_status(812)
        assert isinstance(response, smartsheet.models.SightPublish)
        assert response.read_only_full_enabled == True

    @clean_api_error
    def test_delete_sight(self):
        self.client.as_test_scenario('Delete Sight')
        response = self.client.Sights.delete_sight(700)
        assert response.message == 'SUCCESS'
