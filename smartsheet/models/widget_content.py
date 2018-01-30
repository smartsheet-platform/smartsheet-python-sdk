# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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


class WidgetContent(object):
    """Smartsheet WidgetContent data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the WidgetContent model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        """Represents the CellLinkWidgetContent object."""
        self._cell_data = TypedList(CellDataItem)
        self._columns = TypedList(Column)
        self._hyperlink = TypedObject(Hyperlink)

        """Represents the RichtextWidgetContent object."""
        self._html = String()

        """Represents the ShortcutWidgetContent object."""
        self._shortcut_data = TypedList(ShortcutDataItem)

        """Represents the ReportWidgetContent object."""
        self._html_content = String()

        """Represents the ImageWidgetContent object."""
        self._file_name = String()
        self._format_ = String()
        self._height = Number()
        self._private_id = String()
        self._width = Number()

        """Represents the TitleWidgetContent object."""
        self._background_color = String()

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

    """Represents the RichtextWidgetContent object."""
    @property
    def html(self):
        return self._html.value

    @html.setter
    def html(self, value):
        self._html.value = value

    """Represents the ShortcutWidgetContent object."""
    @property
    def shortcut_data(self):
        return self._shortcut_data

    @shortcut_data.setter
    def shortcut_data(self, value):
        self._shortcut_data.load(value)

    """Represents the ReportWidgetContent object."""
    @property
    def html_content(self):
        return self._html_content.value

    @html_content.setter
    def html_content(self, value):
        self._html_content.value = value

    """Represents the ImageWidgetContent object."""
    @property
    def file_name(self):
        return self._file_name.value

    @file_name.setter
    def file_name(self, value):
        self._file_name.value = value

    @property
    def format_(self):
        return self._format_.value

    @format_.setter
    def format_(self, value):
        self._format_.value = value

    @property
    def height(self):
        return self._height.value

    @height.setter
    def height(self, value):
        self._height.value = value

    @property
    def private_id(self):
        return self._private_id.value

    @private_id.setter
    def private_id(self, value):
        self._private_id.value = value

    @property
    def width(self):
        return self._width.value

    @width.setter
    def width(self, value):
        self._width.value = value

    """Represents the TitleWidgetContent object."""
    @property
    def background_color(self):
        return self._background_color.value

    @background_color.setter
    def background_color(self, value):
        self._background_color.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
