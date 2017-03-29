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

class Template(object):

    """Smartsheet Template data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Template model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER'],
            'type': [
                'sheet',
                'report'],
            'global_template': [
                'BLANK_SHEET',
                'TASK_LIST',
                'PROJECT_SHEET' ]}

        self.__id = None
        self._name = None
        self._description = None
        self._access_level = None
        self._image = None
        self._large_image = None
        self._locale = None
        self._type = None
        self._tags = TypedList(six.string_types)
        self._categories = TypedList(six.string_types)
        self._blank = None
        self._global_template = None

        if props:
            # account for alternate variable names from raw API response
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'name' in props:
                self.name = props['name']
            if 'description' in props:
                self.description = props['description']
            if 'accessLevel' in props:
                self.access_level = props['accessLevel']
            if 'access_level' in props:
                self.access_level = props['access_level']
            if 'image' in props:
                self.image = props['image']
            if 'largeImage' in props:
                self.large_image = props['largeImage']
            if 'large_image' in props:
                self.large_image = props['large_image']
            if 'locale' in props:
                self.locale = props['locale']
            if 'type' in props:
                self.type = props['type']
            if 'tags' in props:
                self.tags = props['tags']
            if 'categories' in props:
                self.categories = props['categories']
            if 'blank' in props:
                self.blank = props['blank']
            if 'globalTemplate' in props:
                self.global_template = props['globalTemplate']
            if 'global_template' in props:
                self.global_template = props['global_template']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self._id
        else:
            raise AttributeError(key)

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
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, six.string_types):
            self._description = value

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Template`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if isinstance(value, six.string_types):
            self._image = value

    @property
    def large_image(self):
        return self._large_image

    @large_image.setter
    def large_image(self, value):
        if isinstance(value, six.string_types):
            self._large_image = value

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        if isinstance(value, six.string_types):
            self._locale = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['type']:
                raise ValueError(
                    ("`{0}` is an invalid value for Template`type`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['type']))
            self._type = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if isinstance(value, list):
            self._tags.purge()
            self._tags.extend([
                (six.string_types(x, self._base)
                 if not isinstance(x, six.string_types) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._tags.purge()
            self._tags = value.to_list()
        elif isinstance(value, six.string_types):
            self._tags.purge()
            self._tags.append(value)

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        if isinstance(value, list):
            self._categories.purge()
            self._categories.extend([
                (six.string_types(x, self._base)
                 if not isinstance(x, six.string_types) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._categories.purge()
            self._categories = value.to_list()
        elif isinstance(value, six.string_types):
            self._categories.purge()
            self._categories.append(value)

    @property
    def blank(self):
        return self._blank

    @blank.setter
    def blank(self, value):
        if isinstance(value, bool):
            self._blank = value

    @property
    def global_template(self):
        return self._global_template

    @global_template.setter
    def global_template(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['global_template']:
                raise ValueError(
                    ("`{0}` is an invalid value for Template`type`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['global_template']))
            self._global_template = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'name': prep(self._name),
            'description': prep(self._description),
            'accessLevel': prep(self._access_level),
            'image': prep(self._image),
            'largeImage': prep(self._large_image),
            'locale': prep(self._locale),
            'type': prep(self._type),
            'tags': prep(self._tags),
            'categories': prep(self._categories),
            'blank': prep(self._blank),
            'globalTemplate': prep(self._global_template)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
