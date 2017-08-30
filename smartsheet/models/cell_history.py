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

from .cell import Cell
from .cell_link import CellLink
from .hyperlink import Hyperlink
from .user import User
from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import six

class CellHistory(Cell):

    """Smartsheet CellHistory data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellHistory model."""
        super(CellHistory, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._link_in_from_cell = None
        self._modified_at = None
        self._column_type = None
        self._modified_by = None
        self._hyperlink = None
        self._conditional_format = None
        self._value = None
        self._column_id = None
        self.__format = None
        self._strict = True
        self._display_value = None
        self._links_out_to_cells = TypedList(CellLink)
        self._formula = None

        if props:
            # account for alternate variable names from raw API response
            if 'linkInFromCell' in props:
                self.link_in_from_cell = props['linkInFromCell']
            if 'link_in_from_cell' in props:
                self.link_in_from_cell = props[
                    'link_in_from_cell']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']
            # read only
            if 'columnType' in props:
                self.column_type = props['columnType']
            if 'modifiedBy' in props:
                self.modified_by = props['modifiedBy']
            if 'modified_by' in props:
                self.modified_by = props['modified_by']
            if 'hyperlink' in props:
                self.hyperlink = props['hyperlink']
            # read only
            if 'conditionalFormat' in props:
                self.conditional_format = props[
                    'conditionalFormat']
            if 'value' in props:
                self.value = props['value']
            if 'columnId' in props:
                self.column_id = props['columnId']
            if 'column_id' in props:
                self.column_id = props['column_id']
            if 'format' in props:
                self._format = props['format']
            if '_format' in props:
                self._format = props['_format']
            if 'strict' in props:
                self.strict = props['strict']
            # read only
            if 'displayValue' in props:
                self.display_value = props['displayValue']
            if 'linksOutToCells' in props:
                self.links_out_to_cells = props[
                    'linksOutToCells']
            if 'links_out_to_cells' in props:
                self.links_out_to_cells = props[
                    'links_out_to_cells']
            if 'formula' in props:
                self.formula = props['formula']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self._format
        else:
            raise AttributeError(key)

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
    def column_type(self):
        return self._column_type

    @column_type.setter
    def column_type(self, value):
        if isinstance(value, six.string_types):
            self._column_type = value

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
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, value):
        if isinstance(value, Hyperlink):
            self._hyperlink = value
        else:
            self._hyperlink = Hyperlink(value, self._base)

    @property
    def conditional_format(self):
        return self._conditional_format

    @conditional_format.setter
    def conditional_format(self, value):
        if isinstance(value, six.string_types):
            self._conditional_format = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, six.string_types):
            self._value = value

    @property
    def column_id(self):
        return self._column_id

    @column_id.setter
    def column_id(self, value):
        if isinstance(value, six.integer_types):
            self._column_id = value

    @property
    def _format(self):
        return self.__format

    @_format.setter
    def _format(self, value):
        if isinstance(value, six.string_types):
            self.__format = value

    @property
    def strict(self):
        return self._strict

    @strict.setter
    def strict(self, value):
        if isinstance(value, bool):
            self._strict = value

    @property
    def display_value(self):
        return self._display_value

    @display_value.setter
    def display_value(self, value):
        if isinstance(value, six.string_types):
            self._display_value = value

    @property
    def links_out_to_cells(self):
        return self._links_out_to_cells

    @links_out_to_cells.setter
    def links_out_to_cells(self, value):
        if isinstance(value, list):
            self._links_out_to_cells.purge()
            self._links_out_to_cells.extend([
                 (CellLink(x, self._base)
                  if not isinstance(x, CellLink) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._links_out_to_cells.purge()
            self._links_out_to_cells = value.to_list()
        elif isinstance(value, CellLink):
            self._links_out_to_cells.purge()
            self._links_out_to_cells.append(value)

    @property
    def formula(self):
        return self._formula

    @formula.setter
    def formula(self, value):
        if isinstance(value, six.string_types):
            self._formula = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(CellHistory, self).to_dict(op_id, method)
        obj = {
            'linkInFromCell': prep(self._link_in_from_cell),
            'modifiedAt': prep(self._modified_at),
            'columnType': prep(self._column_type),
            'modifiedBy': prep(self._modified_by),
            'hyperlink': prep(self._hyperlink),
            'conditionalFormat': prep(self._conditional_format),
            'value': prep(self._value),
            'columnId': prep(self._column_id),
            'format': prep(self.__format),
            'strict': prep(self._strict),
            'displayValue': prep(self._display_value),
            'linksOutToCells': prep(self._links_out_to_cells),
            'formula': prep(self._formula)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
