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

from .enums import AccessLevel
from .source import Source
from .widget import Widget
from ..types import *
from ..util import serialize
from ..util import deserialize


class Sight(object):

    """Smartsheet Sight data model."""

    def __init__(self, props=None, base_obj=None):
        from .workspace import Workspace
        """Initialize the Sight model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._access_level = EnumeratedValue(AccessLevel)
        self._background_color = String()
        self._column_count = Number()
        self._created_at = Timestamp()
        self._favorite = Boolean()
        self._id_ = Number()
        self._modified_at = Timestamp()
        self._name = String()
        self._permalink = String()
        self._source = TypedObject(Source)
        self._widgets = TypedList(Widget)
        self._workspace = TypedObject(Workspace)

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
            super(Sight, self).__setattr__(key, value)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level.set(value)

    @property
    def background_color(self):
        return self._background_color.value

    @background_color.setter
    def background_color(self, value):
        self._background_color.value = value

    @property
    def column_count(self):
        return self._column_count.value

    @column_count.setter
    def column_count(self, value):
        self._column_count.value = value

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def favorite(self):
        return self._favorite.value

    @favorite.setter
    def favorite(self, value):
        self._favorite.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def permalink(self):
        return self._permalink.value

    @permalink.setter
    def permalink(self, value):
        self._permalink.value = value

    @property
    def source(self):
        return self._source.value

    @source.setter
    def source(self, value):
        self._source.value = value

    @property
    def widgets(self):
        return self._widgets

    @widgets.setter
    def widgets(self, value):
        self._widgets.load(value)

    @property
    def workspace(self):
        return self._workspace.value

    @workspace.setter
    def workspace(self, value):
        self._workspace.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
