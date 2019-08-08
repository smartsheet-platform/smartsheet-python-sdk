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

from .report_column import ReportColumn
from .report_row import ReportRow
from .sheet import Sheet
from .scope import Scope
from ..types import *
from ..util import deserialize
from ..util import serialize


class Report(Sheet):

    """Smartsheet Report data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Report model."""
        super(Report, self).__init__(None, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._columns = TypedList(ReportColumn)
        self._rows = TypedList(ReportRow)
        self._scope = TypedObject(Scope)
        self._source_sheets = TypedList(Sheet)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns.load(value)

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows.load(value)

    @property
    def scope(self):
        return self._scope.value

    @scope.setter
    def scope(self, value):
        self._scope.value = value

    @property
    def source_sheets(self):
        return self._source_sheets

    @source_sheets.setter
    def source_sheets(self, value):
        self._source_sheets.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
