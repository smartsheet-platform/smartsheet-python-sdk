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

from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class CellLink(object):

    """Smartsheet CellLink data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellLink model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'status': [
                'OK',
                'BROKEN',
                'INACCESSIBLE',
                'NOT_SHARED',
                'BLOCKED',
                'CIRCULAR',
                'INVALID',
                'DISABLED']}

        self._column_id = None
        self._row_id = None
        self._sheet_id = None
        self._sheet_name = None
        self._status = None

        if props:
            # account for alternate variable names from raw API response
            if 'columnId' in props:
                self.column_id = props['columnId']
            if 'column_id' in props:
                self.column_id = props['column_id']
            if 'rowId' in props:
                self.row_id = props['rowId']
            if 'row_id' in props:
                self.row_id = props['row_id']
            if 'sheetId' in props:
                self.sheet_id = props['sheetId']
            if 'sheet_id' in props:
                self.sheet_id = props['sheet_id']
            if 'sheetName' in props:
                self.sheet_name = props['sheetName']
            if 'sheet_name' in props:
                self.sheet_name = props['sheet_name']
            if 'status' in props:
                self.status = props['status']

    @property
    def column_id(self):
        return self._column_id

    @column_id.setter
    def column_id(self, value):
        if isinstance(value, six.integer_types):
            self._column_id = value

    @property
    def row_id(self):
        return self._row_id

    @row_id.setter
    def row_id(self, value):
        if isinstance(value, six.integer_types):
            self._row_id = value

    @property
    def sheet_id(self):
        return self._sheet_id

    @sheet_id.setter
    def sheet_id(self, value):
        if isinstance(value, six.integer_types):
            self._sheet_id = value

    @property
    def sheet_name(self):
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, value):
        if isinstance(value, six.string_types):
            self._sheet_name = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['status']:
                raise ValueError(
                    ("`{0}` is an invalid value for CellLink`status`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['status']))
            self._status = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'columnId': prep(self._column_id),
            'rowId': prep(self._row_id),
            'sheetId': prep(self._sheet_id),
            'sheetName': prep(self._sheet_name),
            'status': prep(self._status)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
