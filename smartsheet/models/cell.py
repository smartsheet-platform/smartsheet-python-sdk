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

from .cell_link import CellLink
from .hyperlink import Hyperlink
from .image import Image
from .object_value import *
from .duration import Duration
from .predecessor_list import PredecessorList
from .contact_object_value import ContactObjectValue
from .date_object_value import DateObjectValue
from .string_object_value import StringObjectValue
from .number_object_value import NumberObjectValue
from .boolean_object_value import BooleanObjectValue
from ..types import TypedList
from ..types import ExplicitNull
from ..util import serialize
from ..util import deserialize


class Cell(object):

    """Smartsheet Cell data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Cell model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column_id = None
        self._column_type = None
        self._conditional_format = None
        self._display_value = None
        self._format_ = None
        self._formula = None
        self._hyperlink = None
        self._image = None
        self._link_in_from_cell = None
        self._links_out_to_cells = TypedList(CellLink)
        self._object_value = None
        self._override_validation = None
        self._strict = None
        self._value = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self.format_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'format':
            self.format_ = value
        else:
            super(Cell, self).__setattr__(key, value)

    @property
    def column_id(self):
        return self._column_id

    @column_id.setter
    def column_id(self, value):
        if isinstance(value, six.integer_types):
            self._column_id = value

    @property
    def column_type(self):
        return self._column_type

    @column_type.setter
    def column_type(self, value):
        if isinstance(value, six.string_types):
            self._column_type = value

    @property
    def conditional_format(self):
        return self._conditional_format

    @conditional_format.setter
    def conditional_format(self, value):
        if isinstance(value, six.string_types):
            self._conditional_format = value

    @property
    def display_value(self):
        return self._display_value

    @display_value.setter
    def display_value(self, value):
        if isinstance(value, six.string_types):
            self._display_value = value

    @property
    def format_(self):
        return self._format_

    @format_.setter
    def format_(self, value):
        if isinstance(value, six.string_types):
            self._format_ = value

    @property
    def formula(self):
        return self._formula

    @formula.setter
    def formula(self, value):
        if isinstance(value, six.string_types):
            self._formula = value

    @property
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, value):
        if isinstance(value, (Hyperlink, ExplicitNull)):
            self._hyperlink = value
        else:
            self._hyperlink = Hyperlink(value, self._base)

    def set_hyperlink_null(self):
        self.hyperlink = ExplicitNull()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if isinstance(value, Image):
            self._image = value
        else:
            self._image = Image(value, self._base)

    @property
    def link_in_from_cell(self):
        return self._link_in_from_cell

    @link_in_from_cell.setter
    def link_in_from_cell(self, value):
        if isinstance(value, (CellLink, ExplicitNull)):
            self._link_in_from_cell = value
        else:
            self._link_in_from_cell = CellLink(value, self._base)

    def set_link_in_from_cell_null(self):
        self.link_in_from_cell = ExplicitNull()

    @property
    def links_out_to_cells(self):
        return self._links_out_to_cells

    @links_out_to_cells.setter
    def links_out_to_cells(self, value):
        self._links_out_to_cells.load(value)

    @property
    def object_value(self):
        return self._object_value

    @object_value.setter
    def object_value(self, value):
        if isinstance(value, ObjectValue):
            self._object_value = value
        elif isinstance(value, dict):
            object_type = value['objectType']
            if object_type in OBJECT_VALUE['object_type']:
                enum_object_type = enum_object_value_type(object_type)
                if enum_object_type == DURATION:
                    self._object_value = Duration(value, self._base)
                elif enum_object_type == PREDECESSOR_LIST:
                    self._object_value = PredecessorList(value, self._base)
                elif enum_object_type == CONTACT:
                    self._object_value = ContactObjectValue(value, self._base)
                elif enum_object_type == DATE or enum_object_type == DATETIME or \
                        enum_object_type == ABSTRACT_DATETIME:
                    self._object_value = DateObjectValue(value, enum_object_value_type, self._base)
                else:
                    self._object_value = None
            else:
                raise ValueError(
                    ("`{0}` is an invalid value for ObjectValue`object_type`,"
                     " must be one of {1}").format(
                        object_type, OBJECT_VALUE['object_type']))
        elif isinstance(value, six.string_types):
            self._object_value = StringObjectValue(value)
        elif isinstance(value, (six.integer_types, float)):
            self._object_value = NumberObjectValue(value)
        elif isinstance(value, bool):
            self._object_value = BooleanObjectValue(value)

    @property
    def override_validation(self):
        return self._override_validation

    @override_validation.setter
    def override_validation(self, value):
        if isinstance(value, bool):
            self._override_validation = value

    @property
    def strict(self):
        return self._strict

    @strict.setter
    def strict(self, value):
        if isinstance(value, bool):
            self._strict = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (six.string_types, six.integer_types, float, bool, ExplicitNull)):
            self._value = value

    def set_value_null(self):
        self.value = ExplicitNull()

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
