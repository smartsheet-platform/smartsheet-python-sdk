# pylint: disable=C0103,W0232

import smartsheet
import pytest
from mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockApiSheets(MockApiTestHelper):
    @clean_api_error
    def test_list_automation_rules(self):
        self.client.as_test_scenario('List Automation Rules')
        response = self.client.Sheets.list_automation_rules(324)
        assert isinstance(response.data, list)

    @clean_api_error
    def test_get_automation_rule(self):
        self.client.as_test_scenario('Get Automation Rule')
        response = self.client.Sheets.get_automation_rule(324, 284)
        assert isinstance(response, smartsheet.models.AutomationRule)

    @clean_api_error
    def test_update_automation_rule(self):
        pytest.skip('skipping until API can be updated')
        self.client.as_test_scenario('Update Automation Rule')
        auto_rule = smartsheet.models.AutomationRule()
        auto_rule.action = smartsheet.models.AutomationAction()
        auto_rule.action.type = 'NOTIFICATION_ACTION'
        recipient = smartsheet.models.Recipient()
        recipient.email = 'jane@example.com'
        auto_rule.action.recipients = [recipient]
        auto_rule.action.frequency = 'WEEKLY'
        response = self.client.Sheets.update_automation_rule(324, 284, auto_rule)
        assert response.message == 'SUCCESS'

    @clean_api_error
    def test_delete_automation_rule(self):
        self.client.as_test_scenario('Delete Automation Rule')
        response = self.client.Sheets.delete_automation_rule(324, 284)
        assert response.message == 'SUCCESS'
