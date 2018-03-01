import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestCrossSheetReferences:

    def test_create_cross_sheet_reference(self, smart_setup):
        smart = smart_setup['smart']
        xref = smart.models.CrossSheetReference()
        xref.source_sheet_id = smart_setup['sheet_b'].id
        xref.start_column_id = smart_setup['sheet_b'].columns[0].id
        xref.end_column_id = smart_setup['sheet_b'].columns[0].id
        action = smart.Sheets.create_cross_sheet_reference(smart_setup['sheet'].id, xref)
        assert action.message == 'SUCCESS'

    def test_list_cross_sheet_references(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.list_cross_sheet_references(smart_setup['sheet'].id)
        assert isinstance(action.data[0], smart.models.CrossSheetReference)

    def test_get_cross_sheet_references(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.get_sheet(smart_setup['sheet'].id, include='crossSheetReferences')
        assert isinstance(action, smart.models.Sheet)
        assert len(action.cross_sheet_references) == 1

        action = smart.Sheets.get_cross_sheet_reference(smart_setup['sheet'].id, action.cross_sheet_references[0].id)
        assert isinstance(action, smart.models.CrossSheetReference)


