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

from .duration import Duration
from .enums import PredecessorType
from ..types import *
from ..util import serialize
from ..util import deserialize


class Predecessor(object):
    """Smartsheet Predecessor data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Predecessor model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._in_critical_path = Boolean()
        self._invalid = Boolean()
        self._lag = TypedObject(Duration)
        self._row_id = Number()
        self._row_number = Number()
        self._type = EnumeratedValue(PredecessorType)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def in_critical_path(self):
        return self._in_critical_path.value

    @in_critical_path.setter
    def in_critical_path(self, value):
        self._in_critical_path.value = value

    @property
    def invalid(self):
        return self._invalid.value

    @invalid.setter
    def invalid(self, value):
            self._invalid.value = value

    @property
    def lag(self):
        return self._lag.value

    @lag.setter
    def lag(self, value):
        self._lag.value = value

    @property
    def row_id(self):
        return self._row_id.value

    @row_id.setter
    def row_id(self, value):
        self._row_id.value = value

    @property
    def row_number(self):
        return self._row_number.value

    @row_number.setter
    def row_number(self, value):
        self._row_number.value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type.set(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
