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

from .enums import CrossSheetReferenceStatus
from ..types import *
from ..util import serialize
from ..util import deserialize


class CrossSheetReference(object):

    """Smartsheet CrossSheetReference data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CrossSheetReference model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._end_column_id = Number()
        self._end_row_id = Number()
        self._id_ = Number()
        self._name = String()
        self._source_sheet_id = Number()
        self._start_column_id = Number()
        self._start_row_id = Number()
        self._status = EnumeratedValue(CrossSheetReferenceStatus)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
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
            super(CrossSheetReference, self).__setattr__(key, value)

    @property
    def end_column_id(self):
        return self._end_column_id.value

    @end_column_id.setter
    def end_column_id(self, value):
        self._end_column_id.value = value

    @property
    def end_row_id(self):
        return self._end_row_id.value

    @end_row_id.setter
    def end_row_id(self, value):
        self._end_row_id.value = value

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
    def source_sheet_id(self):
        return self._source_sheet_id.value

    @source_sheet_id.setter
    def source_sheet_id(self, value):
        self._source_sheet_id.value = value

    @property
    def start_column_id(self):
        return self._start_column_id.value

    @start_column_id.setter
    def start_column_id(self, value):
        self._start_column_id.value = value

    @property
    def start_row_id(self):
        return self._start_row_id.value

    @start_row_id.setter
    def start_row_id(self, value):
        self._start_row_id.value = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status.set(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
