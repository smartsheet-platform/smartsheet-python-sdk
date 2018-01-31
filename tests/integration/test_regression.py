import pytest
import six
import os.path
from datetime import date

_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.usefixtures("smart_setup")
class TestRegression:

    def test_link_in_from_cell(self, smart_setup):
        smart = smart_setup['smart']

        sheet = smart_setup['sheet']
        row = smart.models.Row()
        row.to_bottom = True
        col_id = sheet.columns[0].id
        row.cells.append({
            'column_id': col_id,
            'value': 'abc123'
        })

        action = smart.Sheets.add_rows(sheet.id, [row])
        added_row = action.result[0]

        assert isinstance(added_row, smart.models.row.Row)
        assert action.request_response.status_code == 200

        sheet_b = smart_setup['sheet_b']
        cell_link = smart.models.CellLink()
        cell_link.sheet_id = sheet_b.id
        cell_link.row_id = sheet_b.rows[0].id
        cell_link.column_id = sheet_b.columns[0].id

        cell = smart.models.Cell()
        cell.column_id = col_id
        cell.link_in_from_cell = cell_link
        cell.value = smart.models.ExplicitNull()

        row = smart.models.Row()
        row.id = added_row.id
        row.cells.append(cell)

        action = smart.Sheets.update_rows(sheet.id, [row])
        assert action.request_response.status_code == 200

        action = smart.Sheets.delete_rows(sheet.id, [added_row.id])
        assert action.request_response.status_code == 200

    def test_strict(self, smart_setup):
        smart = smart_setup['smart']

        sheet = smart_setup['sheet']
        col_id = sheet.columns[0].id

        row_1 = smart.models.Row()
        row_1.to_bottom = True
        row_1.cells.append({
            'column_id': col_id,
            'strict': True,
            'value': 0
        })

        row_2 = smart.models.Row()
        row_2.to_bottom = True
        row_2.cells.append({
            'column_id': col_id,
            'strict': True,
            'value': '0'
        })

        row_3 = smart.models.Row()
        row_3.to_bottom = True
        row_3.cells.append({
            'column_id': col_id,
            'strict': False,
            'value': 0
        })

        row_4 = smart.models.Row()
        row_4.to_bottom = True
        row_4.cells.append({
            'column_id': col_id,
            'strict': False,
            'value': '0'
        })

        action = smart.Sheets.add_rows(sheet.id, [row_1, row_2, row_3, row_4])

        # strict, num - expecting numeric
        assert isinstance(action.result[0].cells[0].value, (six.integer_types, float))
        # strict, str - expecting str
        assert isinstance(action.result[1].cells[0].value, six.string_types)
        # not strict, num - expecting numeric
        assert isinstance(action.result[2].cells[0].value, (six.integer_types, float))
        # not strict, str - expecting numeric
        assert isinstance(action.result[3].cells[0].value, (six.integer_types, float))

        row_1 = smart.models.Row()
        row_1.id = action.result[0].id
        row_1.cells.append({
            'column_id': col_id,
            'strict': True,
            'value': 1
        })

        row_2 = smart.models.Row()
        row_2.id = action.result[1].id
        row_2.cells.append({
            'column_id': col_id,
            'strict': True,
            'value': '1'
        })

        row_3 = smart.models.Row()
        row_3.id = action.result[2].id
        row_3.cells.append({
            'column_id': col_id,
            'strict': False,
            'value': 1
        })

        row_4 = smart.models.Row()
        row_4.id = action.result[3].id
        row_4.cells.append({
            'column_id': col_id,
            'strict': False,
            'value': '1'
        })

        action = smart.Sheets.update_rows(sheet.id, [row_1, row_2, row_3, row_4])
        assert action.request_response.status_code == 200

        # strict, num - expecting numeric
        assert isinstance(action.result[0].cells[0].value, (six.integer_types, float))
        # strict, str - expecting str
        assert isinstance(action.result[1].cells[0].value, six.string_types)
        # not strict, num - expecting numeric
        assert isinstance(action.result[2].cells[0].value, (six.integer_types, float))
        # not strict, str - expecting numeric
        assert isinstance(action.result[3].cells[0].value, (six.integer_types, float))

        action = smart.Sheets.delete_rows(sheet.id, [action.result[0].id, action.result[1].id,
                                                     action.result[2].id, action.result[3].id])
        assert action.request_response.status_code == 200

    def test_validation(self, smart_setup):
        smart = smart_setup['smart']

        sheet_spec = smart.models.Sheet({
            'name': 'my validation sheet',
            'columns': [{
                'title': 'col 1',
                'type': 'DATE'
            }, {
                'title': 'col 2',
                'primary': True,
                'type': 'TEXT_NUMBER'
            }]
        })
        action = smart.Home.create_sheet(sheet_spec)
        assert action.message == 'SUCCESS'
        sheet = action.result

        col1 = smart.models.Column()
        col1.validation = True
        action = smart.Sheets.update_column(sheet.id, sheet.columns[0].id, col1)
        assert action.message == 'SUCCESS'

        sheet_row = smart.models.Row({
            'to_top': True,
            'cells': [{
                'column_id': sheet.columns[0].id,
                'value': date.today().strftime("%Y-%m-%d")
            }, {
                'column_id': sheet.columns[1].id,
                'value': 'this is a test'
            }]
        })
        action = smart.Sheets.add_rows(sheet.id, [sheet_row])
        assert action.message == 'SUCCESS'

        sheet_row = smart.models.Row({
            'to_top': True,
            'cells': [{
                'column_id': sheet.columns[0].id,
                'value': 'this is an invalid value'
            }, {
                'column_id': sheet.columns[1].id,
                'value': 'this is a test'
            }]
        })
        action = smart.Sheets.add_rows(sheet.id, [sheet_row])
        assert action.message == 'ERROR'

        sheet_row.cells[0].override_validation = True
        sheet_row.cells[0].strict = False
        action = smart.Sheets.add_rows(sheet.id, [sheet_row])
        assert action.message == 'SUCCESS'

        sheet = smart.Sheets.get_sheet(sheet.id)
        action = smart.Cells.add_image_to_cell(sheet.id, sheet.rows[0].id, sheet.columns[0].id,
                                               _dir + '/fixtures/stooges_v1.jpg', 'image/jpeg')
        # expect error here because we did not override validation
        assert action.message == 'ERROR'

        action = smart.Cells.add_image_to_cell(sheet.id, sheet.rows[0].id, sheet.columns[0].id,
                                               _dir + '/fixtures/stooges_v1.jpg', 'image/jpeg', True)
        # expect error here because we did not override validation
        assert action.message == 'SUCCESS'

        # clean up
        action = smart.Sheets.delete_sheet(sheet.id)
        assert action.message == 'SUCCESS'
