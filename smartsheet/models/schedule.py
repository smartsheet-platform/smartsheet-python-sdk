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

from .enums import DayOrdinal, DayDescriptors, ScheduleType
from ..types import *
from ..util import serialize
from ..util import deserialize


class Schedule(object):
    """Smartsheet Schedule data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Schedule model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._day_descriptors = EnumeratedList(DayDescriptors)
        self._day_of_month = Number()
        self._day_ordinal = EnumeratedValue(DayOrdinal)
        self._end_at = Timestamp()
        self._last_sent_at = Timestamp()
        self._next_send_at = Timestamp()
        self._repeat_every = Number()
        self._start_at = Timestamp()
        self._type_ = EnumeratedValue(ScheduleType)

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

    @property
    def day_of_month(self):
        return self._day_of_month.value

    @day_of_month.setter
    def day_of_month(self, value):
        self._day_of_month.value = value

    @property
    def day_ordinal(self):
        return self._day_ordinal

    @day_ordinal.setter
    def day_ordinal(self, value):
        self._day_ordinal.set(value)

    @property
    def end_at(self):
        return self._end_at.value

    @end_at.setter
    def end_at(self, value):
        self._end_at.value = value

    @property
    def last_sent_at(self):
        return self._last_sent_at.value

    @last_sent_at.setter
    def last_sent_at(self, value):
        self._last_sent_at.value = value

    @property
    def next_send_at(self):
        return self._next_send_at.value

    @next_send_at.setter
    def next_send_at(self, value):
        self._next_send_at.value = value

    @property
    def repeat_every(self):
        return self._repeat_every.value

    @repeat_every.setter
    def repeat_every(self, value):
        self._repeat_every.value = value

    @property
    def start_at(self):
        return self._start_at.value

    @start_at.setter
    def start_at(self, value):
        self._start_at.value = value

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        self._type_.set(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
