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

from ..util import prep
from ..types import TypedList
from .user import User
from .recipient import Recipient
from datetime import datetime
from dateutil.parser import parse
import logging
import six
import json


class SentUpdateRequest(object):
    """Smartsheet SentUpdateRequest data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SentUpdateRequest model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'update_request_status': [
                'PENDING',
                'COMPLETE']}

        self.__id = None
        self._update_request_id = None
        self._sent_at = None
        self._sent_by = None
        self._status = None
        self._row_ids = TypedList(six.integer_types)
        self._column_ids = TypedList(six.integer_types)
        self._include_attachments = None
        self._include_discussions = None
        self._sent_to = None
        self._subject = None
        self._message = None

        if props:
            # account for alternate variable names from raw API response
            if 'id' in props:
                self._id = props['id']
            if '_id' in props:
                self._id = props['_id']
            if 'updateRequestId' in props:
                self.update_request_id = props['updateRequestId']
            if 'update_request_id' in props:
                self.update_request_id = props['update_request_id']
            if 'sentAt' in props:
                self.sent_at = props['sentAt']
            if 'sent_at' in props:
                self.sent_at = props['sent_at']
            if 'sendBy' in props:
                self.sent_by = props['sentBy']
            if 'send_by' in props:
                self.sent_by = props['sent_by']
            if 'status' in props:
                self.status = props['status']
            if 'rowsIds' in props:
                self.rows_ids = props['rowIds']
            if 'rows_ids' in props:
                self.rows_ids = props['row_ids']
            if 'columnIds' in props:
                self.column_ids = props['columnIds']
            if 'column_ids' in props:
                self.column_ids = props['column_ids']
            if 'includeAttachments' in props:
                self.include_attachments = props['includeAttachments']
            if 'include_attachments' in props:
                self.include_attachments = props['include_attachments']
            if 'includeDiscussions' in props:
                self.include_discussions = props['includeDiscussions']
            if 'include_discussions' in props:
                self.include_discussions = props['include_discussions']
            if 'sentTo' in props:
                self.sent_to = props['sentTo']
            if 'sent_to' in props:
                self.sent_to = props['sent_to']
            if 'subject' in props:
                self.subject = props['subject']
            if 'message' in props:
                self.message = props['message']
        # requests package Response object
        self.request_response = None
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
    def update_request_id(self):
        return self._update_request_id

    @update_request_id.setter
    def update_request_id(self, value):
        if isinstance(value, six.integer_types):
            self._update_request_id = value

    @property
    def sent_at(self):
        return self._sent_at

    @sent_at.setter
    def sent_at(self, value):
        if isinstance(value, datetime):
            self._sent_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._sent_at = value

    @property
    def sent_by(self):
        return self._sent_by

    @sent_by.setter
    def sent_by(self, value):
        if isinstance(value, User):
            self._sent_by = value
        else:
            if isinstance(value, dict):
                self._sent_by = User(value, self._base)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['update_request_status']:
                raise ValueError(
                    ("`{0}` is an invalid value for SentUpdateRequest`update_request_status`,"
                     " must be one of {1}").format(
                        value, self.allowed_values['update_request_status']))
            self._status = value

    @property
    def row_ids(self):
        return self._row_ids

    @row_ids.setter
    def row_ids(self, value):
        if isinstance(value, list):
            self._row_ids.purge()
            self._row_ids.extend([
                (int(x)
                 if not isinstance(x, int) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._row_ids.purge()
            self._row_ids = value.to_list()
        elif isinstance(value, int):
            self._row_ids.purge()
            self._row_ids.append(value)

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
        if isinstance(self, value):
            self._include_discussions = value

    @property
    def sent_to(self):
        return self._sent_to

    @sent_to.setter
    def sent_to(self, value):
        if isinstance(value, Recipient):
            self._sent_to = value
        elif isinstance(value, dict):
            self._sent_to = Recipient(value, self._base)

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, six.string_types):
            self._subject = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

    def to_dict(self, op_id=None, method=None):
        obj = {
            'id': prep(self.__id),
            'updateRequestId': prep(self._update_request_id),
            'sentAt': prep(self._sent_at),
            'sentBy': prep(self._sent_by),
            'status': prep(self._status),
            'rowIds': prep(self._row_ids),
            'columnIds': prep(self._column_ids),
            'includeAttachments': prep(self._include_attachments),
            'includeDiscussions': prep(self._include_discussions),
            'sentTo': prep(self._sent_to),
            'subject': prep(self._subject),
            'message': prep(self._message)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())