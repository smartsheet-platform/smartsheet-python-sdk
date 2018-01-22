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

import six
import json

from .cell import Cell
from .object_value import ObjectValue
from .string_object_value import StringObjectValue
from .boolean_object_value import BooleanObjectValue
from .number_object_value import NumberObjectValue
from ..util import serialize
from ..util import deserialize


class CellDataItem(object):
    """Smartsheet CellDataItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellDataItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._cell = None
        self._column_id = None
        self._label = None
        self._label_format = None
        self._object_value = None
        self._order = None
        self._value_format = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, value):
        if isinstance(value, Cell):
            self._cell = value
        elif isinstance(value, dict):
            self._cell = Cell(value, self._base)

    @property
    def column_id(self):
        return self._column_id

    @column_id.setter
    def column_id(self, value):
        if isinstance(value, six.integer_types):
            self._column_id = value

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
        if isinstance(value, ObjectValue):
            self._object_value = value
        elif isinstance(value, six.string_types):
            self._object_value = StringObjectValue(value)
        elif isinstance(value, (six.integer_types, float)):
            self._object_value = NumberObjectValue(value)
        elif isinstance(value, bool):
            self._object_value = BooleanObjectValue(value)

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if isinstance(value, six.integer_types):
            self._order = value

    @property
    def value_format(self):
        return self._value_format

    @value_format.setter
    def value_format(self, value):
        if isinstance(value, six.string_types):
            self._value_format = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
