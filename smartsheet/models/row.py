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

from .attachment import Attachment
from .cell import Cell
from .column import Column
from .discussion import Discussion
from ..types import TypedList
from .user import User
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class Row(object):

    """Smartsheet Row data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Row model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER']}

        self._above = None
        self._access_level = None
        self._attachments = TypedList(Attachment)
        self._cells = TypedList(Cell)
        self._columns = TypedList(Column)
        self._conditional_format = None
        self._created_at = None
        self._created_by = None
        self._discussions = TypedList(Discussion)
        self._expanded = None
        self._filtered_out = None
        self._format_ = None
        self._id_ = None
        self._in_critical_path = None
        self._indent = None
        self._locked = None
        self._locked_for_user = None
        self._modified_at = None
        self._modified_by = None
        self._outdent = None
        self._parent_id = None
        self._permalink = None
        self._row_number = None
        self._sheet_id = None
        self._sibling_id = None
        self._to_bottom = None
        self._to_top = None
        self._version = None

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
        return self._above

    @above.setter
    def above(self, value):
        if isinstance(value, bool):
            self._above = value

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Row`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        if isinstance(value, list):
            self._attachments.purge()
            self._attachments.extend([
                (Attachment(x, self._base)
                 if not isinstance(x, Attachment) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._attachments.purge()
            self._attachments = value.to_list()
        elif isinstance(value, Attachment):
            self._attachments.purge()
            self._attachments.append(value)

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        if isinstance(value, list):
            self._cells.purge()
            self._cells.extend([
                (Cell(x, self._base)
                 if not isinstance(x, Cell) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._cells.purge()
            self._cells = value.to_list()
        elif isinstance(value, Cell):
            self._cells.purge()
            self._cells.append(value)

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        if isinstance(value, list):
            self._columns.purge()
            self._columns.extend([
                (Column(x, self._base)
                 if not isinstance(x, Column) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._columns.purge()
            self._columns = value.to_list()
        elif isinstance(value, Column):
            self._columns.purge()
            self._columns.append(value)

    @property
    def conditional_format(self):
        return self._conditional_format

    @conditional_format.setter
    def conditional_format(self, value):
        if isinstance(value, six.string_types):
            self._conditional_format = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._created_at = value

    @property
    def created_by(self):
        return self._created_by

    @created_by.setter
    def created_by(self, value):
        if isinstance(value, User):
            self._created_by = value
        else:
            self._created_by = User(value, self._base)

    @property
    def discussions(self):
        return self._discussions

    @discussions.setter
    def discussions(self, value):
        if isinstance(value, list):
            self._discussions.purge()
            self._discussions.extend([
                (Discussion(x, self._base)
                 if not isinstance(x, Discussion) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._discussions.purge()
            self._discussions = value.to_list()
        elif isinstance(value, Discussion):
            self._discussions.purge()
            self._discussions.append(value)

    @property
    def expanded(self):
        return self._expanded

    @expanded.setter
    def expanded(self, value):
        if isinstance(value, bool):
            self._expanded = value

    @property
    def filtered_out(self):
        return self._filtered_out

    @filtered_out.setter
    def filtered_out(self, value):
        if isinstance(value, bool):
            self._filtered_out = value

    @property
    def format_(self):
        return self._format_

    @format_.setter
    def format_(self, value):
        if isinstance(value, six.string_types):
            self._format_ = value

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def in_critical_path(self):
        return self._in_critical_path

    @in_critical_path.setter
    def in_critical_path(self, value):
        if isinstance(value, bool):
            self._in_critical_path = value

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, value):
        if isinstance(value, six.integer_types):
            self._indent = value

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        if isinstance(value, bool):
            self._locked = value

    @property
    def locked_for_user(self):
        return self._locked_for_user

    @locked_for_user.setter
    def locked_for_user(self, value):
        if isinstance(value, bool):
            self._locked_for_user = value

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
    def outdent(self):
        return self._outdent

    @outdent.setter
    def outdent(self, value):
        if isinstance(value, six.integer_types):
            self._outdent = value

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        if isinstance(value, (six.integer_types, type(None))):
            self._parent_id = value

    @property
    def permalink(self):
        return self._permalink

    @permalink.setter
    def permalink(self, value):
        if isinstance(value, six.string_types):
            self._permalink = value

    @property
    def row_number(self):
        return self._row_number

    @row_number.setter
    def row_number(self, value):
        if isinstance(value, six.integer_types):
            self._row_number = value

    @property
    def sheet_id(self):
        return self._sheet_id

    @sheet_id.setter
    def sheet_id(self, value):
        if isinstance(value, six.integer_types):
            self._sheet_id = value

    @property
    def sibling_id(self):
        return self._sibling_id

    @sibling_id.setter
    def sibling_id(self, value):
        if isinstance(value, (six.integer_types, type(None))):
            self._sibling_id = value

    @property
    def to_bottom(self):
        return self._to_bottom

    @to_bottom.setter
    def to_bottom(self, value):
        if isinstance(value, bool):
            self._to_bottom = value

    @property
    def to_top(self):
        return self._to_top

    @to_top.setter
    def to_top(self, value):
        if isinstance(value, bool):
            self._to_top = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

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
