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

from .email import Email
from ..types import TypedList
from ..util import serialize
from ..util import deserialize


class RowEmail(Email):

    """Smartsheet RowEmail data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the RowEmail model."""
        super(RowEmail, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column_ids = TypedList(int)
        self._include_attachments = False
        self._include_discussions = False
        self._layout = None

        if props:
            deserialize(self, props)

    @property
    def column_ids(self):
        return self._column_ids

    @column_ids.setter
    def column_ids(self, value):
        self._column_ids.load(value)

    @property
    def include_attachments(self):
        return self._include_attachments

    @include_attachments.setter
    def include_attachments(self, value):
        if isinstance(value, bool):
            self._include_attachments = value

    @property
    def include_discussions(self):
        return self._include_discussions

    @include_discussions.setter
    def include_discussions(self, value):
        if isinstance(value, bool):
            self._include_discussions = value

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        if isinstance(value, six.string_types):
            self._layout = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
