import pytest
import smartsheet

from mock_api_test_helper import MockApiTestHelper

class TestMockApiSheets(MockApiTestHelper):
    def test_list_sheets(self):
        self.client.as_test_scenario('List Sheets - No Params')

        response = self.client.Sheets.list_sheets()

        sheets = response.result

        assert sheets[0].id == 1
