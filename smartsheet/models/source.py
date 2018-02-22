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


class Source(object):

    """Smartsheet Source data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Source model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            '_type': [
                'sheet',
                'template']}

        self._id_ = Number()
        self._type_ = String(
            accept=self.allowed_values['_type']
        )

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'id':
            return self.id_
        elif key == 'type':
            return self.type_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == 'id':
            self.id_ = value
        elif key == 'type':
            self.type_ = value
        else:
            super(Source, self).__setattr__(key, value)

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

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
