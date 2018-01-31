import pytest


@pytest.mark.usefixtures("smart_setup")
class TestObjectValue:

    def test_get_sheet_object_value(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.Sheets.get_sheet(smart_setup['sheet'].id, include='objectValue')
        assert isinstance(sheet.rows[0].cells[0].object_value, smart.models.StringObjectValue)
        assert isinstance(sheet, smart.models.Sheet)

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
        p1.row_id = task1_row.id

        p2 = smart.models.Predecessor()
        p2.type = 'FS'
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
        for col in sheet.columns:
            if col.type == 'PREDECESSOR':
                row.cells.append({
                    'column_id': col.id,
                    'value': smart.models.ExplicitNull()
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
