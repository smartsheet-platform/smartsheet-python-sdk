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

from ..types import *
from ..util import serialize
from ..util import deserialize


class AutoNumberFormat(object):

    """Smartsheet AutoNumberFormat data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the AutoNumberFormat model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._fill = String()
        self._prefix = String()
        self._starting_number = Number()
        self._suffix = String()

        if props:
            deserialize(self, props)

    @property
    def fill(self):
        return self._fill.value

    @fill.setter
    def fill(self, value):
        self._fill.value = value

    @property
    def prefix(self):
        return self._prefix.value

    @prefix.setter
    def prefix(self, value):
        self._prefix.value = value

    @property
    def starting_number(self):
        return self._starting_number.value

    @starting_number.setter
    def starting_number(self, value):
        self._starting_number.value = value

    @property
    def suffix(self):
        return self._suffix.value

    @suffix.setter
    def suffix(self, value):
        self._suffix.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
