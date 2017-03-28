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

from .group_member import GroupMember
from ..types import TypedList
from ..util import prep
from datetime import datetime
from dateutil.parser import parse
import json
import logging
import six

class Group(object):

    """Smartsheet Group data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Group model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self._created_at = None
        self._description = None
        self.__id = None
        self._members = TypedList(GroupMember)
        self._modified_at = None
        self._name = None
        self._owner = None
        self._owner_id = None

        if props:
            # account for alternate variable names from raw API response
            if 'createdAt' in props:
                self.created_at = props['createdAt']
            if 'created_at' in props:
                self.created_at = props['created_at']
            if 'description' in props:
                self.description = props['description']
            # read only
            if 'id' in props:
                self._id = props['id']
            if 'members' in props:
                self.members = props['members']
            if 'modifiedAt' in props:
                self.modified_at = props['modifiedAt']
            if 'modified_at' in props:
                self.modified_at = props['modified_at']
            if 'name' in props:
                self.name = props['name']
            if 'owner' in props:
                self.owner = props['owner']
            if 'ownerId' in props:
                self.owner_id = props['ownerId']
            if 'owner_id' in props:
                self.owner_id = props['owner_id']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

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
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, six.string_types):
            self._description = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if isinstance(value, six.integer_types):
            self.__id = value

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, value):
        if isinstance(value, list):
            self._members.purge()
            self._members.extend([
                (GroupMember(x, self._base)
                 if not isinstance(x, GroupMember) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._members.purge()
            self._members = value.to_list()
        elif isinstance(value, GroupMember):
            self._members.purge()
            self._members.append(value)

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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if isinstance(value, six.string_types):
            self._owner = value

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if isinstance(value, six.integer_types):
            self._owner_id = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.members is not None:
            # GroupMember
            for item in self.members:
                item.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.members is not None:
                for item in self.members:
                    item.pre_request_filter = req_filter

        obj = {
            'createdAt': prep(self._created_at),
            'description': prep(self._description),
            'id': prep(self.__id),
            'members': prep(self._members),
            'modifiedAt': prep(self._modified_at),
            'name': prep(self._name),
            'owner': prep(self._owner),
            'ownerId': prep(self._owner_id)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'create_group':
            permitted = ['name', 'description', 'members']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_group':
            permitted = ['name', 'description', 'ownerId']
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
