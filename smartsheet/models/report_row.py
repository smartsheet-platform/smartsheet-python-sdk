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

from .row import Row
from .report_cell import ReportCell
from ..types import *
from ..util import serialize
from ..util import deserialize


class ReportRow(Row):

    """Smartsheet ReportRow data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportRow model."""
        super(ReportRow, self).__init__(None, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._cells = TypedList(ReportCell)
        self._sheet_id = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells.load(value)

    @property
    def sheet_id(self):
        return self._sheet_id.value

    @sheet_id.setter
    def sheet_id(self, value):
        self._sheet_id.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
