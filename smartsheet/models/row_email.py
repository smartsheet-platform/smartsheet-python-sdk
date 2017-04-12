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

from .email import Email
from .recipient import Recipient
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class RowEmail(Email):

    """Smartsheet RowEmail data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the RowEmail model."""
        super(RowEmail, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._column_ids = TypedList(int)
        self._include_attachments = False
        self._include_discussions = False
        self._layout = None

        if props:
            # account for alternate variable names from raw API response
            if 'columnIds' in props:
                self.column_ids = props['columnIds']
            if 'column_ids' in props:
                self.column_ids = props['column_ids']
            if 'includeAttachments' in props:
                self.include_attachments = props[
                    'includeAttachments']
            if 'include_attachments' in props:
                self.include_attachments = props[
                    'include_attachments']
            if 'includeDiscussions' in props:
                self.include_discussions = props[
                    'includeDiscussions']
            if 'include_discussions' in props:
                self.include_discussions = props[
                    'include_discussions']
            if 'layout' in props:
                self.layout = props['layout']

    @property
    def column_ids(self):
        return self._column_ids

    @column_ids.setter
    def column_ids(self, value):
        if isinstance(value, list):
            self._column_ids.purge()
            self._column_ids.extend([
                (int(x)
                 if not isinstance(x, int) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._column_ids.purge()
            self._column_ids = value.to_list()
        elif isinstance(value, int):
            self._column_ids.purge()
            self._column_ids.append(value)

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

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(RowEmail, self).to_dict(op_id, method)
        obj = {
            'columnIds': prep(self._column_ids),
            'includeAttachments': prep(self._include_attachments),
            'includeDiscussions': prep(self._include_discussions),
            'layout' : prep(self._layout)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
