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

class SearchResultItem(object):

    """Smartsheet SearchResultItem data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SearchResultItem model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'object_type': [
                'row',
                'sheet',
                'report',
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
        self._object_id = None
        self._object_type = None
        self._parent_object_id = None
        self._parent_object_name = None
        self._parent_object_type = None
        self._text = None

        if props:
            # account for alternate variable names from raw API response
            if 'contextData' in props:
                self.context_data = props['contextData']
            if 'context_data' in props:
                self.context_data = props['context_data']
            # read only
            if 'objectId' in props:
                self.object_id = props['objectId']
            # read only
            if 'objectType' in props:
                self.object_type = props['objectType']
            # read only
            if 'parentObjectId' in props:
                self.parent_object_id = props['parentObjectId']
            # read only
            if 'parentObjectName' in props:
                self.parent_object_name = props[
                    'parentObjectName']
            # read only
            if 'parentObjectType' in props:
                self.parent_object_type = props[
                    'parentObjectType']
            if 'text' in props:
                self.text = props['text']

    @property
    def context_data(self):
        return self._context_data

    @context_data.setter
    def context_data(self, value):
        if isinstance(value, list):
            self._context_data.purge()
            self._context_data.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._context_data.purge()
            self._context_data = value.to_list()
        elif isinstance(value, str):
            self._context_data.purge()
            self._context_data.append(value)

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

    def to_dict(self, op_id=None, method=None):
        obj = {
            'contextData': prep(self._context_data),
            'objectId': prep(self._object_id),
            'objectType': prep(self._object_type),
            'parentObjectId': prep(self._parent_object_id),
            'parentObjectName': prep(self._parent_object_name),
            'parentObjectType': prep(self._parent_object_type),
            'text': prep(self._text)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
