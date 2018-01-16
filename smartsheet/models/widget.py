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
from ..util import prep
from .widget_content import WidgetContent
import six
import json


class Widget(object):
    """Smartsheet Widget data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Widget model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'widget_type': [
                'CELLLINK',
                'SHEETSUMMARY',
                'RICHTEXT',
                'SHORTCUTICON',
                'SHORTCUTLIST',
                'GRIDGANTT',
                'IMAGE',
                'TITLE'
            ]}

        self._contents = None
        self._height = None
        self.__id = None
        self._show_title = None
        self._show_title_icon = None
        self._title = None
        self._title_format = None
        self._type = None
        self._version = None
        self._width = None
        self._x_position = None
        self._y_position = None

        if props:
            # account for alternate variable names from raw API response
            if 'contents' in props:
                self.contents = props['contents']
            if 'height' in props:
                self.height = props['height']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'showTitle' in props:
                self.show_title = props['showTitle']
            if 'show_title' in props:
                self.show_title = props['show_title']
            if 'showTitleIcon' in props:
                self.show_title_icon = props['showTitleIcon']
            if 'show_title_icon' in props:
                self.show_title_icon = props['show_title_icon']
            if 'title' in props:
                self.title = props['title']
            if 'titleFormat' in props:
                self.title_format = props['titleFormat']
            if 'title_format' in props:
                self.title_format = props['title_format']
            if 'type' in props:
                self.type = props['type']
            if 'version' in props:
                self.version = props['version']
            if 'width' in props:
                self.width = props['width']
            if 'xPosition' in props:
                self.x_position = props['xPosition']
            if 'x_position' in props:
                self.x_position = props['x_position']
            if 'yPosition' in props:
                self.y_position = props['yPosition']
            if 'y_position' in props:
                self.y_position = props['y_position']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, value):
        if isinstance(value, WidgetContent):
            self._contents = value
        elif isinstance(value, dict):
            self._contents = WidgetContent(value, self._base)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, six.integer_types):
            self._height = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def show_title(self):
        return self._show_title

    @show_title.setter
    def show_title(self, value):
        if isinstance(value, bool):
            self._show_title = value

    @property
    def show_title_icon(self):
        return self._show_title_icon

    @show_title_icon.setter
    def show_title_icon(self, value):
        if isinstance(value, bool):
            self._show_title_icon = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, six.string_types):
            self._title = value

    @property
    def title_format(self):
        return self._title_format

    @title_format.setter
    def title_format(self, value):
        if isinstance(value, six.string_types):
            self._title_format = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['widget_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Widget `widget_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['widget_type']))
            self._type = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    @property
    def x_position(self):
        return self._x_position

    @x_position.setter
    def x_position(self, value):
        if isinstance(value, six.integer_types):
            self._x_position = value

    @property
    def y_position(self):
        return self._y_position

    @y_position.setter
    def y_position(self, value):
        if isinstance(value, six.integer_types):
            self._y_position = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'contents': prep(self._contents),
            'id': prep(self.__id),
            'height': prep(self._height),
            'showTitle': prep(self._show_title),
            'showTitleIcon': prep(self._show_title_icon),
            'title': prep(self._title),
            'titleFormat': prep(self._title_format),
            'type': prep(self._type),
            'version': prep(self._version),
            'width': prep(self._width),
            'xPosition': prep(self._x_position),
            'yPosition': prep(self._y_position)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
