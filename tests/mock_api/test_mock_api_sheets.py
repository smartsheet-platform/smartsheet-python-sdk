# pylint: disable=C0103,W0232

import pytest
from smartsheet.models import Sheet, ExplicitNull
from smartsheet.exceptions import ApiError
from mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockApiSheets(MockApiTestHelper):
    @clean_api_error
    def test_list_sheets(self):
        self.client.as_test_scenario('List Sheets - No Params')

        response = self.client.Sheets.list_sheets()

        sheets = response.result

        assert sheets[0].name == "Copy of Sample Sheet"

    @clean_api_error
    def test_list_sheets_include_owner_info(self):
        self.client.as_test_scenario('List Sheets - Include Owner Info')

        response = self.client.Sheets.list_sheets(include='ownerInfo')

        sheets = response.result

        assert sheets[0].owner == "john.doe@smartsheet.com"

    @clean_api_error
    def test_create_sheet_invalid_no_columns(self):
        self.client.as_test_scenario('Create Sheet - Invalid - No Columns')

        new_sheet = Sheet({
            "name": "New Sheet",
            "columns": ExplicitNull()
        })

        with pytest.raises(ApiError) as e:
            self.client.Home.create_sheet(new_sheet)

        self.check_error_code(e, 1054)
