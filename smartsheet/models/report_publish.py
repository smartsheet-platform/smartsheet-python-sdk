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

from ..util import prep
import json
import six


class ReportPublish(object):

    """Smartsheet ReportPublish data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportPublish model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._read_only_full_accessible_by = None
        self._read_only_full_default_view = None
        self._read_only_full_enabled = False
        self._read_only_full_show_toolbar = True
        self._read_only_full_url = None

        if props:
            # account for alternate variable names from raw API response
            if 'readOnlyFullAccessibleBy' in props:
                self.read_only_full_accessible_by = props['readOnlyFullAccessibleBy']
            if 'read_only_full_accessible_by' in props:
                self.read_only_full_accessible_by = props['read_only_full_accessible_by']
            if 'readOnlyFullDefaultView' in props:
                self.read_only_full_default_view = props['readOnlyFullDefaultView']
            if 'read_only_full_default_view' in props:
                self.read_only_full_default_view = props['read_only_full_default_view']
            if 'readOnlyFullEnabled' in props:
                self.read_only_full_enabled = props['readOnlyFullEnabled']
            if 'read_only_full_enabled' in props:
                self.read_only_full_enabled = props['read_only_full_enabled']
            if 'readOnlyFullShowToolbar' in props:
                self.read_only_full_show_toolbar = props['readOnlyFullShowToolbar']
            if 'read_only_full_show_toolbar' in props:
                self.read_only_full_show_toolbar = props['read_only_full_show_toolbar']
            # read only
            if 'readOnlyFullUrl' in props:
                self.read_only_full_url = props['readOnlyFullUrl']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def read_only_full_accessible_by(self):
        return self._read_only_full_accessible_by

    @read_only_full_accessible_by.setter
    def read_only_full_accessible_by(self, value):
        if isinstance(value, six.string_types):
            self._read_only_full_accessible_by = value

    @property
    def read_only_full_default_view(self):
        return self._read_only_full_default_view

    @read_only_full_default_view.setter
    def read_only_full_default_view(self, value):
        if isinstance(value, six.string_types):
            self._read_only_full_default_view = value

    @property
    def read_only_full_enabled(self):
        return self._read_only_full_enabled

    @read_only_full_enabled.setter
    def read_only_full_enabled(self, value):
        if isinstance(value, bool):
            self._read_only_full_enabled = value

    @property
    def read_only_full_show_toolbar(self):
        return self._read_only_full_show_toolbar

    @read_only_full_show_toolbar.setter
    def read_only_full_show_toolbar(self, value):
        if isinstance(value, bool):
            self._read_only_full_show_toolbar = value

    @property
    def read_only_full_url(self):
        return self._read_only_full_url

    @read_only_full_url.setter
    def read_only_full_url(self, value):
        if isinstance(value, six.string_types):
            self._read_only_full_url = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'readOnlyFullAccessibleBy': prep(self._read_only_full_accessible_by),
            'readOnlyFullDefaultView': prep(self._read_only_full_default_view),
            'readOnlyFullEnabled': prep(self._read_only_full_enabled),
            'readOnlyFullShowToolbar': prep(self._read_only_full_show_toolbar),
            'readOnlyFullUrl': prep(self._read_only_full_url)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
