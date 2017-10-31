import smartsheet
import os

class MockApiTestHelper:
    def setup_method(self, method):
        os.environ['API_BASE'] = 'http://localhost:8082'
        self.client = smartsheet.Smartsheet(access_token='abc123')
        self.client.errors_as_exceptions()