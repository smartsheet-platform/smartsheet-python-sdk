import pytest
import smartsheet
from smartsheet.models.enums import ColumnType


@pytest.mark.usefixtures("smart_setup")
class TestMultiPicklist:

    def test_add_multi_picklist_column(self, smart_setup):
        smart = smart_setup['smart']
        mpl = smartsheet.models.Column({
            'title': 'This is a multi-picklist column',
            'index': 0,
            'type': ColumnType.MULTI_PICKLIST,
            'options': ['Cat', 'Rat', 'Bat']
        })
        action = smart.Sheets.add_columns(smart_setup['sheet'].id, [mpl])
        assert action.message == 'SUCCESS'
        smart_setup['multi_picklist_col_id'] = action.data[0].id

    def test_list_multi_picklist_column(self, smart_setup):
        smart = smart_setup['smart']
        cols = smart.Sheets.get_columns(smart_setup['sheet'].id, level=None)
        # should be TEXT_NUMBER since level not specified
        assert cols.data[0].type == ColumnType.TEXT_NUMBER

        cols = smart.Sheets.get_columns(smart_setup['sheet'].id, level=2)
        # should be MULTI_PICKLIST since level 2 specified
        assert cols.data[0].type == ColumnType.MULTI_PICKLIST

    def test_add_multi_picklist_row(self, smart_setup):
        smart = smart_setup['smart']

        mplov = smartsheet.models.MultiPicklistObjectValue({
            'values': ['Bat', 'Cat']
        })

        insert_cell = smartsheet.models.Cell({
            'column_id': smart_setup['multi_picklist_col_id'],
            'object_value': mplov
        })

        row = smart.models.Row({
            'to_top': True,
            'cells': [insert_cell]
        })

        action = smart.Sheets.add_rows(smart_setup['sheet'].id, [row])
        assert action.request_response.status_code == 200

    def test_get_multi_picklist_sheet(self, smart_setup):
        smart = smart_setup['smart']

        sheet = smart.Sheets.get_sheet(smart_setup['sheet'].id, include='objectValue',
                                        column_ids=[smart_setup['multi_picklist_col_id']], level=None)
        # should be TEXT_NUMBER since level not specified
        assert isinstance(sheet.rows[0].cells[0].object_value, smartsheet.models.StringObjectValue)

        sheet = smart.Sheets.get_sheet(smart_setup['sheet'].id, include='objectValue',
                                        column_ids=[smart_setup['multi_picklist_col_id']], level=2)
        # should be TEXT_NUMBER since level not specified
        assert isinstance(sheet.rows[0].cells[0].object_value, smartsheet.models.MultiPicklistObjectValue)




