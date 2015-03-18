import sys
import datetime
import unittest
from smartsheetclient import SmartsheetClient, SheetInfo, RowWrapper, Column, CellTypes
import logging
log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG, format=log_format)


api_token = 'UNSET'


class RowAddDeleteTest(unittest.TestCase):
    logger = None
    client = None
    columns = []
    sheet = None


    def setUp(self):
        self.logger = logging.getLogger()
        self.client = SmartsheetClient(api_token, logger=self.logger)

        time_str = str(datetime.datetime.utcnow())
        self.new_sheet_name = 'TestRowAddDelete-%s' % time_str

        col_1 = Column("Col 1 - TextNumber", type=CellTypes.TextNumber,
                primary=True)
        col_2 = Column("Col 2 - Date", type=CellTypes.Date)
        col_3 = Column("Col 3 - Picklist" , type=CellTypes.Picklist,
                options=['Yes', 'No', 'Maybe'])
        col_4 = Column("Col 4 - Checkbox", type=CellTypes.Checkbox)
        col_5 = Column("Col 5 - ContactList", type=CellTypes.ContactList)
        self.columns = [col_1, col_2, col_3, col_4, col_5]

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
        self.logger.info("########### Test %s uses Sheet: %s ############",
                self.__class__.__name__, self.new_sheet_name)


    def tearDown(self):
        sheet_name = self.sheet.name
        self.sheet.delete()
        self.logger.info("Sheet %s deleted", sheet_name)


    def test_add_rows_to_top_of_sheet(self):
        '''Add Rows, one at a time, to the top of an initially blank Sheet.'''
        r = self.sheet.makeRow()
        r[0] = "one"
        self.sheet.addRow(r, position='toTop')
        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "one")

        r = self.sheet.makeRow()
        r[0] = "two"
        self.sheet.addRow(r, position='toTop')
        self.assertTrue(len(self.sheet) == 2)
        self.assertTrue(self.sheet[1][0] == "two")
        self.assertTrue(self.sheet[2][0] == "one")

        r = self.sheet.makeRow()
        r[0] = "three"
        self.sheet.addRow(r, position='toTop')
        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "three")
        self.assertTrue(self.sheet[2][0] == "two")
        self.assertTrue(self.sheet[3][0] == "one")

    def test_add_rows_to_bottom_of_sheet(self):
        r = self.sheet.makeRow()
        r[0] = "one"
        self.sheet.addRow(r, position='toBottom')
        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "one")

        r = self.sheet.makeRow()
        r[0] = "two"
        self.sheet.addRow(r, position='toBottom')
        self.assertTrue(len(self.sheet) == 2)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")

        r = self.sheet.makeRow()
        r[0] = "three"
        self.sheet.addRow(r, position='toBottom')
        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")
        self.assertTrue(self.sheet[3][0] == "three")


    def test_add_row_between_rows_on_sheet(self):
        r = self.sheet.makeRow()
        r[0] = "one"
        self.sheet.addRow(r, position='toBottom')
        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "one")

        r = self.sheet.makeRow()
        r[0] = "two"
        self.sheet.addRow(r, position='toBottom')
        self.assertTrue(len(self.sheet) == 2)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")

        r = self.sheet.makeRow()
        r[0] = "one-two"
        self.sheet.addRow(r, siblingId=self.sheet[1].id)
        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "one-two")
        self.assertTrue(self.sheet[3][0] == "two")


    def test_add_multiple_rows_to_blank_sheet(self):
        '''Add multiple Rows at once to the top of a blank/empty Sheet.'''
        # Add two rows at once at the very top of a blank Sheet.
        row_1 = self.sheet.makeRow()
        row_1[0] = 'one'
        row_2 = self.sheet.makeRow()
        row_2[0] = 'two'

        rw = RowWrapper(self.sheet, position='toTop')
        rw.addRow(row_1)
        rw.addRow(row_2)

        self.assertTrue(len(rw.rows) == 2)
        res = self.sheet.addRows(rw)
        self.assertTrue(res is not None)

        self.assertTrue(self.sheet[1][0] == 'one')
        self.assertTrue(self.sheet[2][0] == 'two')

   
    def test_add_multiple_rows_to_top_of_one_row_sheet(self):
        '''Add multiple Rows at once to the top of a one-row Sheet.'''
        r = self.sheet.makeRow()
        r[0] = "one"
        self.sheet.addRow(r, position='toBottom')
        r = self.sheet.makeRow()

        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "one")

        rw = self.sheet.makeRowWrapper(position='toTop')
        r = rw.makeRow()
        r[0] = "New Top Row"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "Second Row From Top"
        rw.addRow(r)

        self.sheet.addRows(rw)

        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "New Top Row")
        self.assertTrue(self.sheet[2][0] == "Second Row From Top")
        self.assertTrue(self.sheet[3][0] == "one")


    def test_add_multiple_rows_below_a_one_row_sheet__without_position_equal_toBottom(self):
        '''
        Add multiple Rows at once as a sibling to the Row in a one-row Sheet.
        '''
        r = self.sheet.makeRow()
        r[0] = "one"
        self.sheet.addRow(r, position='toBottom')

        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "one")

        rw = self.sheet.makeRowWrapper(siblingId=self.sheet[1].id)
        r = rw.makeRow()
        r[0] = "Second Row From Top"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "Third Row From Top"
        rw.addRow(r)

        self.sheet.addRows(rw)

        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "Second Row From Top")
        self.assertTrue(self.sheet[3][0] == "Third Row From Top")


    def test_add_multiple_rows_between_rows(self):
        '''
        Add multiple Rows at once between the Rows in a Sheet.
        '''
        rw = self.sheet.makeRowWrapper(position='toBottom')
        r = rw.makeRow()
        r[0] = "one"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "two"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "three"
        rw.addRow(r)

        self.sheet.addRows(rw)

        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")
        self.assertTrue(self.sheet[3][0] == "three")

        rw = self.sheet.makeRowWrapper(siblingId=self.sheet[1].id)
        r = rw.makeRow()
        r[0] = "one-one"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "one-two"
        rw.addRow(r)

        res = self.sheet.addRows(rw)
        self.assertTrue(len(self.sheet) == 5)
        self.assertTrue(res is not None)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "one-one")
        self.assertTrue(self.sheet[3][0] == "one-two")
        self.assertTrue(self.sheet[4][0] == "two")
        self.assertTrue(self.sheet[5][0] == "three")


    def test_add_multiple_rows_just_before_the_last_row(self):
        rw = self.sheet.makeRowWrapper(position='toBottom')
        r = rw.makeRow()
        r[0] = "one"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "two"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "three"
        rw.addRow(r)

        self.sheet.addRows(rw)

        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")
        self.assertTrue(self.sheet[3][0] == "three")

        rw = self.sheet.makeRowWrapper(siblingId=self.sheet[2].id)
        r = rw.makeRow()
        r[0] = "two-one"
        rw.addRow(r)
        r = rw.makeRow()
        r[0] = "two-two"
        rw.addRow(r)

        res = self.sheet.addRows(rw)
        self.assertTrue(len(self.sheet) == 5)
        self.assertTrue(res is not None)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")
        self.assertTrue(self.sheet[3][0] == "two-one")
        self.assertTrue(self.sheet[4][0] == "two-two")
        self.assertTrue(self.sheet[5][0] == "three")


    def test_delete_only_row_in_sheet(self):
        '''Test deleting the only Row in a Sheet.'''
        r = self.sheet.makeRow()
        r[0] = "only"
        self.sheet.addRow(r)

        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "only")

        res = self.sheet[1].delete()

        self.assertTrue(len(self.sheet) == 0)

    def test_delete_rows_in_sheet_with_multiple_rows(self):
        '''Delete Rows from a Sheet with multiple Rows.'''
        rw = self.sheet.makeRowWrapper(position='toTop')
        r = rw.makeRow(); r[0] = "one"; rw.addRow(r)
        r = rw.makeRow(); r[0] = "two"; rw.addRow(r)
        r = rw.makeRow(); r[0] = "three"; rw.addRow(r)
        r = rw.makeRow(); r[0] = "four"; rw.addRow(r)
        self.sheet.addRows(rw)

        self.assertTrue(len(self.sheet) == 4)
        self.assertTrue(self.sheet[1][0] == "one")
        self.assertTrue(self.sheet[2][0] == "two")
        self.assertTrue(self.sheet[3][0] == "three")
        self.assertTrue(self.sheet[4][0] == "four")

        self.sheet[1].delete()
        self.assertTrue(len(self.sheet) == 3)
        self.assertTrue(self.sheet[1][0] == "two")
        self.assertTrue(self.sheet[2][0] == "three")
        self.assertTrue(self.sheet[3][0] == "four")

        self.sheet[3].delete()
        self.assertTrue(len(self.sheet) == 2)
        self.assertTrue(self.sheet[1][0] == "two")
        self.assertTrue(self.sheet[2][0] == "three")

        self.sheet[-2].delete()
        self.assertTrue(len(self.sheet) == 1)
        self.assertTrue(self.sheet[1][0] == "three")

        self.sheet[-1].delete()
        self.assertTrue(len(self.sheet) == 0)




   

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1] 
    unittest.main()

