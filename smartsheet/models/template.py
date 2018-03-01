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

from .enums import AccessLevel, GlobalTemplate
from ..types import *
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
            'type': [
                'sheet',
                'report']}

        self._access_level = EnumeratedValue(AccessLevel)
        self._blank = Boolean()
        self._categories = TypedList(six.string_types)
        self._description = String()
        self._global_template = EnumeratedValue(GlobalTemplate)
        self._id_ = Number()
        self._image = String()
        self._large_image = String()
        self._locale = String()
        self._name = String()
        self._tags = TypedList(six.string_types)
        self._type = String(
            accept=self.allowed_values['type']
        )

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
        self._access_level.set(value)

    @property
    def blank(self):
        return self._blank.value

    @blank.setter
    def blank(self, value):
        self._blank.value = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories.load(value)

    @property
    def description(self):
        return self._description.value

    @description.setter
    def description(self, value):
        self._description.value = value

    @property
    def global_template(self):
        return self._global_template

    @global_template.setter
    def global_template(self, value):
        self._global_template.set(value)

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def image(self):
        return self._image.value

    @image.setter
    def image(self, value):
        self._image.value = value

    @property
    def large_image(self):
        return self._large_image.value

    @large_image.setter
    def large_image(self, value):
        self._large_image.value = value

    @property
    def locale(self):
        return self._locale.value

    @locale.setter
    def locale(self, value):
        self._locale.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.load(value)

    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, value):
        self._type.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
