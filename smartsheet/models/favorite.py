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

from ..types import *
from ..util import serialize
from ..util import deserialize


class Favorite(object):

    """Smartsheet Favorite data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Favorite model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            '_type': [
                'workspace',
                'folder',
                'sheet',
                'report',
                'template',
                'sight']}

        self._object_id = Number()
        self._type_ = String(
            accept=self.allowed_values['_type']
        )

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'type':
            return self.type_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'type':
            self.type_ = value
        else:
            super(Favorite, self).__setattr__(key, value)

    @property
    def object_id(self):
        return self._object_id.value

    @object_id.setter
    def object_id(self, value):
        self._object_id.value = value

    @property
    def type_(self):
        return self._type_.value

    @type_.setter
    def type_(self, value):
        self._type_.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
