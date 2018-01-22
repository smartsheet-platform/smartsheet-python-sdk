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

import six
import json

from .attachment import Attachment
from .column import Column
from .discussion import Discussion
from .row import Row
from .sheet import Sheet
from .sheet_user_settings import SheetUserSettings
from .source import Source
from ..types import TypedList
from ..util import deserialize
from ..util import serialize
from datetime import datetime
from dateutil.parser import parse


class Report(Sheet):

    """Smartsheet Report data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Report model."""
        super(Report, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            'access_level': [
                'VIEWER',
                'EDITOR',
                'EDITOR_SHARE',
                'ADMIN',
                'OWNER']}

        self._access_level = None
        self._attachments = TypedList(Attachment)
        self._columns = TypedList(Column)
        self._created_at = None
        self._dependencies_enabled = None
        self._discussions = TypedList(Discussion)
        self._effective_attachment_options = TypedList(str)
        self._favorite = None
        self._from_id = None
        self._gantt_enabled = None
        self._id_ = None
        self._modified_at = None
        self._name = None
        self._owner = None
        self._owner_id = None
        self._permalink = None
        self._read_only = None
        self._resource_management_enabled = None
        self._rows = TypedList(Row)
        self._show_parent_rows_for_filters = None
        self._source = None
        self._source_sheets = TypedList(Sheet)
        self._total_row_count = None
        self._user_settings = None
        self._version = None

        if props:
            deserialize(self, props)
            if 'source_sheets' not in props and 'sourceSheets' not in props:
                # props is a sheet or a list of sheets
                self.source_sheets = props

        # requests package Response object
        self.request_response = None
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
            super(__class__, self).__setattr__(key, value)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['access_level']:
                raise ValueError(
                    ("`{0}` is an invalid value for Report`access_level`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['access_level']))
            self._access_level = value

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        if isinstance(value, list):
            self._attachments.purge()
            self._attachments.extend([
                (Attachment(x, self._base)
                 if not isinstance(x, Attachment) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._attachments.purge()
            self._attachments = value.to_list()
        elif isinstance(value, Attachment):
            self._attachments.purge()
            self._attachments.append(value)

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        if isinstance(value, list):
            self._columns.purge()
            self._columns.extend([
                (Column(x, self._base)
                 if not isinstance(x, Column) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._columns.purge()
            self._columns = value.to_list()
        elif isinstance(value, Column):
            self._columns.purge()
            self._columns.append(value)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if isinstance(value, datetime):
            self._created_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._created_at = value

    @property
    def dependencies_enabled(self):
        return self._dependencies_enabled

    @dependencies_enabled.setter
    def dependencies_enabled(self, value):
        if isinstance(value, bool):
            self._dependencies_enabled = value

    @property
    def discussions(self):
        return self._discussions

    @discussions.setter
    def discussions(self, value):
        if isinstance(value, list):
            self._discussions.purge()
            self._discussions.extend([
                (Discussion(x, self._base)
                 if not isinstance(x, Discussion) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._discussions.purge()
            self._discussions = value.to_list()
        elif isinstance(value, Discussion):
            self._discussions.purge()
            self._discussions.append(value)

    @property
    def effective_attachment_options(self):
        return self._effective_attachment_options

    @effective_attachment_options.setter
    def effective_attachment_options(self, value):
        if isinstance(value, list):
            self._effective_attachment_options.purge()
            self._effective_attachment_options.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._effective_attachment_options.purge()
            self._effective_attachment_options = value.to_list()
        elif isinstance(value, str):
            self._effective_attachment_options.purge()
            self._effective_attachment_options.append(value)

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, value):
        if isinstance(value, bool):
            self._favorite = value

    @property
    def from_id(self):
        return self._from_id

    @from_id.setter
    def from_id(self, value):
        if isinstance(value, six.integer_types):
            self._from_id = value

    @property
    def gantt_enabled(self):
        return self._gantt_enabled

    @gantt_enabled.setter
    def gantt_enabled(self, value):
        if isinstance(value, bool):
            self._gantt_enabled = value

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, value):
        if isinstance(value, six.integer_types):
            self._id_ = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        if isinstance(value, datetime):
            self._modified_at = value
        else:
            if isinstance(value, six.string_types):
                value = parse(value)
                self._modified_at = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, six.string_types):
            self._name = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if isinstance(value, six.string_types):
            self._owner = value

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if isinstance(value, six.integer_types):
            self._owner_id = value

    @property
    def permalink(self):
        return self._permalink

    @permalink.setter
    def permalink(self, value):
        if isinstance(value, six.string_types):
            self._permalink = value

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        if isinstance(value, bool):
            self._read_only = value

    @property
    def resource_management_enabled(self):
        return self._resource_management_enabled

    @resource_management_enabled.setter
    def resource_management_enabled(self, value):
        if isinstance(value, bool):
            self._resource_management_enabled = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        if isinstance(value, list):
            self._rows.purge()
            self._rows.extend([
                (Row(x, self._base)
                 if not isinstance(x, Row) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._rows.purge()
            self._rows = value.to_list()
        elif isinstance(value, Row):
            self._rows.purge()
            self._rows.append(value)

    @property
    def show_parent_rows_for_filters(self):
        return self._show_parent_rows_for_filters

    @show_parent_rows_for_filters.setter
    def show_parent_rows_for_filters(self, value):
        if isinstance(value, bool):
            self._show_parent_rows_for_filters = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if isinstance(value, Source):
            self._source = value
        else:
            self._source = Source(value, self._base)

    @property
    def source_sheets(self):
        return self._source_sheets

    @source_sheets.setter
    def source_sheets(self, value):
        if isinstance(value, list):
            self._source_sheets.purge()
            self._source_sheets.extend([
                (Sheet(x, self._base)
                 if not isinstance(x, Sheet) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._source_sheets.purge()
            self._source_sheets = value.to_list()
        elif isinstance(value, Sheet):
            self._source_sheets.purge()
            self._source_sheets.append(value)

    @property
    def total_row_count(self):
        return self._total_row_count

    @total_row_count.setter
    def total_row_count(self, value):
        if isinstance(value, six.integer_types):
            self._total_row_count = value

    @property
    def user_settings(self):
        return self._user_settings

    @user_settings.setter
    def user_settings(self, value):
        if isinstance(value, SheetUserSettings):
            self._user_settings = value
        else:
            self._user_settings = SheetUserSettings(value, self._base)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if isinstance(value, six.integer_types):
            self._version = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
