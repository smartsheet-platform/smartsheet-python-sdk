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
from .hyperlink import Hyperlink
import logging
import six
import json

class ShortcutDataItem(object):
    """Smartsheet ShortcutDataItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ShortcutDataItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._label = None
        self._label_format = None
        self._mime_type = None
        self._hyperlink = None
        self._order = None

        if props:
            # account for alternate variable names from raw API response
            if 'label' in props:
                self.label = props['label']
            if 'labelFormat' in props:
                self.label_format = props['labelFormat']
            if 'label_format' in props:
                self.label_format = props['label_format']
            if 'mimeType' in props:
                self.mime_type = props['mimeType']
            if 'mime_type' in props:
                self.mime_type = props['mime_type']
            if 'hyperlink' in props:
                self.hyperlink = props['hyperlink']
            if 'order' in props:
                self.order = props['order']
        self.__initialized = True

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
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, value):
        if isinstance(value, Hyperlink):
            self._hyperlink = value

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if isinstance(value, six.integer_types):
            self._order = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'label': prep(self._label),
            'labelFormat': prep(self._label_format),
            'mimeTtype': prep(self._mime_type),
            'hyperlink': prep(self._hyperlink),
            'order': prep(self._order)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())