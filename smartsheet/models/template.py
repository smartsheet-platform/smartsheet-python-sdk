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


class Template(object):

    """Smartsheet Template data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Template model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

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
                'PROJECT_SHEET']}

        self._access_level = None
        self._blank = None
        self._categories = TypedList(six.string_types)
        self._description = None
        self._global_template = None
        self._id_ = None
        self._image = None
        self._large_image = None
        self._locale = None
        self._name = None
        self._tags = TypedList(six.string_types)
        self._type = None

        if props:
            deserialize(self, props)

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
            super(Template, self).__setattr__(key, value)

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
    def blank(self):
        return self._blank

    @blank.setter
    def blank(self, value):
        if isinstance(value, bool):
            self._blank = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories.load(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, six.string_types):
            self._description = value

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

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.load(value)

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

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
