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
from datetime import datetime
from dateutil.parser import parse
import json
import six


class DateObjectValue(ObjectValue):
    """Smartsheet DateObjectValue data model."""

    def __init__(self, props=None, object_type=None, base_obj=None):
        """Initialize the DateObjectValue model."""
        super(DateObjectValue, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._value = None

        if props:
            # account for alternate variable names from raw API response
            if 'value' in props:
                self.value = props['value']
        else:
            self.object_type = object_type

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

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(DateObjectValue, self).to_dict(op_id, method)
        obj = {
            'value': prep(self._value)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())