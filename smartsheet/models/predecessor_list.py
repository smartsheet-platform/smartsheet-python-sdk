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
from .object_value import *
import json


class PredecessorList(ObjectValue):
    """Smartsheet PredecessorList data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the PredecessorList model."""
        super(PredecessorList, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._predecessors = TypedList(Predecessor)

        if props:
            # account for alternate variable names from raw API response
            if 'predecessors' in props:
                self.predecessors = props['predecessors']
        else:
            self.object_type = PREDECESSOR_LIST

        self.__initialized = True

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
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        for item in self.predecessors:
            item.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(PredecessorList, self).to_dict(op_id, method)
        obj = {
            'predecessors': prep(self._predecessors)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())