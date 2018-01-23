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

from ..types import TypedList
from ..util import serialize
from ..util import deserialize


class SearchResultItem(object):

    """Smartsheet SearchResultItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SearchResultItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'object_type': [
                'row',
                'sheet',
                'report',
                'folder',
                'workspace',
                'sight',
                'template',
                'discussion',
                'attachment'],
            'parent_object_type': [
                'workspace',
                'folder',
                'sheet',
                'report',
                'template']}

        self._context_data = TypedList(str)
        self._favorite = None
        self._object_id = None
        self._object_type = None
        self._parent_object_favorite = None
        self._parent_object_id = None
        self._parent_object_name = None
        self._parent_object_type = None
        self._text = None

        if props:
            deserialize(self, props)

    @property
    def context_data(self):
        return self._context_data

    @context_data.setter
    def context_data(self, value):
        self._context_data.load(value)

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, value):
        if isinstance(value, bool):
            self._favorite = value

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        if isinstance(value, six.integer_types):
            self._object_id = value

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['object_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for SearchResultItem`object_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['object_type']))
            self._object_type = value

    @property
    def parent_object_favorite(self):
        return self._parent_object_favorite

    @parent_object_favorite.setter
    def parent_object_favorite(self, value):
        if isinstance(value, bool):
            self._parent_object_favorite = value

    @property
    def parent_object_id(self):
        return self._parent_object_id

    @parent_object_id.setter
    def parent_object_id(self, value):
        if isinstance(value, six.integer_types):
            self._parent_object_id = value

    @property
    def parent_object_name(self):
        return self._parent_object_name

    @parent_object_name.setter
    def parent_object_name(self, value):
        if isinstance(value, six.string_types):
            self._parent_object_name = value

    @property
    def parent_object_type(self):
        return self._parent_object_type

    @parent_object_type.setter
    def parent_object_type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['parent_object_type']:
                raise ValueError(
                    ("`{0}` is an invalid value for SearchResultItem`parent_object_type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['parent_object_type']))
            self._parent_object_type = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if isinstance(value, six.string_types):
            self._text = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
