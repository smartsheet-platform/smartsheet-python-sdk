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
from .enums import WidgetType
from .widget_content import WidgetContent
from .widget_hyperlink import WidgetHyperlink
from ..types import *
from ..util import serialize
from ..util import deserialize


class CellLinkWidgetContent(WidgetContent):
    """Smartsheet CellLinkWidgetContent data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CellLinkWidgetContent model."""
        super(CellLinkWidgetContent, self).__init__(WidgetType.METRIC, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        """Represents the CellLinkWidgetContent object."""
        self._sheet_id = Number()
        self._cell_data = TypedList(CellDataItem)
        self._columns = TypedList(Column)
        self._hyperlink = TypedObject(WidgetHyperlink)

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
            super(WidgetContent, self).__setattr__(key, value)

    """Represents the CellLinkWidgetContent object."""
    @property
    def sheet_id(self):
        return self._sheet_id.value

    @sheet_id.setter
    def sheet_id(self, value):
        self._sheet_id.value = value

    @property
    def cell_data(self):
        return self._cell_data

    @cell_data.setter
    def cell_data(self, value):
        self._cell_data.load(value)

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns.load(value)

    @property
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
