import sys
import datetime
import unittest
from smartsheetclient import SmartsheetClient, SheetInfo, Column, CellTypes
import logging
logging.basicConfig(filename='tests.log', level=logging.DEBUG)

api_token = 'UNSET'


class RowAddDeleteTest(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.client = SmartsheetClient(api_token, logger=self.logger)

        time_str = str(datetime.datetime.utcnow())
        self.new_sheet_name = 'test-row_add-%s' % time_str

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
        self.logger.info("########### Test uses Sheet: %s ############",
                self.new_sheet_name)

    def test_add_and_delete_rows(self):
        row_1 = self.sheet.makeRow()
        row_1[0] = "Row 1:0"
        self.sheet.addRow(row_1, position='toBottom')
        # self.logger.debug("row 1 values: %r" % list(self.sheet[1]))

        self.assertTrue(len(self.sheet.rows) == 1)
        self.assertTrue(self.sheet[1][0] == "Row 1:0")
        self.assertTrue(self.sheet.getRowByRowNumber(1) == self.sheet[1])

        row_2 = self.sheet.makeRow()
        row_2[0] = "Row 2:0 -- bottom"
        self.sheet.addRow(row_2)
        # self.logger.debug("row 2 values: %r" % list(self.sheet[2]))

        self.assertTrue(len(self.sheet.rows) == 2)
        self.assertTrue(self.sheet[2][0] == "Row 2:0 -- bottom")
        self.assertTrue(self.sheet.getRowByRowNumber(2) == self.sheet[2])

        # Refetch is necessary to make sure the Rows are in the right order.
        self.sheet = self.sheet.refetch()

        self.assertTrue(self.sheet is not None)
        self.assertTrue(len(self.sheet.rows) == 2)
        self.assertTrue(self.sheet[1][0] == "Row 1:0")
        self.assertTrue(self.sheet[2][0] == "Row 2:0 -- bottom")

        # Add a Row at the top, this will move the others down.
        row_3 = self.sheet.makeRow()
        row_3[0] = "New Top Row"
        self.sheet.addRow(row_3, position='toTop')

        # Refetch is necessary to make sure the Rows are in the right order.
        self.sheet = self.sheet.refetch()
        self.assertTrue(self.sheet[1][0] == "New Top Row")
        self.assertTrue(self.sheet[2][0] == "Row 1:0")
        self.assertTrue(self.sheet[3][0] == "Row 2:0 -- bottom")

        # TODO: Do row deletion.

   

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1] 
    unittest.main()

