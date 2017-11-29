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

from .criteria import Criteria
from ..types import TypedList
from ..util import prep
import json
import six

class SheetFilterDetails(object):

    """Smartsheet SheetFilterDetails data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetFilterDetails model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'operator': [
                'AND',
                'OR']}

        self._operator = None
        self._criteria = TypedList(Criteria)
        self._include_parent = None

        if props:
            # account for alternate variable names from raw API response
            if 'operator' in props:
                self.operator = props['operator']
            if 'criteria' in props:
                self.criteria = props['criteria']
            if 'includeParent' in props:
                self.include_parent = props['includeParent']
            if 'include_parent' in props:
                self.include_parent = props['include_parent']
        self.__initialized = True

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['operator']:
                raise ValueError(
                    ("`{0}` is an invalid value for Filter`operator`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['operator']))
            self._operator = value

    @property
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, value):
        if isinstance(value, list):
            self._criteria.purge()
            self._criteria.extend([
                (Criteria(x)
                 if not isinstance(x, Criteria) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._criteria.purge()
            self._criteria = value.to_list()
        elif isinstance(value, Criteria):
            self._criteria.purge()
            self._criteria.append(value)

    @property
    def include_parent(self):
        return self._include_parent

    @include_parent.setter
    def include_parent(self, value):
        if isinstance(value, bool):
            self._include_parent = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'operator': prep(self._operator),
            'criteria': prep(self._criteria),
            'includeParent': prep(self._include_parent)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
