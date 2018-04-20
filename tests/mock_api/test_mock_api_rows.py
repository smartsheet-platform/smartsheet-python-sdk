# pylint: disable=C0103,W0232

import pytest
from smartsheet.models import Row, PredecessorList, Duration, ExplicitNull
from smartsheet.exceptions import ApiError

from mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockApiRows(MockApiTestHelper):
    @clean_api_error
    def test_add_rows_assign_values_string(self):
        self.client.as_test_scenario('Add Rows - Assign Values - String')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": "Apple"
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Red Fruit"
        })

        second_row = Row()
        second_row.cells.append({
            "columnId": 101,
            "value": "Banana"
        })
        second_row.cells.append({
            "columnId": 102,
            "value": "Yellow Fruit"
        })

        response = self.client.Sheets.add_rows(1, [first_row, second_row])

        assert response.result[0].cells[0].value == "Apple"

    @clean_api_error
    def test_add_rows_assign_values_int(self):
        self.client.as_test_scenario('Add Rows - Assign Values - Int')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": 100
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "One Hundred"
        })

        second_row = Row()
        second_row.cells.append({
            "columnId": 101,
            "value": 2.1
        })
        second_row.cells.append({
            "columnId": 102,
            "value": "Two Point One"
        })

        response = self.client.Sheets.add_rows(1, [first_row, second_row])

        assert response.result[1].cells[0].value == 2.1

    @clean_api_error
    def test_add_rows_assign_values_bool(self):
        self.client.as_test_scenario('Add Rows - Assign Values - Bool')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": True
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "This is True"
        })

        second_row = Row()
        second_row.cells.append({
            "columnId": 101,
            "value": False
        })
        second_row.cells.append({
            "columnId": 102,
            "value": "This is False"
        })

        response = self.client.Sheets.add_rows(1, [first_row, second_row])

        assert response.result[1].cells[0].value is False

    @clean_api_error
    def test_add_rows_assign_formulae(self):
        self.client.as_test_scenario('Add Rows - Assign Formulae')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "formula": "=SUM([Column2]3, [Column2]4)*2"
        })
        first_row.cells.append({
            "columnId": 102,
            "formula": "=SUM([Column2]3, [Column2]3, [Column2]4)"
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].cells[1].formula == "=SUM([Column2]3, [Column2]3, [Column2]4)"

    @clean_api_error
    def test_add_rows_assign_values_hyperlink(self):
        self.client.as_test_scenario('Add Rows - Assign Values - Hyperlink')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": "Google",
            "hyperlink": {
                "url": "http://google.com"
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Bing",
            "hyperlink": {
                "url": "http://bing.com"
            }
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].cells[0].hyperlink.url == "http://google.com"

    @clean_api_error
    def test_add_rows_assign_values_hyperlink_sheet_id(self):
        self.client.as_test_scenario('Add Rows - Assign Values - Hyperlink SheetID')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": "Sheet2",
            "hyperlink": {
                "sheetId": 2
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Sheet3",
            "hyperlink": {
                "sheetId": 3
            }
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].cells[1].hyperlink.sheet_id == 3

    @clean_api_error
    def test_add_rows_assign_values_hyperlink_report_id(self):
        self.client.as_test_scenario('Add Rows - Assign Values - Hyperlink ReportID')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": "Report9",
            "hyperlink": {
                "reportId": 9
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Report8",
            "hyperlink": {
                "reportId": 8
            }
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].cells[0].hyperlink.report_id == 9

    @clean_api_error
    def test_add_rows_invalid_assign_value_and_formulae(self):
        self.client.as_test_scenario('Add Rows - Invalid - Assign Value and Formulae')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "formula": "=SUM([Column2]3, [Column2]4)*2",
            "value": "20"
        })
        first_row.cells.append({
            "columnId": 102,
            "formula": "=SUM([Column2]3, [Column2]3, [Column2]4)"
        })

        with pytest.raises(ApiError) as e:
            self.client.Sheets.add_rows(1, [first_row])

        self.check_error_code(e, 1163)

    @clean_api_error
    def test_add_rows_invalid_assign_hyperlink_url_and_sheet_id(self):
        self.client.as_test_scenario('Add Rows - Invalid - Assign Hyperlink URL and SheetId')

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "value": "Google",
            "hyperlink": {
                "url": "http://google.com",
                "sheetId": 2
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Bing",
            "hyperlink": {
                "url": "http://bing.com"
            }
        })

        with pytest.raises(ApiError) as e:
            self.client.Sheets.add_rows(1, [first_row])

        self.check_error_code(e, 1112)

    @clean_api_error
    def test_add_rows_assign_object_value_predecessor_list(self):
        self.client.as_test_scenario('Add Rows - Assign Object Value - Predecessor List')

        lag = Duration({
            "objectType": "DURATION",
            "days": 2,
            "hours": 4
        })

        predecessor_list = PredecessorList()
        predecessor_list.predecessors.append({
            "rowId": 10,
            "type": "FS",
            "lag": lag
        })

        first_row = Row()
        first_row.cells.append({
            "columnId": 101,
            "objectValue": predecessor_list
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].cells[1].display_value == "2FS +2d 4h"

    @clean_api_error
    def test_add_rows_assign_object_value_predecessor_list_using_float_duration(self):
        self.client.as_test_scenario(
            'Add Rows - Assign Object Value - Predecessor List (using floats)')

        lag = Duration({
            'objectType': 'DURATION',
            'days': 2.5
        })

        predecessor_list = PredecessorList()
        predecessor_list.predecessors.append({
            'rowId': 10,
            'type': 'FS',
            'lag': lag
        })

        row = Row()
        row.cells.append({
            'columnId': 101,
            'objectValue': predecessor_list
        })

        response = self.client.Sheets.add_rows(1, [row])

        assert response.result[0].cells[1].display_value == '2FS +2.5d'

    @clean_api_error
    def test_add_rows_location_top(self):
        self.client.as_test_scenario('Add Rows - Location - Top')

        first_row = Row()
        first_row.to_top = True
        first_row.cells.append({
            "columnId": 101,
            "value": "Apple"
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Red Fruit"
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].row_number == 1

    @clean_api_error
    def test_add_rows_location_bottom(self):
        self.client.as_test_scenario('Add Rows - Location - Bottom')

        first_row = Row()
        first_row.to_bottom = True
        first_row.cells.append({
            "columnId": 101,
            "value": "Apple"
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Red Fruit"
        })

        response = self.client.Sheets.add_rows(1, [first_row])

        assert response.result[0].row_number == 100

    @clean_api_error
    def test_update_rows_assign_values_string(self):
        self.client.as_test_scenario('Update Rows - Assign Values - String')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "Apple"
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Red Fruit"
        })

        second_row = Row()
        second_row.id = 11
        second_row.cells.append({
            "columnId": 101,
            "value": "Banana"
        })
        second_row.cells.append({
            "columnId": 102,
            "value": "Yellow Fruit"
        })

        response = self.client.Sheets.update_rows(1, [first_row, second_row])

        assert response.result[0].cells[0].display_value == "Apple"

    @clean_api_error
    def test_update_rows_assign_values_int(self):
        self.client.as_test_scenario('Update Rows - Assign Values - Int')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": 100
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "One Hundred"
        })

        second_row = Row()
        second_row.id = 11
        second_row.cells.append({
            "columnId": 101,
            "value": 2.1
        })
        second_row.cells.append({
            "columnId": 102,
            "value": "Two Point One"
        })

        response = self.client.Sheets.update_rows(1, [first_row, second_row])

        assert response.result[0].cells[1].display_value == "One Hundred"

    @clean_api_error
    def test_update_rows_assign_values_bool(self):
        self.client.as_test_scenario('Update Rows - Assign Values - Bool')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": True
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "This is True"
        })

        second_row = Row()
        second_row.id = 11
        second_row.cells.append({
            "columnId": 101,
            "value": False
        })
        second_row.cells.append({
            "columnId": 102,
            "value": "This is False"
        })

        response = self.client.Sheets.update_rows(1, [first_row, second_row])

        assert response.result[1].cells[0].display_value == "false"

    @clean_api_error
    def test_update_rows_assign_formulae(self):
        self.client.as_test_scenario('Update Rows - Assign Formulae')

        first_row = Row()
        first_row.id = 11
        first_row.cells.append({
            "columnId": 101,
            "formula": "=SUM([Column2]3, [Column2]4)*2"
        })
        first_row.cells.append({
            "columnId": 102,
            "formula": "=SUM([Column2]3, [Column2]3, [Column2]4)"
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[0].value == 14

    @clean_api_error
    def test_update_rows_assign_values_hyperlink(self):
        self.client.as_test_scenario('Update Rows - Assign Values - Hyperlink')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "Google",
            "hyperlink": {
                "url": "http://google.com"
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Bing",
            "hyperlink": {
                "url": "http://bing.com"
            }
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[0].hyperlink.url == "http://google.com"

    @clean_api_error
    def test_update_rows_assign_values_hyperlink_sheet_id(self):
        self.client.as_test_scenario('Update Rows - Assign Values - Hyperlink SheetID')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "Sheet2",
            "hyperlink": {
                "sheetId": 2
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Sheet3",
            "hyperlink": {
                "sheetId": 3
            }
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[1].hyperlink.sheet_id == 3

    @clean_api_error
    def test_update_rows_assign_values_hyperlink_report_id(self):
        self.client.as_test_scenario('Update Rows - Assign Values - Hyperlink ReportID')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "Report9",
            "hyperlink": {
                "reportId": 9
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Report8",
            "hyperlink": {
                "reportId": 8
            }
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[1].hyperlink.report_id == 8

    @clean_api_error
    def test_update_rows_invalid_assign_value_and_formulae(self):
        self.client.as_test_scenario('Update Rows - Invalid - Assign Value and Formulae')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "formula": "=SUM([Column2]3, [Column2]4)*2",
            "value": "20"
        })
        first_row.cells.append({
            "columnId": 102,
            "formula": "=SUM([Column2]3, [Column2]3, [Column2]4)"
        })

        with pytest.raises(ApiError) as e:
            self.client.Sheets.update_rows(1, [first_row])

        self.check_error_code(e, 1163)

    @clean_api_error
    def test_update_rows_invalid_assign_hyperlink_url_and_sheet_id(self):
        self.client.as_test_scenario('Update Rows - Invalid - Assign Hyperlink URL and SheetId')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "Google",
            "hyperlink": {
                "url": "http://google.com",
                "sheetId": 2
            }
        })
        first_row.cells.append({
            "columnId": 102,
            "value": "Bing",
            "hyperlink": {
                "url": "http://bing.com"
            }
        })

        with pytest.raises(ApiError) as e:
            self.client.Sheets.update_rows(1, [first_row])

        self.check_error_code(e, 1112)

    @clean_api_error
    def test_update_rows_clear_value_text_number(self):
        self.client.as_test_scenario('Update Rows - Clear Value - Text Number')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": ""
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[0].column_id == 101
        assert response.result[0].cells[0].value is None

    @clean_api_error
    def test_update_rows_clear_value_checkbox(self):
        self.client.as_test_scenario('Update Rows - Clear Value - Checkbox')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": ""
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[0].column_id == 101
        assert response.result[0].cells[0].value is False

    @clean_api_error
    def test_update_rows_clear_value_hyperlink(self):
        self.client.as_test_scenario('Update Rows - Clear Value - Hyperlink')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "",
            "hyperlink": ExplicitNull()
        })

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[0].column_id == 101
        assert response.result[0].cells[0].value is None
        assert response.result[0].cells[0].hyperlink is None

    @clean_api_error
    def test_update_rows_clear_value_cell_link(self):
        self.client.as_test_scenario('Update Rows - Clear Value - Cell Link')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": ""
        })
        first_row.cells[0].link_in_from_cell = ExplicitNull()

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].cells[0].column_id == 101
        assert response.result[0].cells[0].value is None
        assert response.result[0].cells[0].link_in_from_cell is None

    @clean_api_error
    def test_update_rows_clear_value_predecessor_list(self):
        self.client.as_test_scenario('Update Rows - Clear Value - Predecessor List')

        row = Row()
        row.id = 10
        row.cells.append({
            'columnId': 123,
            'value': ExplicitNull()
        })

        response = self.client.Sheets.update_rows(1, [row])

        assert response.result[0].cells[0].column_id == 123
        assert response.result[0].cells[0].value is None

    @clean_api_error
    def test_update_rows_invalid_assign_hyperlink_and_cell_link(self):
        self.client.as_test_scenario('Update Rows - Invalid - Assign Hyperlink and Cell Link')

        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "",
            "linkInFromCell": {
                "sheetId": 2,
                "rowId": 20,
                "columnId": 201
            },
            "hyperlink": {
                "url": "www.google.com"
            }
        })

        with pytest.raises(ApiError) as e:
            self.client.Sheets.update_rows(1, [first_row])

        self.check_error_code(e, 1109)

    @clean_api_error
    def test_update_rows_location_top(self):
        self.client.as_test_scenario('Update Rows - Location - Top')
        first_row = Row()
        first_row.id = 10
        first_row.to_top = True

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].row_number == 1

    @clean_api_error
    def test_update_rows_location_bottom(self):
        self.client.as_test_scenario('Update Rows - Location - Bottom')
        first_row = Row()
        first_row.id = 10
        first_row.to_bottom = True

        response = self.client.Sheets.update_rows(1, [first_row])

        assert response.result[0].row_number == 100

    @clean_api_error
    def test_move_row_to_another_sheet(self):
        self.client.as_test_scenario('Move row to another sheet')

        result = self.client.Sheets.move_rows(
            1228520367122308,
            self.client.models.CopyOrMoveRowDirective({
                'row_ids': [1765250516182916],
                'to': self.client.models.CopyOrMoveRowDestination({
                    'sheet_id': 799249123305348
                })
            })
        )

        assert result.destination_sheet_id == 799249123305348

    @clean_api_error
    def test_copy_row_to_another_sheet(self):
        self.client.as_test_scenario('Copy row to another sheet')

        result = self.client.Sheets.copy_rows(
            1228520367122308,
            self.client.models.CopyOrMoveRowDirective({
                'row_ids': [2891150423025540],
                'to': self.client.models.CopyOrMoveRowDestination({
                    'sheet_id': 799249123305348
                })
            })
        )

        assert result.destination_sheet_id == 799249123305348
