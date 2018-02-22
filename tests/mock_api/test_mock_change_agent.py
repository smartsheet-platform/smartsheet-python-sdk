# pylint: disable=C0103,W0232

from smartsheet.models import Sheet
from mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockChangeAgent(MockApiTestHelper):
    @clean_api_error
    def test_create_sheet(self):
        self.client.as_test_scenario('Change Agent Header - Can Be Passed')
        self.client.with_change_agent('MyChangeAgent')

        new_sheet = Sheet({
            "name": "My new sheet",
            "columns": [
                {
                    "title": "Col1",
                    "primary": True,
                    "type": "TEXT_NUMBER"
                }
            ]
        })

        response = self.client.Home.create_sheet(new_sheet)

        assert response.message == "SUCCESS"

