import sys
import datetime
import unittest
from smartsheetclient import SmartsheetClient, SheetInfo, Column, CellTypes, SmartsheetClientError
import logging
log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG, format=log_format)


api_token = 'UNSET'


class CreateSheetTest(unittest.TestCase):


    def setUp(self):
        self.logger = logging.getLogger()
        self.client = SmartsheetClient(api_token, logger=self.logger)

        time_str = str(datetime.datetime.utcnow())
        self.new_sheet_name = 'testSheetCreateDelete-%s' % time_str

        col_1 = Column("Col 1 - TextNumber", type=CellTypes.TextNumber,
                primary=True)
        col_2 = Column("Col 2 - Date", type=CellTypes.Date)
        col_3 = Column("Col 3 - Picklist" , type=CellTypes.Picklist,
                options=['Yes', 'No', 'Maybe'])
        col_4 = Column("Col 4 - Checkbox", type=CellTypes.Checkbox)
        col_5 = Column("Col 5 - ContactList", type=CellTypes.ContactList)
        self.columns = [col_1, col_2, col_3, col_4, col_5]
        # TODO: Add some system or autonumber columns.
        self.logger.info("########### Test uses Sheet: %s ############",
                                self.new_sheet_name)

    def test_create_and_delete_sheet(self):
        '''
        Test the creation of a new Sheet and the deletion of it.
        '''
        si = self.client.createSheet(self.new_sheet_name, self.columns,
                location='')

        self.assertIsNotNone(si) 
        self.assertIsInstance(si, SheetInfo)
        self.assertEqual(si.name, self.new_sheet_name)
        self.assertIsNotNone(si.permalink)

        # Make sure it shows up on the SheetList by name.
        sheet_list = self.client.fetchSheetInfoByName(self.new_sheet_name)
        self.assertIsNotNone(sheet_list)
        self.assertEqual(1, len(sheet_list))
        self.assertEqual(si, sheet_list[0])

        # Fetch the Sheet and make sure it corresponds to what we meant to create.
        sheet = si.loadSheet()
        self.assertIsNotNone(sheet)
        self.assertEqual(sheet.name, self.new_sheet_name)
        self.assertTrue(len(sheet.columns) == len(self.columns))
        self.assertTrue(len(sheet.rows) == 0)
        self.assertEqual(sheet.permalink, si.permalink)

        for sheet_col, src_col in zip(sheet.columns, self.columns):
            self.assertEqual(sheet_col.title, src_col.title)

        # Delete the sheet and make sure it is gone.
        sheet_id = sheet.id
        sheet_permalink = sheet.permalink
        sheet.delete()
        with self.assertRaises(SmartsheetClientError):
            self.client.fetchSheetById(sheet_id)
        sheet_list = self.client.fetchSheetInfoByName(self.new_sheet_name)
        self.assertTrue(len(sheet_list) == 0)
        sheet_info = self.client.fetchSheetInfoByPermalink(sheet_permalink)
        self.assertTrue(sheet_info is None)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1] 
    unittest.main()

