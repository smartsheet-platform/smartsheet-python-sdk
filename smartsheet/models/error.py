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

import json

from .error_result import ErrorResult
from ..util import serialize
from ..util import deserialize
from ..types import TypedObject


class Error(object):

    """Smartsheet Error data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Error model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._request_response = None
        self._result = TypedObject(ErrorResult)

        if props:
            deserialize(self, props)

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
        return self._result.value

    @result.setter
    def result(self, value):
        self._result.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
