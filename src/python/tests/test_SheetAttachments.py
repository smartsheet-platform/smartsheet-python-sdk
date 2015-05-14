import smartsheetclient
import argparse
import unittest
import datetime
import logging
import sys

log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG,
                    format=log_format)

api_token = 'UNSET'


class SheetAttachmentsTest(unittest.TestCase):
    def setUp(self):
        global api_token
        self.logger = logging.getLogger()
        self.client = smartsheetclient.SmartsheetClient(api_token,
                                                        logger=self.logger)
    def test_nop(self):
        self.assertTrue(True)

    def test_hyperlink_attachment(self):
        pass

    def test_file_attachment(self):
        pass

def main():
    if len(sys.argv) < 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1]
    unittest.main()


if __name__ == "__main__":
    main()
