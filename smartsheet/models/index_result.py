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
from .cell_history import CellHistory
from .column import Column
from .contact import Contact
from .discussion import Discussion
from .favorite import Favorite
from .folder import Folder
from .group import Group
from .report import Report
from .sent_update_request import SentUpdateRequest
from .share import Share
from .sheet import Sheet
from .sight import Sight
from .template import Template
from .update_request import UpdateRequest
from .user import User
from .webhook import Webhook
from .workspace import Workspace
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class IndexResult(object):

    """Smartsheet IndexResult data model."""

    def __init__(self, props=None, dynamic_data_type=None, base_obj=None):
        """Initialize the IndexResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._dynamic_data_type = None
        if dynamic_data_type is not None:
            self._dynamic_data_type = dynamic_data_type
        self._data = TypedList(object)
        self._page_number = None
        self._page_size = None
        self._total_count = None
        self._total_pages = None

        if props:
            # account for alternate variable names from raw API response
            if 'data' in props:
                self.data = props['data']
            if 'pageNumber' in props:
                self.page_number = props['pageNumber']
            if 'page_number' in props:
                self.page_number = props['page_number']
            if 'pageSize' in props:
                self.page_size = props['pageSize']
            if 'page_size' in props:
                self.page_size = props['page_size']
            if 'totalCount' in props:
                self.total_count = props['totalCount']
            if 'total_count' in props:
                self.total_count = props['total_count']
            if 'totalPages' in props:
                self.total_pages = props['totalPages']
            if 'total_pages' in props:
                self.total_pages = props['total_pages']
        # requests package Response object
        self.request_response = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if self._dynamic_data_type == 'AlternateEmail':
            if isinstance(value, list):
                self._data = [AlternateEmail(x, self._base) for x in value]
            else:
                self._data = AlternateEmail(value, self._base)
        if self._dynamic_data_type == 'Attachment':
            if isinstance(value, list):
                self._data = [Attachment(x, self._base) for x in value]
            else:
                self._data = Attachment(value, self._base)
        if self._dynamic_data_type == 'CellHistory':
            if isinstance(value, list):
                self._data = [CellHistory(x, self._base) for x in value]
            else:
                self._data = CellHistory(value, self._base)
        if self._dynamic_data_type == 'Column':
            if isinstance(value, list):
                self._data = [Column(x, self._base) for x in value]
            else:
                self._data = Column(value, self._base)
        if self._dynamic_data_type == 'Contact':
            if isinstance(value, list):
                self._data = [Contact(x, self._base) for x in value]
            else:
                self._data = Contact(value, self._base)
        if self._dynamic_data_type == 'Discussion':
            if isinstance(value, list):
                self._data = [Discussion(x, self._base) for x in value]
            else:
                self._data = Discussion(value, self._base)
        if self._dynamic_data_type == 'Favorite':
            if isinstance(value, list):
                self._data = [Favorite(x, self._base) for x in value]
            else:
                self._data = Favorite(value, self._base)
        if self._dynamic_data_type == 'Folder':
            if isinstance(value, list):
                self._data = [Folder(x, self._base) for x in value]
            else:
                self._data = Folder(value, self._base)
        if self._dynamic_data_type == 'Group':
            if isinstance(value, list):
                self._data = [Group(x, self._base) for x in value]
            else:
                self._data = Group(value, self._base)
        if self._dynamic_data_type == 'Report':
            if isinstance(value, list):
                self._data = [Report(x, self._base) for x in value]
            else:
                self._data = Report(value, self._base)
        if self._dynamic_data_type == 'SentUpdateRequest':
            if isinstance(value, list):
                self._data = [SentUpdateRequest(x, self._base) for x in value]
            else:
                self._data = SentUpdateRequest(value, self._base)
        if self._dynamic_data_type == 'Share':
            if isinstance(value, list):
                self._data = [Share(x, self._base) for x in value]
            else:
                self._data = Share(value, self._base)
        if self._dynamic_data_type == 'Sheet':
            if isinstance(value, list):
                self._data = [Sheet(x, self._base) for x in value]
            else:
                self._data = Sheet(value, self._base)
        if self._dynamic_data_type == 'Sight':
            if isinstance(value, list):
                self._data = [Sight(x, self._base) for x in value]
            else:
                self._data = Sight(value, self._base)
        if self._dynamic_data_type == 'Template':
            if isinstance(value, list):
                self._data = [Template(x, self._base) for x in value]
            else:
                self._data = Template(value, self._base)
        if self._dynamic_data_type == 'UpdateRequest':
            if isinstance(value, list):
                self._data = [UpdateRequest(x, self._base) for x in value]
            else:
                self._data = UpdateRequest(value, self._base)
        if self._dynamic_data_type == 'User':
            if isinstance(value, list):
                self._data = [User(x, self._base) for x in value]
            else:
                self._data = User(value, self._base)
        if self._dynamic_data_type == 'Webhook':
            if isinstance(value, list):
                self._data = [Webhook(x, self._base) for x in value]
            else:
                self._data = Webhook(value, self._base)
        if self._dynamic_data_type == 'Workspace':
            if isinstance(value, list):
                self._data = [Workspace(x, self._base) for x in value]
            else:
                self._data = Workspace(value, self._base)

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        if isinstance(value, six.integer_types):
            self._page_number = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        if isinstance(value, six.integer_types):
            self._page_size = value

    @property
    def total_count(self):
        return self._total_count

    @total_count.setter
    def total_count(self, value):
        if isinstance(value, six.integer_types):
            self._total_count = value

    @property
    def total_pages(self):
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        if isinstance(value, six.integer_types):
            self._total_pages = value

    @property
    def result(self):
        """Simplify difference between Result and IndexResult"""
        return self._data

    def to_dict(self, op_id=None, method=None):
        obj = {
            'data': prep(self._data),
            'pageNumber': prep(self._page_number),
            'pageSize': prep(self._page_size),
            'totalCount': prep(self._total_count),
            'totalPages': prep(self._total_pages)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
