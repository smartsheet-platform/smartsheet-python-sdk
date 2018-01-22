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


class AutoNumberFormat(object):

    """Smartsheet AutoNumberFormat data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AutoNumberFormat model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._fill = None
        self._prefix = None
        self._starting_number = None
        self._suffix = None

        if props:
            deserialize(self, props)

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value):
        if isinstance(value, six.string_types):
            self._fill = value

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        if isinstance(value, six.string_types):
            self._prefix = value

    @property
    def starting_number(self):
        return self._starting_number

    @starting_number.setter
    def starting_number(self, value):
        if isinstance(value, six.integer_types):
            self._starting_number = value

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        if isinstance(value, six.string_types):
            self._suffix = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
