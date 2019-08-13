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
from .explicit_null import ExplicitNull
from .hyperlink import Hyperlink
from .image import Image
from ..object_value import assign_to_object_value
from ..types import *
from ..util import serialize
from ..util import deserialize


class Cell(object):

    """Smartsheet Cell data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Cell model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column_id = Number()
        self._column_type = String()
        self._conditional_format = String()
        self._display_value = String()
        self._format_ = String()
        self._formula = String()
        self._hyperlink = TypedObject(Hyperlink)
        self._image = TypedObject(Image)
        self._link_in_from_cell = TypedObject(CellLink)
        self._links_out_to_cells = TypedList(CellLink)
        self._object_value = None
        self._override_validation = Boolean()
        self._strict = Boolean()
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
        return self._column_id.value

    @column_id.setter
    def column_id(self, value):
        self._column_id.value = value

    @property
    def column_type(self):
        return self._column_type.value

    @column_type.setter
    def column_type(self, value):
        self._column_type.value = value

    @property
    def conditional_format(self):
        return self._conditional_format.value

    @conditional_format.setter
    def conditional_format(self, value):
        self._conditional_format.value = value

    @property
    def display_value(self):
        return self._display_value.value

    @display_value.setter
    def display_value(self, value):
        self._display_value.value = value

    @property
    def format_(self):
        return self._format_.value

    @format_.setter
    def format_(self, value):
        self._format_.value = value

    @property
    def formula(self):
        return self._formula.value

    @formula.setter
    def formula(self, value):
        self._formula.value = value

    @property
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

    @property
    def image(self):
        return self._image.value

    @image.setter
    def image(self, value):
        self._image.value = value

    @property
    def link_in_from_cell(self):
        return self._link_in_from_cell.value

    @link_in_from_cell.setter
    def link_in_from_cell(self, value):
        self._link_in_from_cell.value = value

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
        self._object_value = assign_to_object_value(value)

    @property
    def override_validation(self):
        return self._override_validation.value

    @override_validation.setter
    def override_validation(self, value):
        self._override_validation.value = value

    @property
    def strict(self):
        return self._strict.value

    @strict.setter
    def strict(self, value):
        self._strict.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (six.string_types, six.integer_types, float, bool, ExplicitNull)):
            self._value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
