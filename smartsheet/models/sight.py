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

from ..types import TypedList
from ..util import prep
from .widget import Widget
from datetime import datetime
from dateutil.parser import parse
import logging
import six
import json


class Sight(object):

    """Smartsheet Sight data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Sight model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'ADMIN',
                'OWNER']}

        self.__id = None
        self._name = None
        self._column_count = None
        self._widgets = TypedList(Widget)
        self._favorite = None
        self._access_level = None
        self._permalink = None
        self._created_at = None
        self._modified_at = None
        self._workspace = None

        if props:
            # account for alternate variable names from raw API response
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'name' in props:
                self.name = props['name']
            if 'columnCount' in props:
                self.column_count = props['columnCount']
            if 'column_count' in props:
                self.column_count = props['column_count']
            if 'widgets' in props:
                self.widgets = props['widgets']
            if 'favorite' in props:
                self.favorite = props['favorite']
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'permalink' in props:
                self.permalink = props['permalink']
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'created_at' in props:
                self.created_at = props['created_at']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']
            if 'workspace' in props:
                self.workspace = props['workspace']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def column_count(self):
        return self._column_count

    @column_count.setter
    def column_count(self, value):
        if isinstance(value, six.integer_types):
            self._column_count = value

    @property
    def widgets(self):
        return self._widgets

    @widgets.setter
    def widgets(self, value):
        if isinstance(value, list):
            self._widgets.purge()
            self._widgets.extend([
                (Widget(x, self._base)
                 if not isinstance(x, Widget) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._widgets.purge()
            self._widgets = value.to_list()
        elif isinstance(value, Widget):
            self._widgets.purge()
            self._widgets.append(value)

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, value):
        if isinstance(value, bool):
            self._favorite = value

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Sight`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def permalink(self):
        return self._permalink

    @permalink.setter
    def permalink(self, value):
        if isinstance(value, six.string_types):
            self._permalink = value;

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._created_at = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        if isinstance(value, datetime):
            self._modified_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._modified_at = value

    @property
    def workspace(self):
        return self._workspace

    @workspace.setter
    def workspace(self, value):
        from .workspace import Workspace
        if isinstance(value, Workspace):
            self._workspace = value
        elif isinstance(value, dict):
            self._workspace = Workspace(value, self._base)

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'name': prep(self._name),
            'columnCount': prep(self._column_count),
            'widgets': prep(self._widgets),
            'favorite': prep(self._favorite),
            'accessLevel': prep(self._access_level),
            'permalink': prep(self._permalink),
            'createdAt': prep(self._created_at),
            'modifiedA_at': prep(self._modified_at),
            'workspace': prep(self._workspace)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'update_sight':
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