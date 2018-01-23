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

import six
import json

from ..util import serialize
from ..util import deserialize
from ..types import TypedList
from datetime import datetime
from dateutil.parser import parse


class Schedule(object):
    """Smartsheet Schedule data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Schedule model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

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

        self._day_descriptors = TypedList(str)
        self._day_of_month = None
        self._day_ordinal = None
        self._end_at = None
        self._last_sent_at = None
        self._next_send_at = None
        self._repeat_every = None
        self._start_at = None
        self._type_ = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'type':
            return self.type_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'type':
            self.type_ = value
        else:
            super(Schedule, self).__setattr__(key, value)

    @property
    def day_descriptors(self):
        return self._day_descriptors

    @day_descriptors.setter
    def day_descriptors(self, value):
        self._day_descriptors.load(value)
        for string in self._day_descriptors:
            if string not in self.allowed_values['day_descriptors']:
                raise ValueError(
                    ("`{0}` is an invalid value for Schedule`day_descriptors`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['day_descriptors']))

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
    def repeat_every(self):
        return self._repeat_every

    @repeat_every.setter
    def repeat_every(self, value):
        if isinstance(value, six.integer_types):
            self._repeat_every = value

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
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Schedule`type`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['type']))
            self._type_ = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
