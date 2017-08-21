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
from .duration import Duration
import logging
import six
import json


class Predecessor(object):
    """Smartsheet Predecessor data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Predecessor model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            'type': [
                'FS',
                'FF',
                'SS',
                'SS']}

        self._row_id = None
        self._row_number = None
        self._type = None
        self._lag = None
        self._invalid = None
        self._in_critical_path = None

        if props:
            # account for alternate variable names from raw API response
            if 'rowId' in props:
                self.row_id = props['rowId']
            if 'row_id' in props:
                self.row_id = props['row_id']
            if 'rowNumber' in props:
                self.row_number = props['rowNumber']
            if 'row_number' in props:
                self.row_number = props['row_number']
            if 'type' in props:
                self.type = props['type']
            if 'lag' in props:
                self.lag = props['lag']
            if 'invalid' in props:
                self.invalid = props['invalid']
            if 'inCriticalPath' in props:
                self.in_critical_path = props['inCriticalPath']
            if 'in_critical_path' in props:
                self.in_critical_path = props['in_critical_path']
        self.__initialized = True

    @property
    def row_id(self):
        return self._row_id

    @row_id.setter
    def row_id(self, value):
        if isinstance(value, six.integer_types):
            self._row_id = value

    @property
    def row_number(self):
        return self._row_number

    @row_number.setter
    def row_number(self, value):
        if isinstance(value, six.integer_types):
            self._row_number = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, six.string_types):
            self._type = value

    @property
    def lag(self):
        return self._lag

    @lag.setter
    def lag(self, value):
        if isinstance(value, Duration):
            self._lag = value

    @property
    def invalid(self):
        return self._invalid

    @invalid.setter
    def invalid(self, value):
        if isinstance(value, bool):
            self._invalid = value

    @property
    def in_critical_path(self):
        return self._in_critical_path

    @in_critical_path.setter
    def in_critical_path(self, value):
        if isinstance(value, bool):
            self._in_critical_path = value
    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'rowId': prep(self._row_id),
            'rowNumber': prep(self._row_number),
            'type': prep(self._type),
            'lag': prep(self._lag),
            'invalid': prep(self._invalid),
            'inCriticalPath': prep(self._in_critical_path)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_rows':
            permitted = ['rowId', 'type', 'lag']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_rows':
            permitted = ['rowId', 'type', 'lag']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())