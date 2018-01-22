# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
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

from ..util import serialize
from ..util import deserialize


class Image(object):

    """Smartsheet Image data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Image model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._alt_text = None
        self._height = 0
        self._id_ = None
        self._width = 0

        if props:
            deserialize(self, props)

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        else:
            super(__class__, self).__setattr__(key, value)

    @property
    def alt_text(self):
        return self._alt_text

    @alt_text.setter
    def alt_text(self, value):
        if isinstance(value, six.string_types):
            self._alt_text = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, six.integer_types):
            self._height = value

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.string_types):
            self._id_ = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
