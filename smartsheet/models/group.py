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

import six
import json

from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from .group_member import GroupMember
from datetime import datetime
from dateutil.parser import parse


class Group(object):

    """Smartsheet Group data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Group model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._created_at = None
        self._description = None
        self._id_ = None
        self._members = TypedList(GroupMember)
        self._modified_at = None
        self._name = None
        self._owner = None
        self._owner_id = None

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
            super(__class__, self).__setattr__(key, value)

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
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

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

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
