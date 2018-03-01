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

from .enums import SortDirection
from ..types import *
from ..util import serialize
from ..util import deserialize


class SortCriterion(object):

    """Smartsheet SortCriterion data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SortCriterion model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column_id = Number()
        self._direction = EnumeratedValue(SortDirection)

        if props:
            deserialize(self, props)

    @property
    def column_id(self):
        return self._column_id.value

    @column_id.setter
    def column_id(self, value):
        self._column_id.value = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction.set(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
