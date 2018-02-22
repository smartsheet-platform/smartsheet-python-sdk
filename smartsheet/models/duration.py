# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
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

from .object_value import *
from ..types import *
from ..util import deserialize


class Duration(ObjectValue):

    """Smartsheet Duration data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Duration model."""
        super(Duration, self).__init__(DURATION, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._days = Number()
        self._elapsed = Boolean()
        self._hours = Number()
        self._milliseconds = Number()
        self._minutes = Number()
        self._negative = Boolean()
        self._seconds = Number()
        self._weeks = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def days(self):
        return self._days.value

    @days.setter
    def days(self, value):
        self._days.value = value

    @property
    def elapsed(self):
        return self._elapsed.value

    @elapsed.setter
    def elapsed(self, value):
        self._elapsed.value = value

    @property
    def hours(self):
        return self._hours.value

    @hours.setter
    def hours(self, value):
        self._hours.value = value

    @property
    def milliseconds(self):
        return self._milliseconds.value

    @milliseconds.setter
    def milliseconds(self, value):
        self._milliseconds.value = value

    @property
    def minutes(self):
        return self._minutes.value

    @minutes.setter
    def minutes(self, value):
        self._minutes.value = value

    @property
    def negative(self):
        return self._negative.value

    @negative.setter
    def negative(self, value):
        self._negative.value = value

    @property
    def seconds(self):
        return self._seconds.value

    @seconds.setter
    def seconds(self, value):
        self._seconds.value = value

    @property
    def weeks(self):
        return self._weeks.value

    @weeks.setter
    def weeks(self, value):
        self._weeks.value = value
