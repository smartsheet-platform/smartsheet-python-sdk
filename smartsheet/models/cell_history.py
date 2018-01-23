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
from .cell_link import CellLink
from .hyperlink import Hyperlink
from .user import User
from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class CellHistory(Cell):

    """Smartsheet CellHistory data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellHistory model."""
        super(CellHistory, self).__init__(props, base_obj)
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
        self._link_in_from_cell = None
        self._links_out_to_cells = TypedList(CellLink)
        self._modified_at = None
        self._modified_by = None
        self._strict = True
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
            super(CellHistory, self).__setattr__(key, value)

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
        if isinstance(value, Hyperlink):
            self._hyperlink = value
        else:
            self._hyperlink = Hyperlink(value, self._base)

    @property
    def link_in_from_cell(self):
        return self._link_in_from_cell

    @link_in_from_cell.setter
    def link_in_from_cell(self, value):
        if isinstance(value, CellLink):
            self._link_in_from_cell = value
        else:
            self._link_in_from_cell = CellLink(value, self._base)

    @property
    def links_out_to_cells(self):
        return self._links_out_to_cells

    @links_out_to_cells.setter
    def links_out_to_cells(self, value):
        self._links_out_to_cells.load(value)

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        if isinstance(value, datetime):
            self._modified_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._modified_at = value

    @property
    def modified_by(self):
        return self._modified_by

    @modified_by.setter
    def modified_by(self, value):
        if isinstance(value, User):
            self._modified_by = value
        else:
            self._modified_by = User(value, self._base)

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
        if isinstance(value, (six.string_types, six.integer_types, float, bool)):
            self._value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
