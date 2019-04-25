import pytest
import six
from datetime import datetime, timedelta
import smartsheet


@pytest.mark.usefixtures("smart_setup")
class TestEvents:

    def test_list_events(self, smart_setup):
        smart = smart_setup['smart']

        last_hour = datetime.now() - timedelta(hours=1)
        events_list = smart.Events.list_events(since=last_hour.isoformat(), max_count=10)
        assert isinstance(events_list, smart.models.EventResult)
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
                assert isinstance(event.event_timestamp, six.integer_types)
                assert event.user_id is not None
                assert event.request_user_id is not None
                # assert event.access_token_name is not None
                assert event.source.value is not None

    def test_invalid_params(self, smart_setup):
        smart = smart_setup['smart']

        result = smart.Events.list_events(since=0, stream_position='2.1.0An4ZapaQaOXPdojlmediSZ1WqMdi5U_3l9gViOW7ic')
        assert isinstance(result, smart.models.Error)

        result = smart.Events.list_events(since='2019-03-20T22:33:44Z', numeric_dates=True)
        assert isinstance(result, smart.models.Error)
