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
from datetime import date
from dateutil.parser import parse
import six
import json


class ProjectSettings(object):
    """Smartsheet ProjectSettings data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ProjectSettings model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._working_days = TypedList(six.string_types)
        self._non_working_days = TypedList(date)
        self._length_of_day = None

        if props:
            # account for alternate variable names from raw API response
            if 'workingDays' in props:
                self.working_days = props['workingDays']
            if 'working_days' in props:
                self.working_days = props['working_days']
            if 'nonWorkingDays' in props:
                self.non_working_days = props['nonWorkingDays']
            if 'non_working_days' in props:
                self.non_working_days = props['non_working_days']
            if 'lengthOfDay' in props:
                self.length_of_day = props['lengthOfDay']
            if 'length_of_day' in props:
                self.length_of_day = props['length_of_day']
        self.__initialized = True

    @property
    def working_days(self):
        return self._working_days

    @working_days.setter
    def working_days(self, value):
        if isinstance(value, list):
            self._working_days.purge()
            self._working_days.extend([
                 (six.string_types(x, self._base)
                  if not isinstance(x, six.string_types) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._working_days.purge()
            self._working_days = value.to_list()
        elif isinstance(value, six.string_types):
            self._working_days.purge()
            self._working_days.append(value)

    @property
    def non_working_days(self):
        return self._non_working_days

    @non_working_days.setter
    def non_working_days(self, value):
        if isinstance(value, list):
            self._non_working_days.purge()
            for x in value:
                if isinstance(x, six.string_types):
                    x = parse(x).date()
                if isinstance(x, date):
                    self._non_working_days.extend([x])
        elif isinstance(value, TypedList):
            self._non_working_days.purge()
            self._non_working_days = value.to_list()
        elif isinstance(value, date):
            self._non_working_days.purge()
            self._non_working_days.append(value)
        elif isinstance(value, six.string_types):
            value = parse(value).date()
            self._non_working_days.purge()
            self._non_working_days.append(value)

    @property
    def length_of_day(self):
        return self._length_of_day

    @length_of_day.setter
    def length_of_day(self, value):
        if isinstance(value, (six.integer_types, float)):
            self._length_of_day = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'workingDays': prep(self._working_days),
            'nonWorkingDays': prep(self._non_working_days),
            'lengthOfDay': prep(self._length_of_day)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())