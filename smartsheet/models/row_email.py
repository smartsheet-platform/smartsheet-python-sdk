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
        self._log = logging.getLogger(__name__)
        self._log.info('initializing RowEmail (%s)', __name__)

        self._message = None
        self._column_ids = TypedList(int)
        self._send_to = TypedList(Recipient)
        self._include_attachments = False
        self._subject = None
        self._include_discussions = False
        self._cc_me = False

        if props:
            # account for alternate variable names from raw API response
            if 'message' in props:
                self.message = props['message']
            if 'columnIds' in props:
                self.column_ids = props['columnIds']
            if 'column_ids' in props:
                self.column_ids = props['column_ids']
            if 'sendTo' in props:
                self.send_to = props['sendTo']
            if 'send_to' in props:
                self.send_to = props['send_to']
            if 'includeAttachments' in props:
                self.include_attachments = props[
                    'includeAttachments']
            if 'include_attachments' in props:
                self.include_attachments = props[
                    'include_attachments']
            if 'subject' in props:
                self.subject = props['subject']
            if 'includeDiscussions' in props:
                self.include_discussions = props[
                    'includeDiscussions']
            if 'include_discussions' in props:
                self.include_discussions = props[
                    'include_discussions']
            if 'ccMe' in props:
                self.cc_me = props['ccMe']
            if 'cc_me' in props:
                self.cc_me = props['cc_me']

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

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
    def send_to(self):
        return self._send_to

    @send_to.setter
    def send_to(self, value):
        if isinstance(value, list):
            self._send_to.purge()
            self._send_to.extend([
                (Recipient(x, self._base)
                 if not isinstance(x, Recipient) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._send_to.purge()
            self._send_to = value.to_list()
        elif isinstance(value, Recipient):
            self._send_to.purge()
            self._send_to.append(value)

    @property
    def include_attachments(self):
        return self._include_attachments

    @include_attachments.setter
    def include_attachments(self, value):
        if isinstance(value, bool):
            self._include_attachments = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, six.string_types):
            self._subject = value

    @property
    def include_discussions(self):
        return self._include_discussions

    @include_discussions.setter
    def include_discussions(self, value):
        if isinstance(value, bool):
            self._include_discussions = value

    @property
    def cc_me(self):
        return self._cc_me

    @cc_me.setter
    def cc_me(self, value):
        if isinstance(value, bool):
            self._cc_me = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(RowEmail, self).to_dict(op_id, method)
        obj = {
            'message': prep(self._message),
            'columnIds': prep(self._column_ids),
            'sendTo': prep(self._send_to),
            'includeAttachments': prep(self._include_attachments),
            'subject': prep(self._subject),
            'includeDiscussions': prep(self._include_discussions),
            'ccMe': prep(self._cc_me)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
