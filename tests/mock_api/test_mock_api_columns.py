# pylint: disable=C0103,W0232

from smartsheet.models import Column
from mock_api_test_helper import MockApiTestHelper, clean_api_error

class TestMockApiColumns(MockApiTestHelper):
    @clean_api_error
    def test_column_type_change_to_picklist(self):

        self.client.as_test_scenario('Update Column - Change Type - Picklist')

        response = self.client.Sheets.update_column(123, 234, Column({
            'index': 2,
            'title': 'Updated Column',
            'type': 'PICKLIST',
            'options': [
                'An',
                'updated',
                'column'
            ],
            'width': 200
        }))

        assert response.result.title == 'Updated Column'

    @clean_api_error
    def test_column_type_change_to_contact_list(self):

        self.client.as_test_scenario('Update Column - Change Type - Contact List')

        response = self.client.Sheets.update_column(123, 234, Column({
            'index': 2,
            'title': 'Updated Column',
            'type': 'CONTACT_LIST',
            'contactOptions': [
                {
                    'name': 'Some Contact',
                    'email': 'some.contact@smartsheet.com'
                },
                {
                    'name': 'Some Other Contact',
                    'email': 'some.other.contact@smartsheet.com'
                }
            ],
            'width': 200
        }))

        assert response.result.title == 'Updated Column'
