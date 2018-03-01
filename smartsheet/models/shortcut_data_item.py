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

from .enums import AttachmentType
from .hyperlink import Hyperlink
from ..types import *
from ..util import serialize
from ..util import deserialize


class ShortcutDataItem(object):
    """Smartsheet ShortcutDataItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ShortcutDataItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._attachment_type = EnumeratedValue(AttachmentType)
        self._hyperlink = TypedObject(Hyperlink)
        self._label = String()
        self._label_format = String()
        self._mime_type = String()
        self._order = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def attachment_type(self):
        return self._attachment_type

    @attachment_type.setter
    def attachment_type(self, value):
        self._attachment_type.set(value)

    @property
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

    @property
    def label(self):
        return self._label.value

    @label.setter
    def label(self, value):
        self._label.value = value

    @property
    def label_format(self):
        return self._label_format.value

    @label_format.setter
    def label_format(self, value):
        self._label_format.value = value

    @property
    def mime_type(self):
        return self._mime_type.value

    @mime_type.setter
    def mime_type(self, value):
        self._mime_type.value = value

    @property
    def order(self):
        return self._order.value

    @order.setter
    def order(self, value):
        self._order.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
