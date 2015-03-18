import sys
import datetime
import unittest
from smartsheetclient import SmartsheetClient, SheetInfo, RowWrapper, Column, CellTypes, CellHyperlink
import logging
log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG, format=log_format)

api_token = 'UNSET'


class CellAccessTest(unittest.TestCase):
    logger = None
    client = None
    columns = []
    sheet = None


    def setUp(self):
        self.logger = logging.getLogger()
        self.client = SmartsheetClient(api_token, logger=self.logger)

        time_str = str(datetime.datetime.utcnow())
        self.new_sheet_name = 'TestCellAccess-%s' % time_str

        col_1 = Column("Col 1 - TextNumber", type=CellTypes.TextNumber,
                primary=True)
        col_2 = Column("Col 2 - Date", type=CellTypes.Date)
        col_3 = Column("Col 3 - Picklist" , type=CellTypes.Picklist,
                options=['Yes', 'No', 'Maybe'])
        col_4 = Column("Col 4 - Checkbox", type=CellTypes.Checkbox)
        col_5 = Column("Col 5 - ContactList", type=CellTypes.ContactList)
        col_6 = Column("Col 6 - TextNumber", type=CellTypes.TextNumber)
        self.columns = [col_1, col_2, col_3, col_4, col_5, col_6]

        self.sheet_info = self.client.createSheet(self.new_sheet_name,
                self.columns, location='')
        if self.sheet_info is None:
            err = "Failed (probably) to create sheet: %s" % self.new_sheet_name
            self.logger.error(err)
            raise Exception(err)
        self.sheet = self.sheet_info.loadSheet()
        if self.sheet is None:
            err = "Unable to load newly created sheet: %s" % self.new_sheet_name
            self.logger.error(err)
            raise Exception(err)

        self.logger.info("######### Adding Rows to new Sheet ############")

        rw = self.sheet.makeRowWrapper()
        r = rw.makeRow()
        r[0] = "one"
        r[1] = '2014-12-25'
        r[5] = "one.five"
        rw.addRow(r)

        r = rw.makeRow()
        r[0] = "two"
        r[2] = "Yes"
        r[5] = "two.five"
        rw.addRow(r)

        r = rw.makeRow()
        r[0] = "three"
        r[3] = True
        r[5] = "three.five"
        rw.addRow(r)

        self.sheet.addRows(rw)

        self.logger.info("########### Test %s uses Sheet: %s ############",

                self.__class__.__name__, self.new_sheet_name)


    def tearDown(self):
        sheet_name = self.sheet.name
        self.sheet.delete()
        self.logger.info("Sheet %s deleted", sheet_name)


    def test_cell_access(self):
        '''Test the various approaches to Cell access.'''
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[1].getCellByIndex(0).value == "one")
        col_0 = self.sheet.getColumnByIndex(0)
        self.assertTrue(col_0 is not None)
        self.assertTrue(self.sheet[1].getCellByColumnId(col_0.id).value == "one")

        row_1 = self.sheet.getRowByRowNumber(1)
        self.assertTrue(row_1 is not None)
        self.assertTrue(row_1[0] == "one")
        self.assertTrue(row_1.getCellByIndex(5).value == "one.five")

        self.assertTrue(self.sheet[3][0] == "three")
        self.assertTrue(self.sheet[3].getCellByIndex(0).value == "three")
        self.assertTrue(self.sheet[3][5] == "three.five")
        self.assertTrue(self.sheet[3].getCellByIndex(5).value == "three.five")


    def test_add_hyperlink_to_existing_row(self):
        '''Test adding a CellHyperlink to an existing Row.'''
        link_target = 'http://www.smartsheet.com/developers/api-documentation'
        link = CellHyperlink(url=link_target)
        self.sheet.enableCache()
        cell = self.sheet[1].getCellByIndex(0)
        self.assertTrue(cell.value == "one")
        cell.assign("API Docs", hyperlink=link)

        self.assertTrue(self.sheet[1][0] == "API Docs")
        self.assertTrue(self.sheet[1].getCellByIndex(0).value == "API Docs")
        self.assertTrue(self.sheet[1].getCellByIndex(0).hyperlink.url == link_target)
        cell.save()

        self.assertTrue(self.sheet[1][0] == "API Docs")
        self.assertTrue(self.sheet[1].getCellByIndex(0).value == "API Docs")
        self.assertTrue(self.sheet[1].getCellByIndex(0).hyperlink.url == link_target)


    def test_add_hyperlink_to_new_row(self):
        '''Test adding a CellHyperlink to a new Row.'''
        link_target = 'http://www.smartsheet.com/blog'
        link = CellHyperlink(url=link_target)
        r = self.sheet.makeRow()

        r.getCellByIndex(0).assign('Smartsheet Blog', hyperlink=link)

        self.assertTrue(r[0] == 'Smartsheet Blog')
        self.assertTrue(r.getCellByIndex(0).value == 'Smartsheet Blog')
        self.assertTrue(r.getCellByIndex(0).hyperlink.url == link_target)

        self.sheet.addRow(r, position='toTop')

        self.assertTrue(r[0] == 'Smartsheet Blog')
        self.assertTrue(r.getCellByIndex(0).value == 'Smartsheet Blog')
        self.assertTrue(r.getCellByIndex(0).hyperlink.url == link_target)


    def test_changing_multiple_cells_on_a_row_list_sytle(self):
        self.sheet[1][0] = "blue"
        self.sheet[1][5] = "green"
        self.sheet[1].save()

        self.assertTrue(self.sheet[1][0] == "blue")
        self.assertTrue(self.sheet[1][5] == "green")


    def test_changing_multiple_cells_on_a_row_oo_style_cache_enabled(self):
        # Have to enable cache to be able to change multiple Cells on a Row.
        self.sheet.enableCache()
        self.sheet.getRowByRowNumber(1).getCellByIndex(0).assign("blue")
        self.sheet.getRowByRowNumber(1).getCellByIndex(5).assign("green")
        self.sheet.getRowByRowNumber(1).save()

        self.assertTrue(self.sheet[1][0] == "blue")
        self.assertTrue(self.sheet[1][5] == "green")

    def test_changing_multiple_cells_on_a_row_oo_style_without_cache_enabled(self):
        row = self.sheet.getRowByRowNumber(1)
        row.getCellByIndex(0).assign("blue")
        row.getCellByIndex(5).assign("green")
        row.save()

        self.assertTrue(self.sheet[1][0] == "blue")
        self.assertTrue(self.sheet[1][5] == "green")

    def test_changing_multiple_cells_on_a_row_but_oo_no_cache_loses_all_but_last_write(self):
        '''
        In OO access mode, the Row is refetched on each access, as a result,
        changes to multiple Cells on the Row will lose all but the first one.
        Unless the Row is fetched and then used without refetching (as in the
        test case test_changing_multiple_cells_on_a_row_oo_style_without_cache_enabled).
        '''
        self.sheet.getRowByRowNumber(1).getCellByIndex(0).assign("blue")
        self.sheet.getRowByRowNumber(1).getCellByIndex(5).assign("green")
        prior_cache_state = self.sheet.forceCache()
        self.sheet.getRowByRowNumber(1).save()
        self.sheet.restoreCache(prior_cache_state)

        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[1][5] == "green")


    def notest_save_with_vs_without_strict(self):
        '''Test assignments with and without 'strict' setting.'''
        raise NotImplementedError


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1] 
    unittest.main()

