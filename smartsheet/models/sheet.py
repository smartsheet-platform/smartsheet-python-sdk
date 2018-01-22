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
from .sheet_filter import SheetFilter
from .comment import Comment
from .discussion import Discussion
from .project_settings import ProjectSettings
from .row import Row
from .sheet_user_settings import SheetUserSettings
from .source import Source
from ..types import TypedList
from ..util import serialize
from ..util import deserialize
from datetime import datetime
from dateutil.parser import parse


class Sheet(object):

    """Smartsheet Sheet data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Sheet model."""
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
        self._filters = TypedList(SheetFilter)
        self._from_id = None
        self._gantt_enabled = None
        self._id_ = None
        self._modified_at = None
        self._name = None
        self._owner = None
        self._owner_id = None
        self._permalink = None
        self._project_settings = None
        self._read_only = None
        self._resource_management_enabled = None
        self._rows = TypedList(Row)
        self._show_parent_rows_for_filters = None
        self._source = None
        self._total_row_count = None
        self._user_settings = None
        self._version = None

        if props:
            deserialize(self, props)

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
                    ("`{0}` is an invalid value for Sheet`access_level`,"
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
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        if isinstance(value, list):
            self._filters.purge()
            self._filters.extend([
                (SheetFilter(x, self._base)
                 if not isinstance(x, SheetFilter) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._filters.purge()
            self._filters = value.to_list()
        elif isinstance(value, SheetFilter):
            self._filters.purge()
            self._filters.append(value)

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
    def project_settings(self):
        return self._project_settings

    @project_settings.setter
    def project_settings(self, value):
        if isinstance(value, ProjectSettings):
            self._project_settings = value
        elif isinstance(value, dict):
            self._project_settings = ProjectSettings(value, self._base)

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

    def add_columns(self, list_of_columns):
        return self._base.Sheets.add_columns(self.id, list_of_columns)

    def add_rows(self, list_of_rows):
        return self._base.Sheets.add_rows(self.id, list_of_rows)

    def delete_column(self, column_id):
        return self._base.Sheets.delete_column(self.id, column_id)

    def delete_rows(self, object_ids, ignore_rows_not_found=False):
        return self._base.Sheets.delete_rows(self.id, object_ids, ignore_rows_not_found)

    def get_column(self, column_id, include=None):
        return self._base.Sheets.get_column(self.id, column_id, include)

    def get_columns(self, include=None, page_size=100, page=1, include_all=False):
        return self._base.Sheets.get_columns(self.id, include, page_size, page, include_all)

    def get_row(self, row_id, include=None, exclude=None):
        return self._base.Sheets.get_row(self.id, row_id, include, exclude)

    def get_version(self):
        return self._base.Sheets.get_sheet_version(self.id)

    def list_shares(self, page_size=100, page=1, include_all=False):
        return self._base.Sheets.list_shares(self.id, page_size, page, include_all)

    def share(self, share_obj, send_email=False):
        return self._base.Sheets.share_sheet(self.id, share_obj, send_email)

    def shares(self, page_size=100, page=1, include_all=False):
        return self._base.Sheets.list_shares(self.id, page_size=100, page=1, include_all=False)

    def update_share(self, share_id, share_obj):
        return self._base.Sheets.update_share(self.id, share_id, share_obj)

    def get_share(self, share_id):
        return self._base.Sheets.get_share(self.id, share_id)

    def delete_share(self, share_id):
        return self._base.Sheets.delete_share(self.id, share_id)

    def update_name(self, new_name):
        return self._base.Sheets.update_sheet(self.id, Sheet({'name': new_name}))

    def get_publish_status(self):
        return self._base.Sheets.get_publish_status(self.id)

    def set_publish_status(self, sheet_publish_obj):
        return self._base.Sheets.set_publish_status(self.id, sheet_publish_obj)

    def create_discussion(self, title, comment, _file=None):
        dis = Discussion({
            'title': title,
            'comment': Comment({'text': comment})
        })
        if _file is not None:
            return self._base.Discussions.create_discussion_on_sheet_with_attachment(self.id, dis, _file)
        else:
            return self._base.Discussions.create_discussion_on_sheet(self.id, dis)

    def get_all_discussions(self, include=None, page_size=100, page=1, include_all=False):
        return self._base.Discussions.get_all_discussions(self.id, include, page_size, page, include_all)

    def attach_url(self, attachment_obj):
        return self._base.Attachments.attach_url_to_sheet(self.id, attachment_obj)

    def get_column_by_title(self, title):
        for col in self.columns:
            if col.title == title:
                return col

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
