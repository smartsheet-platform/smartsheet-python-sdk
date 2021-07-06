# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2018Smartsheet.com, Inc.
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
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class DatetimeObjectValue(ObjectValue):
    """Smartsheet DateObjectValue data model."""

    def __init__(self, props=None, object_type=None, base_obj=None):
        """Initialize the DateObjectValue model."""
        super(DatetimeObjectValue, self).__init__(object_type, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._value = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, datetime):
            self._value = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._value = value
