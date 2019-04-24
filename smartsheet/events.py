# pylint: disable=C0111,R0902,R0913
# Smartsheet Python SDK.
#
# Copyright 2019 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import

import logging
from datetime import datetime
from . import fresh_operation


class Events(object):

    def __init__(self, smartsheet_obj):
        """Init Events with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_events(self, since=None, stream_position=None, max_count=None, numeric_dates=None):
        """Get the list of all Events.

        Args:
            since (str or long): Starting time for events to return.
                You must pass in a value for either since or streamPosition and never both.
            stream_position (str): Indicates next set of events to return.
                Use value of nextStreamPosition returned from the previous call.
                You must pass in a value for either since or streamPosition and never both.
            max_count (int): Maximum number of events to return as response to this call.
                Must be between 1 through 10,000 (inclusive).
            numeric_dates (bool): If true, dates are accepted and returned in Unix epoch time
                (milliseconds since midnight on January 1, 1970 in UTC time).
                Default is false, which means ISO-8601 format

        Returns:
            EventResult containing Event array as data[]
        """
        _op = fresh_operation('list_events')
        _op['method'] = 'GET'
        _op['path'] = '/events'
        if isinstance(since, datetime):
            _op['query_params']['since'] = since  # .isoformat()
        else:
            _op['query_params']['since'] = since
        _op['query_params']['streamPosition'] = stream_position
        _op['query_params']['maxCount'] = max_count
        _op['query_params']['numericDates'] = numeric_dates

        expected = ['EventResult', 'Event']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
