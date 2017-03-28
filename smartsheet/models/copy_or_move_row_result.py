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

from .row_mapping import RowMapping
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class CopyOrMoveRowResult(object):

    """Smartsheet CopyOrMoveRowResult data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CopyOrMoveRowResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._destination_sheet_id = None
        self._row_mappings = TypedList(RowMapping)

        if props:
            # account for alternate variable names from raw API response
            if 'destinationSheetId' in props:
                self.destination_sheet_id = props[
                    'destinationSheetId']
            if 'destination_sheet_id' in props:
                self.destination_sheet_id = props[
                    'destination_sheet_id']
            if 'rowMappings' in props:
                self.row_mappings = props['rowMappings']
            if 'row_mappings' in props:
                self.row_mappings = props['row_mappings']
        # requests package Response object
        self.request_response = None

    @property
    def destination_sheet_id(self):
        return self._destination_sheet_id

    @destination_sheet_id.setter
    def destination_sheet_id(self, value):
        if isinstance(value, six.integer_types):
            self._destination_sheet_id = value

    @property
    def row_mappings(self):
        return self._row_mappings

    @row_mappings.setter
    def row_mappings(self, value):
        if isinstance(value, list):
            self._row_mappings.purge()
            self._row_mappings.extend([
                (RowMapping(x, self._base)
                 if not isinstance(x, RowMapping) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._row_mappings.purge()
            self._row_mappings = value.to_list()
        elif isinstance(value, RowMapping):
            self._row_mappings.purge()
            self._row_mappings.append(value)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'destinationSheetId': prep(self._destination_sheet_id),
            'rowMappings': prep(self._row_mappings)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
