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

from ..types import TypedList
from ..util import prep
from .column import Column
from .cell_data_item import CellDataItem
from .shortcut_data_item import ShortcutDataItem
import logging
import six
import json


class WidgetContent(object):
    """Smartsheet WidgetContent data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the WidgetContent model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        """Represents the CellLinkWidgetContent object."""
        self._hyperlink = None
        self._cell_data = TypedList(CellDataItem)
        self._column = TypedList(Column)

        """Represents the RichtextWidgetContent object."""
        self._html = None

        """Represents the ShortcutWidgetContent object."""
        self._shortcut_data = TypedList(ShortcutDataItem)

        """Represents the ReportWidgetContent object."""
        self._html_content = None

        """Represents the ImageWidgetContent object."""
        self._private_id = None
        self._height = None
        self._width = None
        self._file_name = None
        self._format = None

        """Represents the TitleWidgetContent object."""
        self._background_color = None

        if props:
            # account for alternate variable names from raw API response
            if 'hyperlink' in props:
                self.hyperlink = props['id']
            if 'cellData' in props:
                self.cell_data = props['cellData']
            if 'cell_data' in props:
                self.cell_data = props['cell_data']
            if 'column' in props:
                self.column = props['column']
            if 'html' in props:
                self.html = props['html']
            if 'shortcutData' in props:
                self.shortcut_data = props['shortcutData']
            if 'shortcut_data' in props:
                self.shortcut_data = props['shortcut_data']
            if 'htmlContent' in props:
                self.html_content = props['htmlContent']
            if 'html_content' in props:
                self.html_content = props['html_content']
            if 'privateId' in props:
                self.private_id = props['privateId']
            if 'private_id' in props:
                self.private_id = props['private_id']
            if 'height' in props:
                self.height = props['height']
            if 'width' in props:
                self.width = props['width']
            if 'fileName' in props:
                self.file_name = props['fileName']
            if 'file_name' in props:
                self.file_name = props['file_name']
            if 'format' in props:
                self.format = props['format']
            if 'backgroundColor' in props:
                self.background_color = props['backgroundColor']
            if 'background_color' in props:
                self.background_color = props['background_color']
        self.__initialized = True

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

    @property
    def html_content(self):
        return self._html_content

    @html_content.setter
    def html_content(self, value):
        if isinstance(value, six.string_types):
            self._html_content = value

    @property
    def private_id(self):
        return self._private_id

    @private_id.setter
    def private_id(self, value):
        if isinstance(value, six.string_types):
            self._private_id = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, six.integer_types):
            self._height = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if isinstance(value, six.string_types):
            self._file_name = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if isinstance(value, six.string_types):
            self._format = value

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        if isinstance(value, six.string_types):
            self._background_color = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'hyperlink': prep(self._hyperlink),
            'cellData': prep(self._cell_data),
            'column': prep(self._column),
            'html': prep(self._html),
            'shortcutData': prep(self._shortcut_data),
            'htmlContent': prep(self._html_content),
            'privateId': prep(self._private_id),
            'height': prep(self._height),
            'width': prep(self._width),
            'fileName': prep(self._file_name),
            'format': prep(self._format),
            'backgroundColor': prep(self._background_color)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())