import pytest
import six
import os.path
from datetime import date

_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.usefixtures("smart_setup")
class TestRegression:

    def test_predecessors(self, smart_setup):
        smart = smart_setup['smart']
        templates = smart.Templates.list_public_templates(include_all=True)

        for template in templates.data:
            if template.name == 'Basic Project with Gantt & Dependencies':
                break

        sheet = smart.models.Sheet({
            'name': 'example_project_python_sdk' + smart_setup['now'],
            'fromId': template.id
        })
        action = smart.Home.create_sheet_from_template(sheet)
        sheet = action.result
        assert action.message == 'SUCCESS'

        sheet = smart.Sheets.get_sheet(sheet.id)

        # add 'Task1'
        row = smart.models.Row()
        row.to_bottom = True
        for col in sheet.columns:
            if col.primary:
                row.cells.append({
                    'column_id': col.id,
                    'value': 'Task1'
                })
                break

        action = smart.Sheets.add_rows(sheet.id, [row])
        task1_row = action.result[0]

        assert isinstance(task1_row, smart.models.row.Row)
        assert action.request_response.status_code == 200

        # add 'Task2' with 'Task1' predecessor
        p1 = smart.models.Predecessor()
        p1.type = 'FS'
        p1.row_number = task1_row.row_number
        p1.row_id = task1_row.id

        predecessor_list = smart.models.PredecessorList()
        predecessor_list.predecessors = [p1]

        row = smart.models.Row()
        row.to_bottom = True
        for col in sheet.columns:
            if col.primary:
                row.cells.append({
                    'column_id': col.id,
                    'value': 'Task2'
                })
            if col.type == 'PREDECESSOR':
                row.cells.append({
                    'column_id': col.id,
                    'object_value': predecessor_list
                })

        action = smart.Sheets.add_rows(sheet.id, [row])
        task2_row = action.result[0]
        assert isinstance(task2_row, smart.models.row.Row)
        assert action.request_response.status_code == 200

        # add 'Task3' with 'Task1','Task2' predecessors
        p1 = smart.models.Predecessor()
        p1.type = 'FS'
        p1.row_number = task1_row.row_number
        p1.row_id = task1_row.id

        p2 = smart.models.Predecessor()
        p2.type = 'FS'
        p2.row_number = task2_row.row_number
        p2.row_id = task2_row.id

        predecessor_list = smart.models.PredecessorList()
        predecessor_list.predecessors = [p1, p2]

        row = smart.models.Row()
        row.to_bottom = True
        for col in sheet.columns:
            if col.primary:
                row.cells.append({
                    'column_id': col.id,
                    'value': 'Task3'
                })
            if col.type == 'PREDECESSOR':
                row.cells.append({
                    'column_id': col.id,
                    'object_value': predecessor_list
                })

        action = smart.Sheets.add_rows(sheet.id, [row])
        task3_row = action.result[0]
        assert isinstance(task3_row, smart.models.row.Row)
        assert action.request_response.status_code == 200

        # clear the predecessor list from task 3
        row = smart.models.Row()
        row.id = task3_row.id
        row.row_number = task3_row.row_number
        for col in sheet.columns:
            if col.type == 'PREDECESSOR':
                row.cells.append({
                    'column_id': col.id
                })
                break

        action = smart.Sheets.update_rows(sheet.id, [row])
        assert action.request_response.status_code == 200
        for cell in action.data[0].cells:
            if cell.column_id == col.id:
                break;
        assert cell.object_value is None

        # clean up
        action = smart.Sheets.delete_sheet(sheet.id)
        assert action.message == 'SUCCESS'

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
