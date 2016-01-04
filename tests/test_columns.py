import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestColumns:
    test_columns = None

    def test_add_columns(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].add_columns([
            smart.models.Column({
                'title': 'Cheese',
                'type': 'TEXT_NUMBER',
                'index': 1
            }),
            smart.models.Column({
                'title': 'Hotdog',
                'type': 'TEXT_NUMBER',
                'index': 1
            })
        ])
        sheet = action.result
        assert action.message == 'SUCCESS'

    def test_add_column_with_dict(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].add_columns({
            'title': 'Model',
            'type': 'TEXT_NUMBER',
            'index': 2
        })
        sheet = action.result
        assert action.message == 'SUCCESS'

    def test_get_columns(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].get_columns()
        columns = action.result
        TestColumns.test_columns = columns
        assert action.total_count > 0

    def test_get_column(self, smart_setup):
        smart = smart_setup['smart']
        some_column = smart_setup['sheet'].columns.pop()
        column = smart_setup['sheet'].get_column(some_column.id)
        assert isinstance(column.id, int)

    def test_update_column(self, smart_setup):
        smart = smart_setup['smart']
        for idx, col in enumerate(TestColumns.test_columns):
            if col.title == 'Hotdog':
                break
        col.title = 'Brand of Hotdog'
        action = smart.Sheets.update_column(
            smart_setup['sheet'].id,
            col.id,
            col
        )
        column = action.result
        assert action.message == 'SUCCESS'

    def test_delete_column(self, smart_setup):
        smart = smart_setup['smart']
        for idx, col in enumerate(TestColumns.test_columns):
            if col.title == 'Disposable':
                break
        action = smart.Sheets.delete_column(
            smart_setup['sheet'].id,
            col.id
        )
        assert action.message == 'SUCCESS'
