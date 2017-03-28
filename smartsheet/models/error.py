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

from .error_result import ErrorResult
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class Error(object):

    """Smartsheet Error data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Error model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._request_response = None
        self._result = None

        if props:
            # account for alternate variable names from raw API response
            if 'requestResponse' in props:
                self.request_response = props['requestResponse']
            if 'request_response' in props:
                self.request_response = props[
                    'request_response']
            if 'result' in props:
                self.result = props['result']
        self.message = 'ERROR'

        # requests package Response object
        self.request_response = None

    @property
    def request_response(self):
        return self._request_response

    @request_response.setter
    def request_response(self, value):
        if isinstance(value, object):
            self._request_response = value
        else:
            self._request_response = object(value, self._base)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if isinstance(value, ErrorResult):
            self._result = value
        else:
            self._result = ErrorResult(value, self._base)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'requestResponse': prep(self._request_response),
            'result': prep(self._result)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
