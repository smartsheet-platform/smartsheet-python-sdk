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

from .row_email import RowEmail
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class MultiRowEmail(RowEmail):

    """Smartsheet MultiRowEmail data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the MultiRowEmail model."""
        super(MultiRowEmail, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self._row_ids = TypedList(int)

        if props:
            # account for alternate variable names from raw API response
            if 'rowIds' in props:
                self.row_ids = props['rowIds']
            if 'row_ids' in props:
                self.row_ids = props['row_ids']

    @property
    def row_ids(self):
        return self._row_ids

    @row_ids.setter
    def row_ids(self, value):
        if isinstance(value, list):
            self._row_ids.purge()
            self._row_ids.extend([
                (int(x)
                 if not isinstance(x, int) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._row_ids.purge()
            self._row_ids = value.to_list()
        elif isinstance(value, int):
            self._row_ids.purge()
            self._row_ids.append(value)

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(MultiRowEmail, self).to_dict(op_id, method)
        obj = {
            'rowIds': prep(self._row_ids)}
        obj = MultiRowEmail._apply_pre_request_filter(self, obj)
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'update_update_request':
            permitted = []
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj', key)
                    del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
