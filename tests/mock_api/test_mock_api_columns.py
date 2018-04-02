# pylint: disable=C0103,W0232

from parameterized import parameterized, param
from smartsheet.models import Column
from mock_api_test_helper import MockApiTestHelper, clean_api_error

class TestMockApiColumns(MockApiTestHelper):
    @parameterized([
        param(
            scenario='Update Column - Change Type - Picklist',
            get_method=lambda client: client.Sheets.update_column,
            params=[
                123,
                234,
                Column({
                    'index': 2,
                    'title': 'Updated Column',
                    'type': 'PICKLIST',
                    'options': [
                        'An',
                        'updated',
                        'column'
                    ],
                    'width': 200
                })
            ],
            get_validation_field=lambda response: response.result.title,
            expected_validation_val='Updated Column'
        ),
        param(
            scenario='Update Column - Change Type - Contact List',
            get_method=lambda client: client.Sheets.update_column,
            params=[
                123,
                234,
                Column({
                    "index": 2,
                    "title": "Updated Column",
                    "type": "CONTACT_LIST",
                    "contactOptions": [
                        {
                            "name": "Some Contact",
                            "email": "some.contact@smartsheet.com"
                        },
                        {
                            "name": "Some Other Contact",
                            "email": "some.other.contact@smartsheet.com"
                        }
                    ],
                    "width": 200
                })
            ],
            get_validation_field=lambda response: response.result.title,
            expected_validation_val='Updated Column'
        )
    ])
    @clean_api_error
    def test_successful(
            self,
            scenario,
            get_method,
            params,
            get_validation_field,
            expected_validation_val):

        self.client.as_test_scenario(scenario)
        response = get_method(self.client)(*params)
        assert get_validation_field(response) == expected_validation_val
