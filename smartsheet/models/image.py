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
import json
import logging
import six

class Image(object):

    """Smartsheet Image data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Image model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.__id = None
        self._width = 0
        self._height = 0
        self._alt_text = None

        if props:
            # account for alternate variable names from raw API response
            if 'id' in props:
                self.id = props['id']
            if 'width' in props:
                self.width = props['width']
            if 'height' in props:
                self.height = props['height']
            if 'altText' in props:
                self.alt_text = props['altText']
            if 'alt_text' in props:
                self.alt_text = props['alt_text']

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.string_types):
            self.__id = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, six.integer_types):
            self._height = value

    @property
    def alt_text(self):
        return self._alt_text

    @alt_text.setter
    def alt_text(self, value):
        if isinstance(value, six.string_types):
            self._alt_text = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'width': prep(self._width),
            'height': prep(self._height),
            'altText' : prep(self._alt_text)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())