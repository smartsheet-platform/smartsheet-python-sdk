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

from .enums import WidgetType
from .widget_hyperlink import WidgetHyperlink
from .widget_content import WidgetContent
from ..types import *
from ..util import serialize
from ..util import deserialize


class ImageWidgetContent(WidgetContent):
    """Smartsheet ImageWidgetContent data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ImageWidgetContent model."""
        super(ImageWidgetContent, self).__init__(WidgetType.IMAGE, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        """Represents the ImageWidgetContent object."""
        self._file_name = String()
        self._format_ = String()
        self._height = Number()
        self._hyperlink = TypedObject(WidgetHyperlink)
        self._private_id = String()
        self._width = Number()

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
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

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

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
