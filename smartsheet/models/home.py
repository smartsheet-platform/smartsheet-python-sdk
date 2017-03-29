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

from .folder import Folder
from .report import Report
from .sheet import Sheet
from .template import Template
from .sight import Sight
from .workspace import Workspace
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class Home(object):

    """Smartsheet Home data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Home model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._folders = TypedList(Folder)
        self._reports = TypedList(Report)
        self._sheets = TypedList(Sheet)
        self._templates = TypedList(Template)
        self._sights = TypedList(Sight)
        self._workspaces = TypedList(Workspace)

        if props:
            if 'folders' in props:
                self.folders = props['folders']
            if 'reports' in props:
                self.reports = props['reports']
            if 'sheets' in props:
                self.sheets = props['sheets']
            if 'templates' in props:
                self.templates = props['templates']
            if 'sights' in props:
                self.sights = props['sights']
            if 'workspaces' in props:
                self.workspaces = props['workspaces']
        # requests package Response object
        self.request_response = None

    @property
    def folders(self):
        return self._folders

    @folders.setter
    def folders(self, value):
        if isinstance(value, list):
            self._folders.purge()
            self._folders.extend([
                (Folder(x, self._base)
                 if not isinstance(x, Folder) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._folders.purge()
            self._folders = value.to_list()
        elif isinstance(value, Folder):
            self._folders.purge()
            self._folders.append(value)

    @property
    def reports(self):
        return self._reports

    @reports.setter
    def reports(self, value):
        if isinstance(value, list):
            self._reports.purge()
            self._reports.extend([
                (Report(x, self._base)
                 if not isinstance(x, Report) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._reports.purge()
            self._reports = value.to_list()
        elif isinstance(value, Report):
            self._reports.purge()
            self._reports.append(value)

    @property
    def sheets(self):
        return self._sheets

    @sheets.setter
    def sheets(self, value):
        if isinstance(value, list):
            self._sheets.purge()
            self._sheets.extend([
                (Sheet(x, self._base)
                 if not isinstance(x, Sheet) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._sheets.purge()
            self._sheets = value.to_list()
        elif isinstance(value, Sheet):
            self._sheets.purge()
            self._sheets.append(value)

    @property
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        if isinstance(value, list):
            self._templates.purge()
            self._templates.extend([
                (Template(x, self._base)
                 if not isinstance(x, Template) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._templates.purge()
            self._templates = value.to_list()
        elif isinstance(value, Template):
            self._templates.purge()
            self._templates.append(value)

    @property
    def sights(self):
        return self._sights

    @sights.setter
    def sights(self, value):
        if isinstance(value, list):
            self._sights.purge()
            self._sights.extend([
                (Sight(x, self._base)
                 if not isinstance(x, Sight) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._sights.purge()
            self._sights = value.to_list()
        elif isinstance(value, Sight):
            self._sights.purge()
            self._sights.append(value)

    @property
    def workspaces(self):
        return self._workspaces

    @workspaces.setter
    def workspaces(self, value):
        if isinstance(value, list):
            self._workspaces.purge()
            self._workspaces.extend([
                (Workspace(x, self._base)
                 if not isinstance(x, Workspace) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._workspaces.purge()
            self._workspaces = value.to_list()
        elif isinstance(value, Workspace):
            self._workspaces.purge()
            self._workspaces.append(value)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'folders': prep(self._folders),
            'reports': prep(self._reports),
            'sheets': prep(self._sheets),
            'templates': prep(self._templates),
            'sights': prep(self._sights),
            'workspaces': prep(self._workspaces)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
