# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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

from ..util import prep
from ..types import TypedList
from .duration import Duration
from datetime import datetime
from dateutil.parser import parse
import logging
import six
import json


class Schedule(object):
    """Smartsheet Schedule data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Schedule model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            'type': [
                'ONCE',
                'DAILY',
                'WEEKLY',
                'MONTHLY',
                'YEARLY'],
            'day_descriptors': [
                'DAY',
                'WEEKDAY',
                'WEEKEND',
                'SUNDAY',
                'MONDAY',
                'TUESDAY',
                'WEDNESDAY',
                'THURSDAY',
                'FRIDAY',
                'SATURDAY'],
            'day_ordinal': [
                'FIRST',
                'SECOND',
                'THIRD',
                'FOURTH',
                'LAST']}

        self._type = None
        self._start_at = None
        self._end_at = None
        self._day_of_month = None
        self._day_ordinal = None
        self._day_descriptors = TypedList(str)
        self._repeat_every = None
        self._last_sent_at = None

        if props:
            # account for alternate variable names from raw API response
            if 'type' in props:
                self.type = props['type']
            if 'startAt' in props:
                self.start_at = props['startAt']
            if 'start_at' in props:
                self.start_at = props['start_at']
            if 'endAt' in props:
                self.end_at = props['endAt']
            if 'end_at' in props:
                self.end_at = props['end_at']
            if 'dayOfMonth' in props:
                self.day_of_month = props['dayOfMonth']
            if 'day_of_month' in props:
                self.day_of_month = props['day_of_month']
            if 'dayOrdinal' in props:
                self.day_ordinal = props['dayOrdinal']
            if 'day_ordinal' in props:
                self.day_ordinal = props['day_ordinal']
            if 'dayDescriptors' in props:
                self.day_descriptors = props['dayDescriptors']
            if 'day_descriptors' in props:
                self.day_descriptors = props['day_descriptors']
            if 'repeatEvery' in props:
                self.repeat_every = props['repeatEvery']
            if 'repeat_every' in props:
                self.repeat_every = props['repeat_every']
            if 'lastSentAt' in props:
                self.last_sent_at = props['lastSentAt']
            if 'last_sent_at' in props:
                self.last_sent_at = props['last_sent_at']
            if 'nextSendAt' in props:
                self.next_send_at = props['nextSendAt']
            if 'next_send_at' in props:
                self.next_send_at = props['next_send_at']
        self.__initialized = True

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Schedule`type`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['type']))
            self._type = value

    @property
    def start_at(self):
        return self._start_at

    @start_at.setter
    def start_at(self, value):
        if isinstance(value, datetime):
            self._start_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._start_at = value

    @property
    def end_at(self):
        return self._end_at

    @end_at.setter
    def end_at(self, value):
        if isinstance(value, datetime):
            self._end_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._end_at = value

    @property
    def day_of_month(self):
        return self._day_of_month

    @day_of_month.setter
    def day_of_month(self, value):
        if isinstance(value, six.integer_types):
            self._day_of_month = value

    @property
    def day_ordinal(self):
        return self._day_ordinal

    @day_ordinal.setter
    def day_ordinal(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['day_ordinal']:
                raise ValueError(
                    ("`{0}` is an invalid value for Schedule`day_ordinal`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['day_ordinal']))
            self._day_ordinal = value

    @property
    def day_descriptors(self):
        return self._day_descriptors

    @day_descriptors.setter
    def day_descriptors(self, value):
        if isinstance(value, list):
            self._day_descriptors.purge()
            self._day_descriptors.extend([
                (str(x)
                 if not isinstance(x, six.string_types) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._day_descriptors.purge()
            self._day_descriptors = value.to_list()
        elif isinstance(value, str):
            self._day_descriptors.purge()
            self._day_descriptors.append(value)

        for string in self._day_descriptors:
            if string not in self.allowed_values['day_descriptors']:
                raise ValueError(
                    ("`{0}` is an invalid value for Schedule`day_descriptors`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['day_descriptors']))

    @property
    def repeat_every(self):
        return self._repeat_every

    @repeat_every.setter
    def repeat_every(self, value):
        if isinstance(value, six.integer_types):
            self._repeat_every = value

    @property
    def last_sent_at(self):
        return self._last_sent_at

    @last_sent_at.setter
    def last_sent_at(self, value):
        if isinstance(value, datetime):
            self._last_sent_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._last_sent_at = value

    @property
    def next_send_at(self):
        return self._next_send_at

    @next_send_at.setter
    def next_send_at(self, value):
        if isinstance(value, datetime):
            self._next_send_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._next_send_at = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'type': prep(self._type),
            'startAt': prep(self._start_at),
            'endAt': prep(self._end_at),
            'dayOfMonth': prep(self._day_of_month),
            'dayDescriptors': prep(self._day_descriptors),
            'dayOrdinal': prep(self._day_ordinal),
            'repeatEvery': prep(self._repeat_every),
            'lastSentAt': prep(self._last_sent_at),
            'nextSendAt': prep(self._next_send_at)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'create_update_request' or \
                        self.pre_request_filter == 'update_update_request':
            permitted = ['type','startAt','endAt','dayOfMonth','dayDescriptors','dayOrdinal','repeatEvery']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj', key)
                    del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())