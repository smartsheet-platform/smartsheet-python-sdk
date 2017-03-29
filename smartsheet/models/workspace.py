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
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class Workspace(object):

    """Smartsheet Workspace data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Workspace model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER']}

        self._access_level = None
        self._favorite = None
        self._folders = TypedList(Folder)
        self.__id = None
        self._name = None
        self._permalink = None
        self._reports = TypedList(Report)
        self._sheets = TypedList(Sheet)
        self._templates = TypedList(Template)

        if props:
            # account for alternate variable names from raw API response
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'favorite' in props:
                self.favorite = props['favorite']
            if 'folders' in props:
                self.folders = props['folders']
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'name' in props:
                self.name = props['name']
            if 'permalink' in props:
                self.permalink = props['permalink']
            if 'reports' in props:
                self.reports = props['reports']
            if 'sheets' in props:
                self.sheets = props['sheets']
            if 'templates' in props:
                self.templates = props['templates']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Workspace`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, value):
        if isinstance(value, bool):
            self._favorite = value

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
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def permalink(self):
        return self._permalink

    @permalink.setter
    def permalink(self, value):
        if isinstance(value, six.string_types):
            self._permalink = value

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
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.folders is not None:
            # Folder
            for item in self.folders:
                item.pre_request_filter = value
        if self.reports is not None:
            # Report
            for item in self.reports:
                item.pre_request_filter = value
        if self.sheets is not None:
            # Sheet
            for item in self.sheets:
                item.pre_request_filter = value
        if self.templates is not None:
            # Template
            for item in self.templates:
                item.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.folders is not None:
                for item in self.folders:
                    item.pre_request_filter = req_filter
            if self.reports is not None:
                for item in self.reports:
                    item.pre_request_filter = req_filter
            if self.sheets is not None:
                for item in self.sheets:
                    item.pre_request_filter = req_filter
            if self.templates is not None:
                for item in self.templates:
                    item.pre_request_filter = req_filter

        obj = {
            'accessLevel': prep(self._access_level),
            'favorite': prep(self._favorite),
            'folders': prep(self._folders),
            'id': prep(self.__id),
            'name': prep(self._name),
            'permalink': prep(self._permalink),
            'reports': prep(self._reports),
            'sheets': prep(self._sheets),
            'templates': prep(self._templates)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'create_workspace':
            permitted = ['name']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_workspace':
            permitted = ['name']
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
