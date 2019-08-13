import pytest
import os.path
import smartsheet

from smartsheet.models.enums.column_type import ColumnType
from smartsheet.models.sheet_summary import SheetSummary
from smartsheet.models.index_result import IndexResult

_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.usefixtures("smart_setup")
class TestSheetSummary:

    def test_add_sheet_summary(self, smart_setup):
        smart = smart_setup['smart']
        summary_field1 = smartsheet.models.SummaryField()
        summary_field1.title = 'today'
        summary_field1.type = ColumnType.DATE
        summary_field1.formula = '=Today()'
        summary_field2 = smartsheet.models.SummaryField()
        summary_field2.title = 'my new summary field'
        summary_field2.type = ColumnType.TEXT_NUMBER
        summary_field_add = smart.Sheets.add_sheet_summary_fields_with_partial_success(smart_setup['sheet_b'].id,
                                                                                    [summary_field1, summary_field2])
        assert summary_field_add.message == 'SUCCESS'

        summary_field_image = smart.Sheets.add_sheet_summary_field_image(smart_setup['sheet_b'].id,
                                                                         summary_field_add.result[0].id,
                                                                         _dir + '/fixtures/curly.jpg', 'image/jpeg')
        assert summary_field_image.message == 'SUCCESS'

    def test_get_sheet_summary(self, smart_setup):
        smart = smart_setup['smart']
        summary = smart.Sheets.get_sheet_summary(smart_setup['sheet_b'].id, include='writerInfo', exclude='displayValue')
        assert isinstance(summary, SheetSummary)

        summary_fields = smart.Sheets.get_sheet_summary_fields(smart_setup['sheet_b'].id, include='format', exclude='image')
        assert isinstance(summary_fields, IndexResult)
        assert summary_fields.total_count > 0

    def test_update_sheet_summary(self, smart_setup):
        smart = smart_setup['smart']
        summary_fields = smart.Sheets.get_sheet_summary_fields(smart_setup['sheet_b'].id, include='format', exclude='image')

        summary_field1 = smartsheet.models.SummaryField()
        summary_field1.id = summary_fields.data[0].id
        summary_field1.title = 'updated field'
        summary_field2 = smartsheet.models.SummaryField({
            'id': 123,
            'title': 'today'
        })
        summary_field_update = smart.Sheets.update_sheet_summary_fields_with_partial_success(smart_setup['sheet_b'].id,
                                                                                             [summary_field1, summary_field2],
                                                                                             rename_if_conflict=True)
        assert summary_field_update.message == 'PARTIAL_SUCCESS'

    def test_delete_sheet_summary(self, smart_setup):
        smart = smart_setup['smart']
        summary_fields = smart.Sheets.get_sheet_summary_fields(smart_setup['sheet_b'].id, include='format', exclude='image')

        summary_delete = smart.Sheets.delete_sheet_summary_fields(smart_setup['sheet_b'].id, [summary_fields.data[0].id, 123],
                                                                  ignore_summary_fields_not_found=True)
        assert summary_delete.message == 'SUCCESS'
