import sys
import datetime
import unittest
from smartsheetclient import SmartsheetClient, SheetInfo, RowWrapper, Column, CellTypes
import logging
log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG, format=log_format)


api_token = 'UNSET'


class ColumnUpdateTest(unittest.TestCase):
    logger = None
    client = None
    columns = []
    sheet = None


    def setUp(self):
        self.logger = logging.getLogger()
        self.client = SmartsheetClient(api_token, logger=self.logger)

        time_str = str(datetime.datetime.utcnow())
        self.new_sheet_name = 'TestColumnUpdate-%s' % time_str

        col_1 = Column("Col 1 - TextNumber", type=CellTypes.TextNumber,
                primary=True)
        col_2 = Column("Col 2 - Date", type=CellTypes.Date)
        col_3 = Column("Col 3 - Picklist" , type=CellTypes.Picklist,
                options=['Yes', 'No', 'Maybe'])
        col_4 = Column("Col 4 - Checkbox", type=CellTypes.Checkbox)
        # col_5 = Column("Col 5 - ContactList", type=CellTypes.ContactList)
        # self.columns = [col_1, col_2, col_3, col_4, col_5]
        self.columns = [col_1, col_2, col_3, col_4]

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

    def test_update_column_title(self):
        '''Test updating a column's title.'''
        self.sheet.columns[0].title = 'New Title'
        self.sheet.columns[0].update()

        self.assertTrue(self.sheet.columns[0].title == 'New Title')


    def test_update_column_index(self):
        '''Test changing a column's index.'''
        self.sheet.columns[1].index = 3
        self.sheet.columns[1].update()

        self.assertTrue(self.sheet.columns[3].title == "Col 2 - Date")
        self.assertTrue(self.sheet.columns[1].title == "Col 3 - Picklist")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with open(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1] 
    unittest.main()

