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

from ..util import prep
import json
import logging
import six

class Hyperlink(object):

    """Smartsheet Hyperlink data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Hyperlink model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._report_id = None
        self._sheet_id = None
        self._sight_id = None
        self._url = None

        if props:
            # account for alternate variable names from raw API response
            if 'reportId' in props:
                self.report_id = props['reportId']
            if 'report_id' in props:
                self.report_id = props['report_id']
            if 'sheetId' in props:
                self.sheet_id = props['sheetId']
            if 'sheet_id' in props:
                self.sheet_id = props['sheet_id']
            if 'sightId' in props:
                self.sight_id = props['sightId']
            if 'sight_id' in props:
                self.sight_id = props['sight_id']
            if 'url' in props:
                self.url = props['url']

    @property
    def report_id(self):
        return self._report_id

    @report_id.setter
    def report_id(self, value):
        if isinstance(value, six.integer_types):
            self._report_id = value

    @property
    def sheet_id(self):
        return self._sheet_id

    @sheet_id.setter
    def sheet_id(self, value):
        if isinstance(value, six.integer_types):
            self._sheet_id = value

    @property
    def sight_id(self):
        return self._sight_id

    @sight_id.setter
    def sight_id(self, value):
        if isinstance(value, six.integer_types):
            self._sight_id = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if isinstance(value, six.string_types):
            self._url = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'reportId': prep(self._report_id),
            'sheetId': prep(self._sheet_id),
            'sightId': prep(self._sight_id),
            'url': prep(self._url)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
