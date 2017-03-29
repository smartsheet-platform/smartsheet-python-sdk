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

from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class ErrorResult(object):

    """Smartsheet ErrorResult data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ErrorResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._code = None
        self._message = None
        self._name = None
        self._recommendation = None
        self._ref_id = None
        self._should_retry = None
        self._status_code = None

        if props:
            # account for alternate variable names from raw API response
            if 'code' in props:
                self.code = props['code']
            if 'errorCode' in props:
                self.error_code = props['errorCode']
            if 'message' in props:
                self.message = props['message']
            if 'name' in props:
                self.name = props['name']
            if 'recommendation' in props:
                self.recommendation = props['recommendation']
            if 'refId' in props:
                self.ref_id = props['refId']
            if 'ref_id' in props:
                self.ref_id = props['ref_id']
            if 'shouldRetry' in props:
                self.should_retry = props['shouldRetry']
            if 'should_retry' in props:
                self.should_retry = props['should_retry']
            if 'statusCode' in props:
                self.status_code = props['statusCode']
            if 'status_code' in props:
                self.status_code = props['status_code']

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if isinstance(value, six.integer_types):
            self._code = value

    @property
    def error_code(self):
        return self._code

    @error_code.setter
    def error_code(self, value):
        if isinstance(value, six.integer_types):
            self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def recommendation(self):
        return self._recommendation

    @recommendation.setter
    def recommendation(self, value):
        if isinstance(value, six.string_types):
            self._recommendation = value

    @property
    def ref_id(self):
        return self._ref_id

    @ref_id.setter
    def ref_id(self, value):
        if isinstance(value, six.string_types):
            self._ref_id = value

    @property
    def should_retry(self):
        return self._should_retry

    @should_retry.setter
    def should_retry(self, value):
        if isinstance(value, bool):
            self._should_retry = value

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value):
        if isinstance(value, six.integer_types):
            self._status_code = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'code': prep(self._code),
            'message': prep(self._message),
            'name': prep(self._name),
            'recommendation': prep(self._recommendation),
            'refId':prep(self._ref_id),
            'shouldRetry': prep(self._should_retry),
            'statusCode': prep(self._status_code)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
