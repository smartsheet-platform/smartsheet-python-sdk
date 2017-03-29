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

from .search_result_item import SearchResultItem
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class SearchResult(object):

    """Smartsheet SearchResult data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SearchResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._results = TypedList(SearchResultItem)
        self._total_count = None

        if props:
            # account for alternate variable names from raw API response
            if 'results' in props:
                self.results = props['results']
            # read only
            if 'totalCount' in props:
                self.total_count = props['totalCount']
        # requests package Response object
        self.request_response = None

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        if isinstance(value, list):
            self._results.purge()
            self._results.extend([
                (SearchResultItem(x, self._base)
                 if not isinstance(x, SearchResultItem) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._results.purge()
            self._results = value.to_list()
        elif isinstance(value, SearchResultItem):
            self._results.purge()
            self._results.append(value)

    @property
    def total_count(self):
        return self._total_count

    @total_count.setter
    def total_count(self, value):
        if isinstance(value, six.integer_types):
            self._total_count = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'results': prep(self._results),
            'totalCount': prep(self._total_count)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
