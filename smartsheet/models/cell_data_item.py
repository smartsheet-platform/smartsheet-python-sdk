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
from .cell import Cell
import logging
import six
import json

class CellDataItem(object):
    """Smartsheet CellDataItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellDataItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._label = None
        self._label_format = None
        self._object_value = None
        self._cell = None
        self._value_format = None
        self._order = None
        self._column_id = None

        if props:
            # account for alternate variable names from raw API response
            if 'label' in props:
                self.label = props['label']
            if 'labelFormat' in props:
                self.label_format = props['labelFormat']
            if 'label_format' in props:
                self.label_format = props['label_format']
            if 'objectValue' in props:
                self.object_value = props['objectValue']
            if 'object_value' in props:
                self.object_value = props['object_value']
            if 'cell' in props:
                self.cell = props['cell']
            if 'valueFormat' in props:
                self.value_format = props['valueFormat']
            if 'value_format' in props:
                self.value_format = props['value_format']
            if 'order' in props:
                self.order = props['order']
            if 'columnId' in props:
                self.column_id = props['columnId']
            if 'column_id' in props:
                self.column_id = props['column_id']
        self.__initialized = True

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if isinstance(value, six.string_types):
            self._label = value

    @property
    def label_format(self):
        return self._label_format

    @label_format.setter
    def label_format(self, value):
        if isinstance(value, six.string_types):
            self._label_format = value

    @property
    def object_value(self):
        return self._object_value

    @object_value.setter
    def object_value(self, value):
        self._object_value = value

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, value):
        if isinstance(value, Cell):
            self._cell = value

    @property
    def value_format(self):
        return self._value_format

    @value_format.setter
    def value_format(self, value):
        if isinstance(value, six.string_types):
            self._value_format = value

    @property
    def column_id(self):
        return self._column_id

    @column_id.setter
    def column_id(self, value):
        if isinstance(value, six.integer_types):
            self._column_id = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'label': prep(self._label),
            'labelFormat': prep(self._label_format),
            'objectValue': prep(self._object_value),
            'cell': prep(self._cell),
            'valueFormat': prep(self._value_format),
            'order': prep(self._order),
            'columnId': prep(self._column_id)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())