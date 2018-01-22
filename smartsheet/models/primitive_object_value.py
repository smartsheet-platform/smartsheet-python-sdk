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

from ..util import serialize


class PrimitiveObjectValue(object):
    """Smartsheet PrimitiveObjectValue data model."""

    def __init__(self, value=None, base_obj=None):
        """Initialize the PrimitiveObjectValue model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._value = value

        self.__initialized = True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (six.string_types, six.integer_types, float, bool)):
            self._value = value

    def serialize(self):
        return self._value

    def to_dict(self):
        return self._value

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
