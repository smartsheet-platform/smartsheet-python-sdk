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

from .hyperlink import Hyperlink
from ..util import serialize
from ..util import deserialize


class ShortcutDataItem(object):
    """Smartsheet ShortcutDataItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ShortcutDataItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._attachment_type = None
        self._hyperlink = None
        self._label = None
        self._label_format = None
        self._mime_type = None
        self._order = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def attachment_type(self):
        return self._attachment_type

    @attachment_type.setter
    def attachment_type(self, value):
        if isinstance(value, six.string_types):
            self._attachment_type = value

    @property
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, value):
        if isinstance(value, Hyperlink):
            self._hyperlink = value
        elif isinstance(value, dict):
            self._hyperlink = Hyperlink(value, self._base)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if isinstance(value, six.string_types):
            self._label = value

    @property
    def label_format(self):
        return self._label_format

    @label_format.setter
    def label_format(self, value):
        if isinstance(value, six.string_types):
            self._label_format = value

    @property
    def mime_type(self):
        return self._mime_type

    @mime_type.setter
    def mime_type(self, value):
        if isinstance(value, six.string_types):
            self._mime_type = value

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if isinstance(value, six.integer_types):
            self._order = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
