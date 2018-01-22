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

import six
import json

from .column import Column
from .cell_data_item import CellDataItem
from .shortcut_data_item import ShortcutDataItem
from .hyperlink import Hyperlink
from ..types import TypedList
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
        self._hyperlink = None

        """Represents the RichtextWidgetContent object."""
        self._html = None

        """Represents the ShortcutWidgetContent object."""
        self._shortcut_data = TypedList(ShortcutDataItem)

        """Represents the ReportWidgetContent object."""
        self._html_content = None

        """Represents the ImageWidgetContent object."""
        self._file_name = None
        self._format_ = None
        self._height = None
        self._private_id = None
        self._width = None

        """Represents the TitleWidgetContent object."""
        self._background_color = None

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
            super(__class__, self).__setattr__(key, value)

    """Represents the CellLinkWidgetContent object."""
    @property
    def cell_data(self):
        return self._cell_data

    @cell_data.setter
    def cell_data(self, value):
        if isinstance(value, list):
            self._cell_data.purge()
            self._cell_data.extend([
                (CellDataItem(x, self._base)
                 if not isinstance(x, CellDataItem) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._cell_data.purge()
            self._cell_data = value.to_list()
        elif isinstance(value, CellDataItem):
            self._cell_data.purge()
            self._cell_data.append(value)

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
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, value):
        if isinstance(value, Hyperlink):
            self._hyperlink = value
        elif isinstance(value, dict):
            self._hyperlink = Hyperlink(value, self._base)

    """Represents the RichtextWidgetContent object."""
    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        if isinstance(value, six.string_types):
            self._html = value

    """Represents the ShortcutWidgetContent object."""
    @property
    def shortcut_data(self):
        return self._shortcut_data

    @shortcut_data.setter
    def shortcut_data(self, value):
        if isinstance(value, list):
            self._shortcut_data.purge()
            self._shortcut_data.extend([
                (ShortcutDataItem(x, self._base)
                 if not isinstance(x, ShortcutDataItem) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._shortcut_data.purge()
            self._shortcut_data = value.to_list()
        elif isinstance(value, ShortcutDataItem):
            self._shortcut_data.purge()
            self._shortcut_data.append(value)

    """Represents the ReportWidgetContent object."""
    @property
    def html_content(self):
        return self._html_content

    @html_content.setter
    def html_content(self, value):
        if isinstance(value, six.string_types):
            self._html_content = value

    """Represents the ImageWidgetContent object."""
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if isinstance(value, six.string_types):
            self._file_name = value

    @property
    def format_(self):
        return self._format_

    @format_.setter
    def format_(self, value):
        if isinstance(value, six.string_types):
            self._format_ = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, six.integer_types):
            self._height = value

    @property
    def private_id(self):
        return self._private_id

    @private_id.setter
    def private_id(self, value):
        if isinstance(value, six.string_types):
            self._private_id = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    """Represents the TitleWidgetContent object."""
    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        if isinstance(value, six.string_types):
            self._background_color = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
