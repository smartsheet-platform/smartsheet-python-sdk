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


class SheetUserSettings(object):

    """Smartsheet SheetUserSettings data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetUserSettings model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._applied_sheet_filter_id = Number()
        self._critical_path_enabled = Boolean()
        self._display_summary_tasks = Boolean()

        if props:
            deserialize(self, props)

    @property
    def applied_sheet_filter_id(self):
        return self._applied_sheet_filter_id.value

    @applied_sheet_filter_id.setter
    def applied_sheet_filter_id(self, value):
        self._applied_sheet_filter_id.value = value

    @property
    def critical_path_enabled(self):
        return self._critical_path_enabled.value

    @critical_path_enabled.setter
    def critical_path_enabled(self, value):
        self._critical_path_enabled.value = value

    @property
    def display_summary_tasks(self):
        return self._display_summary_tasks.value

    @display_summary_tasks.setter
    def display_summary_tasks(self, value):
        self._display_summary_tasks.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
