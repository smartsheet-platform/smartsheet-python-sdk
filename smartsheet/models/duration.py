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
from .object_value import *
import six
import json


class Duration(ObjectValue):

    """Smartsheet Duration data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Duration model."""
        super(Duration, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._negative = None
        self._elapsed = None
        self._weeks = None
        self._days = None
        self._hours = None
        self._minutes = None
        self._seconds = None
        self._milliseconds = None

        if props:
            if 'negative' in props:
                self.negative = props['negative']
            if 'elapsed' in props:
                self.elapsed = props['elapsed']
            if 'weeks' in props:
                self.weeks = props['weeks']
            if 'days' in props:
                self.days = props['days']
            if 'hours' in props:
                self.hours = props['hours']
            if 'minutes' in props:
                self.minutes = props['minutes']
            if 'seconds' in props:
                self.seconds = props['seconds']
            if 'milliseconds' in props:
                self.milliseconds = props['milliseconds']
        else:
            self.object_type = DURATION

        self.__initialized = True

    @property
    def negative(self):
        return self._negative

    @negative.setter
    def negative(self, value):
        if isinstance(value, bool):
            self._negative = value

    @property
    def elapsed(self):
        return self._elapsed

    @elapsed.setter
    def elapsed(self, value):
        if isinstance(value, bool):
            self._elapsed = value

    @property
    def weeks(self):
        return self._weeks

    @weeks.setter
    def weeks(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._weeks = value

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._days = value

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._hours = value

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._minutes = value

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._seconds = value

    @property
    def milliseconds(self):
        return self._milliseconds

    @milliseconds.setter
    def milliseconds(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._milliseconds = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(Duration, self).to_dict(op_id, method)
        obj = {
            'negative': prep(self._negative),
            'elapsed': prep(self._elapsed),
            'weeks': prep(self._weeks),
            'days': prep(self._days),
            'hours': prep(self._hours),
            'minutes': prep(self._minutes),
            'seconds': prep(self._seconds),
            'milliseconds': prep(self._milliseconds)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())