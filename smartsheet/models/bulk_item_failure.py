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
from .error_result import ErrorResult
import json
import logging
import six

class BulkItemFailure(object):

    """Smartsheet BulkItemFailure data model."""

    def __init__(self, props=None, dynamic_result_type=None, base_obj=None):
        """Initialize the BulkItemFailure model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._index = None
        self._error = None
        self._row_id = None

        if props:
            # account for alternate variable names from raw API response
            if 'index' in props:
                self.index = props['index']
            if 'error' in props:
                self.error = props['error']
            if 'rowId' in props:
                self.row_id = props['rowId']
            if 'row_id' in props:
                self.row_id = props['row_id']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if isinstance(value, six.integer_types):
            self._index = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if isinstance(value, dict):
            self._error = self._result = ErrorResult(value, self._base)

    @property
    def row_id(self):
        return self._row_id

    @row_id.setter
    def row_id(self, value):
        if isinstance(value, six.integer_types):
            self._row_id = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'index': prep(self._index),
            'error': prep(self._error),
            'rowId': prep(self._row_id)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())