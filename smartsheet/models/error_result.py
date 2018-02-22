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


class ErrorResult(object):

    """Smartsheet ErrorResult data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ErrorResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._code = Number()
        self._message = String()
        self._name = String()
        self._recommendation = String()
        self._ref_id = String()
        self._should_retry = Boolean()
        self._status_code = Number()

        if props:
            deserialize(self, props)
            # account for alternate variable names from raw API response

    @property
    def code(self):
        return self._code.value

    @code.setter
    def code(self, value):
        self._code.value = value

    @property
    def error_code(self):
        return self.code

    @error_code.setter
    def error_code(self, value):
        self.code = value

    @property
    def message(self):
        return self._message.value

    @message.setter
    def message(self, value):
        self._message.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def recommendation(self):
        return self._recommendation.value

    @recommendation.setter
    def recommendation(self, value):
        self._recommendation.value = value

    @property
    def ref_id(self):
        return self._ref_id.value

    @ref_id.setter
    def ref_id(self, value):
        self._ref_id.value = value

    @property
    def should_retry(self):
        return self._should_retry.value

    @should_retry.setter
    def should_retry(self, value):
        self._should_retry.value = value

    @property
    def status_code(self):
        return self._status_code.value

    @status_code.setter
    def status_code(self, value):
        self._status_code.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
