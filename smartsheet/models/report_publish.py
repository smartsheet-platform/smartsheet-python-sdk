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
import json
import logging
import six

class ReportPublish(object):

    """Smartsheet ReportPublish data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportPublish model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self._read_only_full_enabled = False
        self._read_only_full_url = None
        self._read_only_full_accessible_by = None

        if props:
            # account for alternate variable names from raw API response
            if 'readOnlyFullEnabled' in props:
                self.read_only_full_enabled = props[
                    'readOnlyFullEnabled']
            if 'read_only_full_enabled' in props:
                self.read_only_full_enabled = props[
                    'read_only_full_enabled']
            # read only
            if 'readOnlyFullUrl' in props:
                self.read_only_full_url = props[
                    'readOnlyFullUrl']
            if 'readOnlyFullAccessibleBy' in props:
                self.read_only_full_accessible_by = props[
                    'readOnlyFullAccessibleBy']
            if 'read_only_full_accessible_by' in props:
                self.read_only_full_accessible_by = props[
                    'read_only_full_accessible_by']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def read_only_full_enabled(self):
        return self._read_only_full_enabled

    @read_only_full_enabled.setter
    def read_only_full_enabled(self, value):
        if isinstance(value, bool):
            self._read_only_full_enabled = value

    @property
    def read_only_full_url(self):
        return self._read_only_full_url

    @read_only_full_url.setter
    def read_only_full_url(self, value):
        if isinstance(value, six.string_types):
            self._read_only_full_url = value

    @property
    def read_only_full_accessible_by(self):
        return self._read_only_full_accessible_by

    @read_only_full_accessible_by.setter
    def read_only_full_accessible_by(self, value):
        if isinstance(value, six.string_types):
            self._read_only_full_accessible_by = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'readOnlyFullEnabled': prep(self._read_only_full_enabled),
            'readOnlyFullAccessibleBy': prep(self._read_only_full_accessible_by),
            'readOnlyFullUrl': prep(self._read_only_full_url)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'set_publish_status':
            permitted = ['readOnlyFullEnabled', 'readOnlyFullAccessibleBy']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
