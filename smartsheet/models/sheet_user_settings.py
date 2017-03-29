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

from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class SheetUserSettings(object):

    """Smartsheet SheetUserSettings data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetUserSettings model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._critical_path_enabled = None
        self._display_summary_tasks = None

        if props:
            # account for alternate variable names from raw API response
            if 'criticalPathEnabled' in props:
                self.critical_path_enabled = props[
                    'criticalPathEnabled']
            if 'critical_path_enabled' in props:
                self.critical_path_enabled = props[
                    'critical_path_enabled']
            if 'displaySummaryTasks' in props:
                self.display_summary_tasks = props[
                    'displaySummaryTasks']
            if 'display_summary_tasks' in props:
                self.display_summary_tasks = props[
                    'display_summary_tasks']

    @property
    def critical_path_enabled(self):
        return self._critical_path_enabled

    @critical_path_enabled.setter
    def critical_path_enabled(self, value):
        if isinstance(value, bool):
            self._critical_path_enabled = value

    @property
    def display_summary_tasks(self):
        return self._display_summary_tasks

    @display_summary_tasks.setter
    def display_summary_tasks(self, value):
        if isinstance(value, bool):
            self._display_summary_tasks = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'criticalPathEnabled': prep(self._critical_path_enabled),
            'displaySummaryTasks': prep(self._display_summary_tasks)}

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
