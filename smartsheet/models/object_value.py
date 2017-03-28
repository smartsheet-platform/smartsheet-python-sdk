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
import logging
import six
import json


class ObjectValue(object):
    """Smartsheet ObjectValue data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ObjectValue model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'object_type': [
                'DATE',
                'DATETIME',
                'ABSTRACT_DATETIME',
                'CONTACT',
                'DURATION',
                'PREDECESSOR_LIST']}

        self._object_type = None

        if props:
            # account for alternate variable names from raw API response
            if 'objectType' in props:
                self.object_type = props['objectType']
            if 'object_type' in props:
                self.object_type = props['object_type']
        self.__initialized = True

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['object_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for ObjectValue`object_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['object_type']))
            self._object_type = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'objectType': prep(self._object_type)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())