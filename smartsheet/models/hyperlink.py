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

from ..types import *
from ..util import serialize
from ..util import deserialize


class Hyperlink(object):

    """Smartsheet Hyperlink data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Hyperlink model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._report_id = Number()
        self._sheet_id = Number()
        self._sight_id = Number()
        self._url = String()

        if props:
            deserialize(self, props)

    @property
    def report_id(self):
        return self._report_id.value

    @report_id.setter
    def report_id(self, value):
        self._report_id.value = value

    @property
    def sheet_id(self):
        return self._sheet_id.value

    @sheet_id.setter
    def sheet_id(self, value):
        self._sheet_id.value = value

    @property
    def sight_id(self):
        return self._sight_id.value

    @sight_id.setter
    def sight_id(self, value):
        self._sight_id.value = value

    @property
    def url(self):
        return self._url.value

    @url.setter
    def url(self, value):
        self._url.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
