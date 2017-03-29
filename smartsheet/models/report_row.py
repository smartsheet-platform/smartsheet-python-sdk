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
from .row import Row
from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import logging
import six

class ReportRow(Row):

    """Smartsheet ReportRow data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportRow model."""
        super(ReportRow, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER']}

        self._in_critical_path = None
        self._cells = TypedList(Cell)
        self._sibling_id = None
        self._modified_at = None
        self._columns = TypedList(Column)
        self._row_number = None
        self.__format = None
        self._expanded = None
        self._access_level = None
        self._version = None
        self._discussions = TypedList(Discussion)
        self.__id = None
        self._parent_id = None
        self._sheet_id = None
        self._to_top = None
        self._to_bottom = None
        self._permalink = None
        self._locked_for_user = None
        self._created_at = None
        self._conditional_format = None
        self._filtered_out = None
        self._above = None
        self._locked = None
        self._attachments = TypedList(Attachment)

        if props:
            # account for alternate variable names from raw API response
            if 'inCriticalPath' in props:
                self.in_critical_path = props['inCriticalPath']
            if 'in_critical_path' in props:
                self.in_critical_path = props[
                    'in_critical_path']
            if 'cells' in props:
                self.cells = props['cells']
            if 'siblingId' in props:
                self.sibling_id = props['siblingId']
            if 'sibling_id' in props:
                self.sibling_id = props['sibling_id']
            # read only
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'columns' in props:
                self.columns = props['columns']
            # read only
            if 'rowNumber' in props:
                self.row_number = props['rowNumber']
            if 'format' in props:
                self._format = props['format']
            if '_format' in props:
                self._format = props['_format']
            if 'expanded' in props:
                self.expanded = props['expanded']
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'version' in props:
                self.version = props['version']
            if 'discussions' in props:
                self.discussions = props['discussions']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'parentId' in props:
                self.parent_id = props['parentId']
            if 'parent_id' in props:
                self.parent_id = props['parent_id']
            if 'sheetId' in props:
                self.sheet_id = props['sheetId']
            if 'sheet_id' in props:
                self.sheet_id = props['sheet_id']
            if 'toTop' in props:
                self.to_top = props['toTop']
            if 'to_top' in props:
                self.to_top = props['to_top']
            if 'toBottom' in props:
                self.to_bottom = props['toBottom']
            if 'to_bottom' in props:
                self.to_bottom = props['to_bottom']
            if 'permalink' in props:
                self.permalink = props['permalink']
            # read only
            if 'lockedForUser' in props:
                self.locked_for_user = props['lockedForUser']
            # read only
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'conditionalFormat' in props:
                self.conditional_format = props[
                    'conditionalFormat']
            if 'conditional_format' in props:
                self.conditional_format = props[
                    'conditional_format']
            # read only
            if 'filteredOut' in props:
                self.filtered_out = props['filteredOut']
            if 'above' in props:
                self.above = props['above']
            if 'locked' in props:
                self.locked = props['locked']
            if 'attachments' in props:
                self.attachments = props['attachments']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self._format
        elif key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def in_critical_path(self):
        return self._in_critical_path

    @in_critical_path.setter
    def in_critical_path(self, value):
        if isinstance(value, bool):
            self._in_critical_path = value

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
    def sibling_id(self):
        return self._sibling_id

    @sibling_id.setter
    def sibling_id(self, value):
        if isinstance(value, six.integer_types):
            self._sibling_id = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        if isinstance(value, datetime):
            self._modified_at = value

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
    def row_number(self):
        return self._row_number

    @row_number.setter
    def row_number(self, value):
        if isinstance(value, six.integer_types):
            self._row_number = value

    @property
    def _format(self):
        return self.__format

    @_format.setter
    def _format(self, value):
        if isinstance(value, six.string_types):
            self.__format = value

    @property
    def expanded(self):
        return self._expanded

    @expanded.setter
    def expanded(self, value):
        if isinstance(value, bool):
            self._expanded = value

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for ReportRow`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

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
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        if isinstance(value, six.integer_types):
            self._parent_id = value

    @property
    def sheet_id(self):
        return self._sheet_id

    @sheet_id.setter
    def sheet_id(self, value):
        if isinstance(value, six.integer_types):
            self._sheet_id = value

    @property
    def to_top(self):
        return self._to_top

    @to_top.setter
    def to_top(self, value):
        if isinstance(value, bool):
            self._to_top = value

    @property
    def to_bottom(self):
        return self._to_bottom

    @to_bottom.setter
    def to_bottom(self, value):
        if isinstance(value, bool):
            self._to_bottom = value

    @property
    def permalink(self):
        return self._permalink

    @permalink.setter
    def permalink(self, value):
        if isinstance(value, six.string_types):
            self._permalink = value

    @property
    def locked_for_user(self):
        return self._locked_for_user

    @locked_for_user.setter
    def locked_for_user(self, value):
        if isinstance(value, bool):
            self._locked_for_user = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value

    @property
    def conditional_format(self):
        return self._conditional_format

    @conditional_format.setter
    def conditional_format(self, value):
        if isinstance(value, six.string_types):
            self._conditional_format = value

    @property
    def filtered_out(self):
        return self._filtered_out

    @filtered_out.setter
    def filtered_out(self, value):
        if isinstance(value, bool):
            self._filtered_out = value

    @property
    def above(self):
        return self._above

    @above.setter
    def above(self, value):
        if isinstance(value, bool):
            self._above = value

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        if isinstance(value, bool):
            self._locked = value

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

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(ReportRow, self).to_dict(op_id, method)
        obj = {
            'inCriticalPath': prep(self._in_critical_path),
            'cells': prep(self._cells),
            'siblingId': prep(self._sibling_id),
            'modifiedAt': prep(self._modified_at),
            'columns': prep(self._columns),
            'rowNumber': prep(self._row_number),
            'format': prep(self.__format),
            'expanded': prep(self._expanded),
            'accessLevel': prep(self._access_level),
            'version': prep(self._version),
            'discussions': prep(self._discussions),
            'id': prep(self.__id),
            'parentId': prep(self._parent_id),
            'sheetId': prep(self._sheet_id),
            'toTop': prep(self._to_top),
            'toBottom': prep(self._to_bottom),
            'permalink': prep(self._permalink),
            'lockedForUser': prep(self._locked_for_user),
            'createdAt': prep(self._created_at),
            'conditionalFormat': prep(self._conditional_format),
            'filteredOut': prep(self._filtered_out),
            'above': prep(self._above),
            'locked': prep(self._locked),
            'attachments': prep(self._attachments)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
