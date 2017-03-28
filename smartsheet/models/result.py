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

from .alternate_email import AlternateEmail
from .attachment import Attachment
from .column import Column
from .comment import Comment
from .discussion import Discussion
from .favorite import Favorite
from .folder import Folder
from .group import Group
from .group_member import GroupMember
from .row import Row
from .share import Share
from .sheet import Sheet
from .sheet_publish import SheetPublish
from .update_request import UpdateRequest
from .user import User
from .webhook import Webhook
from .webhook_secret import WebhookSecret
from .workspace import Workspace
from .report_publish import ReportPublish
from .sent_update_request import SentUpdateRequest
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class Result(object):

    """Smartsheet Result data model."""

    def __init__(self, props=None, dynamic_result_type=None, base_obj=None):
        """Initialize the Result model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._dynamic_result_type = None
        if dynamic_result_type is not None:
            self._dynamic_result_type = dynamic_result_type
        self._message = None
        self._result = TypedList(object)
        self._result_code = None
        self._version = None

        if props:
            # account for alternate variable names from raw API response
            if 'message' in props:
                self.message = props['message']
            if 'result' in props:
                self.result = props['result']
            if 'resultCode' in props:
                self.result_code = props['resultCode']
            if 'result_code' in props:
                self.result_code = props['result_code']
            if 'version' in props:
                self.version = props['version']
        # requests package Response object
        self.request_response = None

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if self._dynamic_result_type == 'AlternateEmail':
            if isinstance(value, list):
                self._result = [AlternateEmail(x, self._base) for x in value]
            else:
                self._result = AlternateEmail(value, self._base)
        if self._dynamic_result_type == 'Attachment':
            if isinstance(value, list):
                self._result = [Attachment(x, self._base) for x in value]
            else:
                self._result = Attachment(value, self._base)
        if self._dynamic_result_type == 'Column':
            if isinstance(value, list):
                self._result = [Column(x, self._base) for x in value]
            else:
                self._result = Column(value, self._base)
        if self._dynamic_result_type == 'Comment':
            if isinstance(value, list):
                self._result = [Comment(x, self._base) for x in value]
            else:
                self._result = Comment(value, self._base)
        if self._dynamic_result_type == 'Discussion':
            if isinstance(value, list):
                self._result = [Discussion(x, self._base) for x in value]
            else:
                self._result = Discussion(value, self._base)
        if self._dynamic_result_type == 'Favorite':
            if isinstance(value, list):
                self._result = [Favorite(x, self._base) for x in value]
            else:
                self._result = Favorite(value, self._base)
        if self._dynamic_result_type == 'Folder':
            if isinstance(value, list):
                self._result = [Folder(x, self._base) for x in value]
            else:
                self._result = Folder(value, self._base)
        if self._dynamic_result_type == 'Group':
            if isinstance(value, list):
                self._result = [Group(x, self._base) for x in value]
            else:
                self._result = Group(value, self._base)
        if self._dynamic_result_type == 'GroupMember':
            if isinstance(value, list):
                self._result = [GroupMember(x, self._base) for x in value]
            else:
                self._result = GroupMember(value, self._base)
        if self._dynamic_result_type == 'Row':
            if isinstance(value, list):
                self._result = [Row(x, self._base) for x in value]
            else:
                self._result = Row(value, self._base)
        if self._dynamic_result_type == 'SentUpdateRequest':
            if isinstance(value, list):
                self._result = [SentUpdateRequest(x, self._base) for x in value]
            else:
                self._result = SentUpdateRequest(value, self._base)
        if self._dynamic_result_type == 'Share':
            if isinstance(value, list):
                self._result = [Share(x, self._base) for x in value]
            else:
                self._result = Share(value, self._base)
        if self._dynamic_result_type == 'Sheet':
            if isinstance(value, list):
                self._result = [Sheet(x, self._base) for x in value]
            else:
                self._result = Sheet(value, self._base)
        if self._dynamic_result_type == 'SheetPublish':
            if isinstance(value, list):
                self._result = [SheetPublish(x, self._base) for x in value]
            else:
                self._result = SheetPublish(value, self._base)
        if self._dynamic_result_type == 'UpdateRequest':
            if isinstance(value, list):
                self._result = [UpdateRequest(x, self._base) for x in value]
            else:
                self._result = UpdateRequest(value, self._base)
        if self._dynamic_result_type == 'User':
            if isinstance(value, list):
                self._result = [User(x, self._base) for x in value]
            else:
                self._result = User(value, self._base)
        if self._dynamic_result_type == 'Webhook':
            if isinstance(value, list):
                self._result = [Webhook(x, self._base) for x in value]
            else:
                self._result = Webhook(value, self._base)
        if self._dynamic_result_type == 'WebhookSecret':
            if isinstance(value, list):
                self._result = [WebhookSecret(x, self._base) for x in value]
            else:
                self._result = WebhookSecret(value, self._base)
        if self._dynamic_result_type == 'Workspace':
            if isinstance(value, list):
                self._result = [Workspace(x, self._base) for x in value]
            else:
                self._result = Workspace(value, self._base)
        if self._dynamic_result_type == 'ReportPublish':
            if isinstance(value, list):
                self._result = [ReportPublish(x, self._base) for x in value]
            else:
                self._result = ReportPublish(value, self._base)

    @property
    def result_code(self):
        return self._result_code

    @result_code.setter
    def result_code(self, value):
        if isinstance(value, six.integer_types):
            self._result_code = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

    @property
    def data(self):
        """Simplify difference between Result and IndexResult"""
        return self._result

    def to_dict(self, op_id=None, method=None):
        obj = {
            'message': prep(self._message),
            'result': prep(self._result),
            'resultCode': prep(self._result_code),
            'version': prep(self._version)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
