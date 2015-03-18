import sys
import unittest
from smartsheetclient import SmartsheetClient, SheetInfo
import logging
log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG, format=log_format)


api_token = 'UNSET'


class SheetListTest(unittest.TestCase):

    permalink_start = 'https://app.smartsheet.com/b/home?lx='

    def setUp(self):
        self.logger = logging.getLogger()
        self.client = SmartsheetClient(api_token, logger=self.logger)

    def test_sheet_list(self):
        sheet_list = self.client.fetchSheetList()
        self.assertIsInstance(sheet_list, list)
        self.logger.debug("SheetList: %s", sheet_list)

        sheet_list_2 = self.client.fetchSheetList(use_cache=True)
        self.logger.debug("SheetList from cache: %s", sheet_list)
        self.assertListEqual(sheet_list, sheet_list_2,
                msg='fetchSheetList(use_cache=True) did not get the same list')

        for si in sheet_list:
            self.assertIsInstance(si, SheetInfo)
            self.assertIsInstance(si.name, basestring)
            self.assertEqual(si.client, self.client)
            self.assertTrue(si.accessLevel in 'OWNER VIEWER EDITOR EDITOR_SHARE ADMIN'.split())
            self.assertTrue(type(si.id) == int or type(si.id) == long)
            self.assertTrue(si.permalink.startswith(self.permalink_start))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1] 
    unittest.main()

