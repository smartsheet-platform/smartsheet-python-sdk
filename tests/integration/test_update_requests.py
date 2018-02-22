import pytest
import time
import datetime


@pytest.mark.usefixtures("smart_setup")
class TestUpdateRequests:
    immediate_update_request=None
    future_update_request=None

    def test_create_update_request(self, smart_setup):
        smart = smart_setup['smart']
        request = smart.models.UpdateRequest()
        request.send_to = [{'email': 'someone@smartsheet.com'}]
        request.subject = 'sample update request'
        request.message = 'Hello, please checkout my update request'
        request.cc_me = False
        request.include_discussions = False
        request.include_attachments = False
        request.row_ids = smart_setup['sheet'].rows[0].id
        request.column_ids = smart_setup['sheet'].columns[0].id
        action = smart.Sheets.create_update_request(smart_setup['sheet'].id, request)
        assert action.message == 'SUCCESS'
        TestUpdateRequests.immediate_update_request = action.data

        ts = time.time() + 3600
        dt = datetime.datetime.utcfromtimestamp(ts)
        dt = dt.replace(minute=0, second=0, microsecond=0)
        schedule = smart.models.Schedule()
        schedule.type = 'ONCE'
        schedule.start_at = dt
        request.schedule = schedule
        action = smart.Sheets.create_update_request(smart_setup['sheet'].id, request)
        assert action.message == 'SUCCESS'
        TestUpdateRequests.future_update_request = action.data

    def test_change_update_request(self, smart_setup):
        smart = smart_setup['smart']
        request = smart.models.UpdateRequest()
        request.subject = 'updated update request'
        request.column_ids = smart.models.ExplicitNull()
        request.include_attachments = True
        action = smart.Sheets.update_update_request(smart_setup['sheet'].id,
                                                    TestUpdateRequests.future_update_request.id, request)
        assert action.message == 'SUCCESS'

    def test_get_all_update_requests(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.list_update_requests(smart_setup['sheet'].id)
        assert isinstance(action, smart.models.IndexResult)
        assert action.total_count >= 1

    def test_get_update_request(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.get_update_request(smart_setup['sheet'].id, TestUpdateRequests.future_update_request.id)
        assert isinstance(action, smart.models.UpdateRequest)

    def test_delete_update_request(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.delete_update_request(smart_setup['sheet'].id, TestUpdateRequests.future_update_request.id)
        assert action.message == 'SUCCESS'
