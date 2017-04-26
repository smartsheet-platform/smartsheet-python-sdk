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

from .attachment import Attachment
from .cell import Cell
from .column import Column
from .discussion import Discussion
from ..types import TypedList
from .user import User
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import logging
import six

class Row(object):

    """Smartsheet Row data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Row model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

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
        self.__format = None
        self.__id = None
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
            # account for alternate variable names from raw API response
            if 'above' in props:
                self.above = props['above']
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'attachments' in props:
                self.attachments = props['attachments']
            if 'cells' in props:
                self.cells = props['cells']
            if 'columns' in props:
                self.columns = props['columns']
            if 'conditionalFormat' in props:
                self.conditional_format = props[
                    'conditionalFormat']
            if 'conditional_format' in props:
                self.conditional_format = props[
                    'conditional_format']
            # read only
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'createdBy' in props:
                self.created_by = props['createdBy']
            if 'discussions' in props:
                self.discussions = props['discussions']
            if 'expanded' in props:
                self.expanded = props['expanded']
            # read only
            if 'filteredOut' in props:
                self.filtered_out = props['filteredOut']
            if 'format' in props:
                self._format = props['format']
            if '_format' in props:
                self._format = props['_format']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'inCriticalPath' in props:
                self.in_critical_path = props['inCriticalPath']
            if 'in_critical_path' in props:
                self.in_critical_path = props[
                    'in_critical_path']
            if 'indent' in props:
                self.indent = props['indent']
            if 'locked' in props:
                self.locked = props['locked']
            # read only
            if 'lockedForUser' in props:
                self.locked_for_user = props['lockedForUser']
            # read only
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modifiedBy' in props:
                self.modified_by = props['modifiedBy']
            if 'outdent' in props:
                self.outdent = props['outdent']
            if 'parentId' in props:
                self.parent_id = props['parentId']
            if 'parent_id' in props:
                self.parent_id = props['parent_id']
            if 'permalink' in props:
                self.permalink = props['permalink']
            # read only
            if 'rowNumber' in props:
                self.row_number = props['rowNumber']
            # read only
            if 'sheetId' in props:
                self.sheet_id = props['sheetId']
            if 'siblingId' in props:
                self.sibling_id = props['siblingId']
            if 'sibling_id' in props:
                self.sibling_id = props['sibling_id']
            if 'toBottom' in props:
                self.to_bottom = props['toBottom']
            if 'to_bottom' in props:
                self.to_bottom = props['to_bottom']
            if 'toTop' in props:
                self.to_top = props['toTop']
            if 'to_top' in props:
                self.to_top = props['to_top']
            if 'version' in props:
                self.version = props['version']

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self._format
        elif key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self._id = value
        else:
            object.__setattr__(self, key, value)

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
    def _format(self):
        return self.__format

    @_format.setter
    def _format(self, value):
        if isinstance(value, six.string_types):
            self.__format = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

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

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.attachments is not None:
            # Attachment
            for item in self.attachments:
                item.pre_request_filter = value
        if self.cells is not None:
            # Cell
            for item in self.cells:
                item.pre_request_filter = value
        if self.columns is not None:
            # Column
            for item in self.columns:
                item.pre_request_filter = value
        if self.discussions is not None:
            # Discussion
            for item in self.discussions:
                item.pre_request_filter = value
        self._pre_request_filter = value

    def get_column(self, column_id):
        for cell in self.cells:
            if cell.column_id == column_id:
                return cell

    def set_column(self, column_id, replacement_cell):
        for idx, cell in enumerate(self.cells):
            if cell.column_id == column_id:
                self.cells[idx] = replacement_cell

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.attachments is not None:
                for item in self.attachments:
                    item.pre_request_filter = req_filter
            if self.cells is not None:
                for item in self.cells:
                    item.pre_request_filter = req_filter
            if self.columns is not None:
                for item in self.columns:
                    item.pre_request_filter = req_filter
            if self.discussions is not None:
                for item in self.discussions:
                    item.pre_request_filter = req_filter

        obj = {
            'above': prep(self._above),
            'accessLevel': prep(self._access_level),
            'attachments': prep(self._attachments),
            'cells': prep(self._cells),
            'columns': prep(self._columns),
            'conditionalFormat': prep(self._conditional_format),
            'createdAt': prep(self._created_at),
            'createdBy': prep(self._created_by),
            'discussions': prep(self._discussions),
            'expanded': prep(self._expanded),
            'filteredOut': prep(self._filtered_out),
            'format': prep(self.__format),
            'id': prep(self.__id),
            'inCriticalPath': prep(self._in_critical_path),
            'indent': prep(self._indent),
            'locked': prep(self._locked),
            'lockedForUser': prep(self._locked_for_user),
            'modifiedAt': prep(self._modified_at),
            'modifiedBy': prep(self._modified_by),
            'outdent': prep(self._outdent),
            'parentId': prep(self._parent_id),
            'permalink': prep(self._permalink),
            'rowNumber': prep(self._row_number),
            'sheetId': prep(self._sheet_id),
            'siblingId': prep(self._sibling_id),
            'toBottom': prep(self._to_bottom),
            'toTop': prep(self._to_top),
            'version': prep(self._version)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_rows':
            permitted = ['format', 'expanded', 'locked',
                         'cells', 'toTop', 'toBottom', 'above', 'siblingId',
                         'parentId']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_rows':
            permitted = ['id', 'format', 'expanded',
                         'locked', 'cells', 'toTop', 'toBottom', 'above',
                         'siblingId', 'parentId', 'indent', 'outdent']
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
