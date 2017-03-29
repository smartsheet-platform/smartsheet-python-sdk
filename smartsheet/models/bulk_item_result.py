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

from .row import Row
from .bulk_item_failure import BulkItemFailure
from ..types import TypedList
from ..util import prep
import json
import logging
import six

class BulkItemResult(object):

    """Smartsheet BulkItemResult data model."""

    def __init__(self, props=None, dynamic_result_type=None, base_obj=None):
        """Initialize the BulkItemResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._dynamic_result_type = None
        if dynamic_result_type is not None:
            self._dynamic_result_type = dynamic_result_type
        self._message = None
        self._result = TypedList(object)
        self._result_code = None
        self._version = None
        self._failed_items = TypedList(BulkItemFailure)

        if props:
            # account for alternate variable names from raw API response
            if 'message' in props:
                self.message = props['message']
            if 'result' in props:
                self.result = props['result']
            if 'resultCode' in props:
                self.result_code = props['resultCode']
            if 'result_code' in props:
                self.result_code = props['result_code']
            if 'version' in props:
                self.version = props['version']
            if 'failedItems' in props:
                self.failed_items = props['failedItems']
            if 'failed_items' in props:
                self.failed_items = props['failed_items']
        self.__initialized = True

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if self._dynamic_result_type == 'Row':
            if isinstance(value, list):
                self._result = [Row(x, self._base) for x in value]
            else:
                self._result = Row(value, self._base)

    @property
    def result_code(self):
        return self._result_code

    @result_code.setter
    def result_code(self, value):
        if isinstance(value, six.integer_types):
            self._result_code = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

    @property
    def failed_items(self):
        return self._failed_items

    @failed_items.setter
    def failed_items(self, value):
        if isinstance(value, list):
            self._failed_items = [BulkItemFailure(x, self._base) for x in value]
        else:
            self._failed_items = BulkItemFailure(value, self._base)

    @property
    def data(self):
        """Simplify difference between Result and IndexResult"""
        return self._result

    def to_dict(self, op_id=None, method=None):
        obj = {
            'message': prep(self._message),
            'result': prep(self._result),
            'resultCode': prep(self._result_code),
            'version': prep(self._version),
            'failedItems':prep(self._failed_items)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
