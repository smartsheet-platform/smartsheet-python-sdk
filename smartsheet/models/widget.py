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

from .enums.widget_type import WidgetType
from .cell_link_widget_content import CellLinkWidgetContent
from .chart_widget_content import ChartWidgetContent
from .error_result import ErrorResult
from .image_widget_content import ImageWidgetContent
from .report_widget_content import ReportWidgetContent
from .shortcut_widget_content import ShortcutWidgetContent
from .title_rich_text_widget_content import TitleRichTextWidgetContent
from .web_content_widget_content import WebContentWidgetContent
from .widget_content import WidgetContent
from ..types import *
from ..util import serialize
from ..util import deserialize


class Widget(object):
    """Smartsheet Widget data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Widget model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._contents = None
        self._error = TypedObject(ErrorResult)
        self._height = Number()
        self._id_ = Number()
        self._show_title = Boolean()
        self._show_title_icon = Boolean()
        self._title = String()
        self._title_format = String()
        self._type = EnumeratedValue(WidgetType)
        self._version = Number()
        self._width = Number()
        self._x_position = Number()
        self._y_position = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        else:
            super(Widget, self).__setattr__(key, value)

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, value):
        if isinstance(value, WidgetContent):
            self._contents = value
        elif isinstance(value, dict):
            widget_type = value['type']
            try:
                widget_type = WidgetType[widget_type]
            except KeyError:
                if widget_type == "WidgetWebContent":
                    widget_type = WidgetType.WEBCONTENT
                else:
                    widget_type = None
            if widget_type == WidgetType.CHART:
                self._contents = ChartWidgetContent(value, self._base)
            elif widget_type == WidgetType.IMAGE:
                self._contents = ImageWidgetContent(value, self._base)
            elif widget_type == WidgetType.METRIC:
                self._contents = CellLinkWidgetContent(value, self._base)
            elif widget_type == WidgetType.GRIDGANTT:
                self._contents = ReportWidgetContent(value, self._base)
            elif widget_type == WidgetType.RICHTEXT or widget_type == WidgetType.TITLE:
                self._contents = TitleRichTextWidgetContent(value, self._base)
            elif widget_type == WidgetType.SHORTCUT:
                self._contents = ShortcutWidgetContent(value, self._base)
            elif widget_type == WidgetType.WEBCONTENT:
                self._contents = WebContentWidgetContent(value, self._base)
            else:
                self._contents = None

    @property
    def error(self):
        return self._error.value

    @error.setter
    def error(self, value):
        self._error.value = value

    @property
    def height(self):
        return self._height.value

    @height.setter
    def height(self, value):
        self._height.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def show_title(self):
        return self._show_title.value

    @show_title.setter
    def show_title(self, value):
        self._show_title.value = value

    @property
    def show_title_icon(self):
        return self._show_title_icon.value

    @show_title_icon.setter
    def show_title_icon(self, value):
        self._show_title_icon.value = value

    @property
    def title(self):
        return self._title.value

    @title.setter
    def title(self, value):
        self._title.value = value

    @property
    def title_format(self):
        return self._title_format.value

    @title_format.setter
    def title_format(self, value):
        self._title_format.value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type.set(value)

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value

    @property
    def width(self):
        return self._width.value

    @width.setter
    def width(self, value):
        self._width.value = value

    @property
    def x_position(self):
        return self._x_position.value

    @x_position.setter
    def x_position(self, value):
        self._x_position.value = value

    @property
    def y_position(self):
        return self._y_position.value

    @y_position.setter
    def y_position(self, value):
        self._y_position.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
