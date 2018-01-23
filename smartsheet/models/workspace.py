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

from .folder import Folder
from .report import Report
from .sheet import Sheet
from .sight import Sight
from .template import Template
from ..types import TypedList
from ..util import serialize
from ..util import deserialize


class Workspace(object):

    """Smartsheet Workspace data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Workspace model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

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
        self._id_ = None
        self._name = None
        self._permalink = None
        self._reports = TypedList(Report)
        self._sheets = TypedList(Sheet)
        self._sights = TypedList(Sight)
        self._templates = TypedList(Template)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        else:
            super(Workspace, self).__setattr__(key, value)

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
        self._folders.load(value)

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

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
        self._reports.load(value)

    @property
    def sheets(self):
        return self._sheets

    @sheets.setter
    def sheets(self, value):
        self._sheets.load(value)

    @property
    def sights(self):
        return self._sights

    @sights.setter
    def sights(self, value):
        self._sights.load(value)

    @property
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
