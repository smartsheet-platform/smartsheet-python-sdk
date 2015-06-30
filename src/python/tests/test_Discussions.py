import sys
import json
import datetime
import unittest
import smartsheetclient
import logging
log_format = '%(module)s.%(funcName)s[%(lineno)d] %(levelname)s - %(message)s'
logging.basicConfig(filename='tests.log', level=logging.DEBUG, format=log_format)

api_token = 'UNSET'

class DiscussionTest(unittest.TestCase):
    logger = None
    client = None
    columns = []
    sheet = None


    def setUp(self):
        self.logger = logging.getLogger()
        self.client = smartsheetclient.SmartsheetClient(api_token,
                logger=self.logger)

        time_str = str(datetime.datetime.utcnow())
        self.new_sheet_name = 'TestDiscussion -%s' % time_str

        col_1 = smartsheetclient.Column("Col 1 - TextNumber",
                type=smartsheetclient.CellTypes.TextNumber,
                primary=True)
        col_2 = smartsheetclient.Column("Col 2 - Date",
                type=smartsheetclient.CellTypes.Date)
        col_3 = smartsheetclient.Column("Col 3 - Picklist",
                type=smartsheetclient.CellTypes.Picklist,
                options=['Yes',
                'No',
                'Maybe'])
        col_4 = smartsheetclient.Column("Col 4 - Checkbox",
                type=smartsheetclient.CellTypes.Checkbox)
        col_5 = smartsheetclient.Column("Col 5 - ContactList",
                type=smartsheetclient.CellTypes.ContactList)
        col_6 = smartsheetclient.Column("Col 6 - TextNumber",
                type=smartsheetclient.CellTypes.TextNumber)
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

    def test_DiscussionCreation(self):
        DISCUSSION_NAME = 'XSXSXSXSXSXSXSXS'
        COMMENT_TEXT = 'asdfghjkllweroiuwere'
        d = self.sheet.addDiscussion(DISCUSSION_NAME, COMMENT_TEXT)

        path = 'sheet/{0}/discussions'.format(self.sheet.id)
        result = self.client.GET(path)
        for i in result:
            if i['id'] == d.id:
                break
        else:
            self.assertTrue(False)

    def test_CommentCreation(self):
        DISCUSSION_NAME = 'SISISISISISISISSISISI'
        COMMENT_1_TEXT = ';lkj;lkj;lkj;lkj;lkj'
        COMMENT_2_TEXT = 'poiupoiupoiupoiupoiu'
        d = self.sheet.addDiscussion(DISCUSSION_NAME, COMMENT_1_TEXT)
        d.addComment(COMMENT_2_TEXT)

        path = 'sheet/{0}/discussion/{1}'.format(self.sheet.id, d.id)
        result = self.client.GET(path)
        for i in result['comments']:
            if i['text'] == COMMENT_2_TEXT:
                break
        else:
            self.assertTrue(False)

    def test_DiscussionDeletion(self):
        DISCUSSION_NAME = 'DEWERWETRQERGERTERTER$'
        COMMENT_TEXT = 'CASCEARG%ERRERSCVFEWRE'
        d = self.sheet.addDiscussion(DISCUSSION_NAME, COMMENT_TEXT)
        expired_id = d.id
        self.sheet.removeDiscussion(d)
        # d.delete()

        path = 'sheet/{0}/discussions'.format(self.sheet.id)
        result = self.client.GET(path)
        for i in result:
            self.assertTrue(i['id'] != expired_id)

    def test_CommentDeletion(self):
        DISCUSSION_NAME = 'POISHJEOIFNROUWIOERE'
        COMMENT_1_TEXT = 'My Initial Comment'
        COMMENT_2_TEXT = 'My Comment to be Deleted'
        d = self.sheet.addDiscussion(DISCUSSION_NAME, COMMENT_1_TEXT)
        d.addComment(COMMENT_2_TEXT)

        self.assertTrue(d.comments[0].text == COMMENT_1_TEXT)
        self.sheet.discussions[0].removeComment(d.comments[0])
        # d.comments[0].delete()

        path = 'sheet/{0}/discussion/{1}'.format(self.sheet.id, d.id)
        result = self.client.GET(path)
        for i in result['comments']:
            self.assertTrue(i['text'] == COMMENT_2_TEXT)

    def test_FetchDiscussions(self):
        DISCUSSION_COUNT = 10
        COMMENT_TEXT = 'now is the time for all good men to come to the aid of their country'
        for i in range(DISCUSSION_COUNT):
            path = 'sheet/{0}/discussions'.format(self.sheet.id)
            body = {
                'title': 'FetchDiscussion_{0}'.format(i),
                'comment': {'text': COMMENT_TEXT},
            }
            self.client.POST(path, body=json.dumps(body))

        self.sheet.fetchAllDiscussions()
        # print self.sheet.discussions
        # This isn't guaranteed to be true, consider walking thru the list
        # and counting them
        self.assertTrue(len(self.sheet.discussions) == DISCUSSION_COUNT)

    def test_FetchComments(self):
        DISCUSSION_NAME = 'Fetch Comments'
        COMMENT_1_TEXT = 'x'
        COMMENT_TEXT = 'Comment to be counted'
        COMMENT_COUNT = 10
        d = self.sheet.addDiscussion(DISCUSSION_NAME, COMMENT_1_TEXT)
        self.assertTrue(d is not None)

        for i in range(COMMENT_COUNT):
            path = 'sheet/{0}/discussion/{1}/comments'.format(self.sheet.id, d.id)
            body = {
                'text': COMMENT_TEXT,
            }
            self.client.POST(path, body=json.dumps(body))
        d.refreshComments()
        self.assertTrue(len(d.comments) == COMMENT_COUNT + 1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Error, must supply path to token file")
    api_token_file = sys.argv[1]

    with file(api_token_file, 'r') as fh:
        api_token = fh.read()
        api_token = api_token.strip()
    del sys.argv[1]
    unittest.main()
