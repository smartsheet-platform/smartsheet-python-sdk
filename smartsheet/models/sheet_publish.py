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

import six
import json

from ..util import serialize
from ..util import deserialize


class SheetPublish(object):

    """Smartsheet SheetPublish data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetPublish model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._ical_enabled = False
        self._ical_url = None
        self._read_only_full_accessible_by = None
        self._read_only_full_default_view = None
        self._read_only_full_enabled = False
        self._read_only_full_show_toolbar = True
        self._read_only_full_url = None
        self._read_only_lite_enabled = False
        self._read_only_lite_ssl_url = None
        self._read_only_lite_url = None
        self._read_write_accessible_by = None
        self._read_write_default_view = None
        self._read_write_enabled = False
        self._read_write_show_toolbar = True
        self._read_write_url = None

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None

    @property
    def ical_enabled(self):
        return self._ical_enabled

    @ical_enabled.setter
    def ical_enabled(self, value):
        if isinstance(value, bool):
            self._ical_enabled = value

    @property
    def ical_url(self):
        return self._ical_url

    @ical_url.setter
    def ical_url(self, value):
        if isinstance(value, six.string_types):
            self._ical_url = value

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

    @property
    def read_only_lite_enabled(self):
        return self._read_only_lite_enabled

    @read_only_lite_enabled.setter
    def read_only_lite_enabled(self, value):
        if isinstance(value, bool):
            self._read_only_lite_enabled = value

    @property
    def read_only_lite_ssl_url(self):
        return self._read_only_lite_ssl_url

    @read_only_lite_ssl_url.setter
    def read_only_lite_ssl_url(self, value):
        if isinstance(value, six.string_types):
            self._read_only_lite_ssl_url = value

    @property
    def read_only_lite_url(self):
        return self._read_only_lite_url

    @read_only_lite_url.setter
    def read_only_lite_url(self, value):
        if isinstance(value, six.string_types):
            self._read_only_lite_url = value

    @property
    def read_write_accessible_by(self):
        return self._read_write_accessible_by

    @read_write_accessible_by.setter
    def read_write_accessible_by(self, value):
        if isinstance(value, six.string_types):
            self._read_write_accessible_by = value

    @property
    def read_write_default_view(self):
        return self._read_write_default_view

    @read_write_default_view.setter
    def read_write_default_view(self, value):
        if isinstance(value, six.string_types):
            self._read_write_default_view = value

    @property
    def read_write_enabled(self):
        return self._read_write_enabled

    @read_write_enabled.setter
    def read_write_enabled(self, value):
        if isinstance(value, bool):
            self._read_write_enabled = value

    @property
    def read_write_show_toolbar(self):
        return self._read_write_show_toolbar

    @read_write_show_toolbar.setter
    def read_write_show_toolbar(self, value):
        if isinstance(value, bool):
            self._read_write_show_toolbar = value

    @property
    def read_write_url(self):
        return self._read_write_url

    @read_write_url.setter
    def read_write_url(self, value):
        if isinstance(value, six.string_types):
            self._read_write_url = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
