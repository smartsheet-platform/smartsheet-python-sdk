# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
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


class RowMapping(object):

    """Smartsheet RowMapping data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the RowMapping model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._from_ = Number()
        self._to = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'from':
            return self.from_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'from':
            self.from_ = value
        else:
            super(RowMapping, self).__setattr__(key, value)

    @property
    def from_(self):
        return self._from_.value

    @from_.setter
    def from_(self, value):
        self._from_.value = value

    @property
    def to(self):
        return self._to.value

    @to.setter
    def to(self, value):
        self._to.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
