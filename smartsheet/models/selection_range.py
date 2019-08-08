# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2019 Smartsheet.com, Inc.
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

from .column import Column
from .cell_data_item import CellDataItem
from .shortcut_data_item import ShortcutDataItem
from .hyperlink import Hyperlink
from ..types import *
from ..util import serialize
from ..util import deserialize


class SelectionRange(object):
    """Smartsheet SelectionRange data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SelectionRange model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._source_column_id1 = Number()
        self._source_column_id2 = Number()
        self._source_row_id1 = Number()
        self._source_row_id2 = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def source_column_id1(self):
        return self._source_column_id1.value

    @source_column_id1.setter
    def source_column_id1(self, value):
        self._source_column_id1.value = value

    @property
    def source_column_id2(self):
        return self._source_column_id2.value

    @source_column_id2.setter
    def source_column_id2(self, value):
        self._source_column_id2.value = value

    @property
    def source_row_id1(self):
        return self._source_row_id1.value

    @source_row_id1.setter
    def source_row_id1(self, value):
        self._source_row_id1.value = value

    @property
    def source_row_id2(self):
        return self._source_row_id2.value

    @source_row_id2.setter
    def source_row_id2(self, value):
        self._source_row_id2.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
