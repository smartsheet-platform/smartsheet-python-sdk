# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
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

from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class Criteria(object):

    """Smartsheet Criteria data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Criteria model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'operator': [
                'EQUAL',
                'NOT_EQUAL',
                'GREATER_THAN',
                'LESS_THAN',
                'CONTAINS',
                'BETWEEN',
                'TODAY',
                'PAST',
                'FUTURE',
                'LAST_N_DAYS',
                'NEXT_N_DAYS',
                'IS_BLANK',
                'IS_NOT_BLANK',
                'IS_NUMBER',
                'IS_NOT_NUMBER',
                'IS_DATE',
                'IS_NOT_DATE',
                'IS_CHECKED',
                'IS_NOT_CHECKED']}

        self._operator = None
        self._value1 = None
        self._value2 = None

        if props:
            if 'operator' in props:
                self.operator = props['operator']
            if 'value1' in props:
                self.value1 = props['value1']
            if 'value2' in props:
                self.value2 = props['value2']

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['operator']:
                raise ValueError(
                    ("`{0}` is an invalid value for Criteria`operator`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['operator']))
            self._operator = value

    @property
    def value1(self):
        return self._value1

    @value1.setter
    def value1(self, value):
        if isinstance(value, six.string_types):
            self._value1 = value

    @property
    def value2(self):
        return self._value2

    @value2.setter
    def value2(self, value):
        if isinstance(value, six.string_types):
            self._value2 = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'operator': prep(self._operator),
            'value1': prep(self._value1),
            'value2': prep(self._value2)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
