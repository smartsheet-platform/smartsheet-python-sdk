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
from ..types import TypedList
from .predecessor import Predecessor
import six
import json
import logging

class ObjectValue(object):
    """Smartsheet ObjectValue data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ObjectValue model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            'object_type': [
                'DATE',
                'DATETIME',
                'ABSTRACT_DATETIME',
                'CONTACT',
                'DURATION',
                'PREDECESSOR_LIST']}

        self._object_type = None
        self._predecessors = TypedList(Predecessor)
        self._value = None

        if props:
            # account for alternate variable names from raw API response
            if 'objectType' in props:
                self.object_type = props['objectType']
            if 'object_type' in props:
                self.object_type = props['object_type']
            if 'predecessors' in props:
                self.predecessors = props['predecessors']
            if 'value' in props:
                self.value = props['value']
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

    @property
    def predecessors(self):
        return self._predecessors

    @predecessors.setter
    def predecessors(self, value):
        if isinstance(value, list):
            self._predecessors.purge()
            self._predecessors.extend([
                 (Predecessor(x, self._base)
                  if not isinstance(x, Predecessor) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._predecessors.purge()
            self._predecessors = value.to_list()
        elif isinstance(value, Predecessor):
            self._predecessors.purge()
            self._predecessors.append(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (six.string_types, six.integer_types, float, bool)):
            self._value = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        for item in self.predecessors:
            item.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'objectType': prep(self._object_type),
            'predecessors': prep(self._predecessors),
            'value': prep(self._value)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_rows':
            permitted = ['objectType', 'predecessors', 'value']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]
            if self.predecessors is not None:
                del obj['value']

        if self.pre_request_filter == 'update_rows':
            permitted = ['objectType', 'predecessors', 'value']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]
            if self.predecessors is not None:
                del obj['value']

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())