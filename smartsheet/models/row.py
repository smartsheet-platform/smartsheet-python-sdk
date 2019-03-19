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

from .attachment import Attachment
from .cell import Cell
from .column import Column
from .discussion import Discussion
from .enums import AccessLevel
from ..types import *
from .user import User
from ..util import serialize
from ..util import deserialize
from datetime import datetime


class Row(object):

    """Smartsheet Row data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Row model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._above = Boolean()
        self._access_level = EnumeratedValue(AccessLevel)
        self._attachments = TypedList(Attachment)
        self._cells = TypedList(Cell)
        self._columns = TypedList(Column)
        self._conditional_format = String()
        self._created_at = Timestamp()
        self._created_by = TypedObject(User)
        self._discussions = TypedList(Discussion)
        self._expanded = Boolean()
        self._filtered_out = Boolean()
        self._format_ = String()
        self._id_ = Number()
        self._in_critical_path = Boolean()
        self._indent = Number()
        self._locked = Boolean()
        self._locked_for_user = Boolean()
        self._modified_at = Timestamp()
        self._modified_by = TypedObject(User)
        self._outdent = Number()
        self._parent_id = Number()
        self._permalink = String()
        self._row_number = Number()
        self._sheet_id = Number()
        self._sibling_id = Number()
        self._to_bottom = Boolean()
        self._to_top = Boolean()
        self._version = Number()

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self.format_
        elif key == 'id':
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'format':
            self.format_ = value
        elif key == 'id':
            self.id_ = value
        else:
            super(Row, self).__setattr__(key, value)

    @property
    def above(self):
        return self._above.value

    @above.setter
    def above(self, value):
        self._above.value = value

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level.set(value)

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments.load(value)

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells.load(value)

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns.load(value)

    @property
    def conditional_format(self):
        return self._conditional_format.value

    @conditional_format.setter
    def conditional_format(self, value):
        self._conditional_format.value = value

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def created_by(self):
        return self._created_by.value

    @created_by.setter
    def created_by(self, value):
        self._created_by.value = value

    @property
    def discussions(self):
        return self._discussions

    @discussions.setter
    def discussions(self, value):
        self._discussions.load(value)

    @property
    def expanded(self):
        return self._expanded.value

    @expanded.setter
    def expanded(self, value):
        self._expanded.value = value

    @property
    def filtered_out(self):
        return self._filtered_out.value

    @filtered_out.setter
    def filtered_out(self, value):
        self._filtered_out.value = value

    @property
    def format_(self):
        return self._format_.value

    @format_.setter
    def format_(self, value):
        self._format_.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def in_critical_path(self):
        return self._in_critical_path.value

    @in_critical_path.setter
    def in_critical_path(self, value):
        self._in_critical_path.value = value

    @property
    def indent(self):
        return self._indent.value

    @indent.setter
    def indent(self, value):
        self._indent.value = value

    @property
    def locked(self):
        return self._locked.value

    @locked.setter
    def locked(self, value):
        self._locked.value = value

    @property
    def locked_for_user(self):
        return self._locked_for_user.value

    @locked_for_user.setter
    def locked_for_user(self, value):
        self._locked_for_user.value = value

    @property
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value

    @property
    def modified_by(self):
        return self._modified_by.value

    @modified_by.setter
    def modified_by(self, value):
        self._modified_by.value = value

    @property
    def outdent(self):
        return self._outdent.value

    @outdent.setter
    def outdent(self, value):
        self._outdent.value = value

    @property
    def parent_id(self):
        return self._parent_id.value

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id.value = value

    @property
    def permalink(self):
        return self._permalink.value

    @permalink.setter
    def permalink(self, value):
        self._permalink.value = value

    @property
    def row_number(self):
        return self._row_number.value

    @row_number.setter
    def row_number(self, value):
        self._row_number.value = value

    @property
    def sheet_id(self):
        return self._sheet_id.value

    @sheet_id.setter
    def sheet_id(self, value):
        self._sheet_id.value = value

    @property
    def sibling_id(self):
        return self._sibling_id.value

    @sibling_id.setter
    def sibling_id(self, value):
        self._sibling_id.value = value

    @property
    def to_bottom(self):
        return self._to_bottom.value

    @to_bottom.setter
    def to_bottom(self, value):
        self._to_bottom.value = value

    @property
    def to_top(self):
        return self._to_top.value

    @to_top.setter
    def to_top(self, value):
        self._to_top.value = value

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value

    def get_column(self, column_id):
        for cell in self.cells:
            if cell.column_id == column_id:
                return cell

    def set_column(self, column_id, replacement_cell):
        for idx, cell in enumerate(self.cells):
            if cell.column_id == column_id:
                self.cells[idx] = replacement_cell

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
