import pytest
import six
from datetime import datetime
import smartsheet


@pytest.mark.usefixtures("smart_setup")
class TestEvents:

    def test_list_events(self, smart_setup):
        smart = smart_setup['smart']

        events_list = smart.Events.list_events(since='2019-03-20T22:33:44Z', max_count=10)
        assert len(events_list.data) <= 10
        for event in events_list.data:
            assert event.object_type.value is not None
            assert event.action.value is not None
            assert event.object_id is not None
            assert event.event_id is not None
            assert isinstance(event.event_timestamp, datetime)
            assert event.user_id is not None
            assert event.request_user_id is not None
            # assert event.access_token_name is not None
            assert event.source.value is not None

        while events_list.more_available:
            events_list = smart.Events.list_events(stream_position=events_list.next_stream_position, max_count=10,
                                                   numeric_dates=True)
            assert len(events_list.data) != 0
            assert len(events_list.data) <= 10
            for event in events_list.data:
                assert event.object_type.value is not None
                assert event.action.value is not None
                assert event.object_id is not None
                assert event.event_id is not None
                assert isinstance(event.event_timestamp, long)
                assert event.user_id is not None
                assert event.request_user_id is not None
                # assert event.access_token_name is not None
                assert event.source.value is not None
