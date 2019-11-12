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

from .cell import Cell
from .object_value import ObjectValue
from .string_object_value import StringObjectValue
from .boolean_object_value import BooleanObjectValue
from .number_object_value import NumberObjectValue
from .summary_field import SummaryField
from ..object_value import assign_to_object_value
from ..types import *
from ..util import serialize
from ..util import deserialize


class CellDataItem(object):
    """Smartsheet CellDataItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellDataItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._cell = TypedObject(Cell)
        self._column_id = Number()
        self._data_source = String()
        self._label = String()
        self._label_format = String()
        self._object_value = None
        self._order = Number()
        self._profile_field = TypedObject(SummaryField)
        self._row_id = Number()
        self._sheet_id = Number()
        self._value_format = String()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def cell(self):
        return self._cell.value

    @cell.setter
    def cell(self, value):
        self._cell.value = value

    @property
    def column_id(self):
        return self._column_id.value

    @column_id.setter
    def column_id(self, value):
        self._column_id.value = value

    @property
    def data_source(self):
        return self._data_source.value

    @data_source.setter
    def data_source(self, value):
        self._data_source.value = value

    @property
    def label(self):
        return self._label.value

    @label.setter
    def label(self, value):
        self._label.value = value

    @property
    def label_format(self):
        return self._label_format.value

    @label_format.setter
    def label_format(self, value):
        self._label_format.value = value

    @property
    def object_value(self):
        return self._object_value

    @object_value.setter
    def object_value(self, value):
        self._object_value = assign_to_object_value(value)

    @property
    def order(self):
        return self._order.value

    @order.setter
    def order(self, value):
        self._order.value = value

    @property
    def profile_field(self):
        return self._profile_field.value

    @profile_field.setter
    def profile_field(self, value):
        self._profile_field.value = value

    @property
    def row_id(self):
        return self._row_id.value

    @row_id.setter
    def row_id(self, value):
        self._row_id.value = value

    @property
    def sheet_id(self):
        return self._sheet_id.value

    @sheet_id.setter
    def sheet_id(self, value):
        self._sheet_id.value = value

    @property
    def value_format(self):
        return self._value_format.value

    @value_format.setter
    def value_format(self, value):
        self._value_format.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
