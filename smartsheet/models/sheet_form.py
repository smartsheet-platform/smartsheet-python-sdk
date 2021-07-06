# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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

from .enums import SheetFilterType
from ..types import *
from ..util import serialize
from ..util import deserialize


class SheetForm(object):

    """Smartsheet SheetForm data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetForm model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
            self._id = Number()
            self._publish_type = String()
            self._publish_key = String()
            self._publish_url = String()
            self._title = String()
            self._published = Boolean()

        if props:
            deserialize(self, props)

        self.request_response = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id.value = value

    @property
    def publish_type(self):
        return self._publish_type.value

    @publish_type.setter
    def publish_type(self, value):
        self._publish_type.value = value

    @property
    def publish_key(self):
        return self._publish_key.value

    @publish_key.setter
    def publish_key(self, value):
        self._publish_key.value = value

    @property
    def publish_url(self):
        return self._publish_url

    @publish_url.setter
    def publish_url(self, value):
        self._publish_url.value = value
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title.value = value

    @property
    def published(self):
        return self._published

    @published.setter
    def published(self, value):
        self._published.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
        