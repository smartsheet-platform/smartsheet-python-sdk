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

from .enums import SheetFilterType
from ..types import *
from ..util import serialize
from ..util import deserialize
from .sheet_filter_details import SheetFilterDetails


class SheetFilter(object):

    """Smartsheet SheetFilter data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetFilter model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._filter_type = EnumeratedValue(SheetFilterType)
        self._id_ = Number()
        self._name = String()
        self._query = TypedObject(SheetFilterDetails)
        self._version = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        else:
            super(SheetFilter, self).__setattr__(key, value)

    @property
    def filter_type(self):
        return self._filter_type

    @filter_type.setter
    def filter_type(self, value):
        self._filter_type.set(value)

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def query(self):
        return self._query.value

    @query.setter
    def query(self, value):
        self._query.value = value

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
