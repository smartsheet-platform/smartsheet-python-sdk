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

from .attachment import Attachment
from .column import Column
from .sheet_filter import SheetFilter
from .comment import Comment
from .contact_object_value import ContactObjectValue
from .cross_sheet_reference import CrossSheetReference
from .discussion import Discussion
from .enums import AccessLevel, AttachmentType
from .project_settings import ProjectSettings
from .row import Row
from .sheet_summary import SheetSummary
from .sheet_user_permissions import SheetUserPermissions
from .sheet_user_settings import SheetUserSettings
from .source import Source
from ..types import *
from ..util import serialize
from ..util import deserialize


class Sheet(object):

    """Smartsheet Sheet data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Sheet model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        # Workspace creates a circular import dependency, so, as much as I'm not a fan of moving the import
        # into the __init__, its the most pragmatic approach for this simple problem.
        from .workspace import Workspace

        self._access_level = EnumeratedValue(AccessLevel)
        self._attachments = TypedList(Attachment)
        self._columns = TypedList(Column)
        self._contact_references = TypedList(ContactObjectValue)
        self._created_at = Timestamp()
        self._cross_sheet_references = TypedList(CrossSheetReference)
        self._dependencies_enabled = Boolean()
        self._discussions = TypedList(Discussion)
        self._effective_attachment_options = EnumeratedList(AttachmentType)
        self._favorite = Boolean()
        self._filters = TypedList(SheetFilter)
        self._from_id = Number()
        self._gantt_enabled = Boolean()
        self._has_summary_fields = Boolean()
        self._id_ = Number()
        self._modified_at = Timestamp()
        self._name = String()
        self._owner = String()
        self._owner_id = Number()
        self._permalink = String()
        self._project_settings = TypedObject(ProjectSettings)
        self._read_only = Boolean()
        self._resource_management_enabled = Boolean()
        self._rows = TypedList(Row)
        self._show_parent_rows_for_filters = Boolean()
        self._source = TypedObject(Source)
        self._summary = TypedObject(SheetSummary)
        self._total_row_count = Number()
        self._user_permissions = TypedObject(SheetUserPermissions)
        self._user_settings = TypedObject(SheetUserSettings)
        self._version = Number()
        self._workspace = TypedObject(Workspace)

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
            super(Sheet, self).__setattr__(key, value)

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level.set(value)

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments.load(value)

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns.load(value)

    @property
    def contact_references(self):
        return self._contact_references

    @contact_references.setter
    def contact_references(self, value):
        self._contact_references.load(value)

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def cross_sheet_references(self):
        return self._cross_sheet_references

    @cross_sheet_references.setter
    def cross_sheet_references(self, value):
        self._cross_sheet_references.load(value)

    @property
    def dependencies_enabled(self):
        return self._dependencies_enabled.value

    @dependencies_enabled.setter
    def dependencies_enabled(self, value):
        self._dependencies_enabled.value = value

    @property
    def discussions(self):
        return self._discussions

    @discussions.setter
    def discussions(self, value):
        self._discussions.load(value)

    @property
    def effective_attachment_options(self):
        return self._effective_attachment_options

    @effective_attachment_options.setter
    def effective_attachment_options(self, value):
        self._effective_attachment_options.load(value)

    @property
    def favorite(self):
        return self._favorite.value

    @favorite.setter
    def favorite(self, value):
        self._favorite.value = value

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters.load(value)

    @property
    def from_id(self):
        return self._from_id.value

    @from_id.setter
    def from_id(self, value):
        self._from_id.value = value

    @property
    def gantt_enabled(self):
        return self._gantt_enabled.value

    @gantt_enabled.setter
    def gantt_enabled(self, value):
        self._gantt_enabled.value = value

    @property
    def has_summary_fields(self):
        return self._has_summary_fields.value

    @has_summary_fields.setter
    def has_summary_fields(self, value):
        self._has_summary_fields.value = value

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def owner(self):
        return self._owner.value

    @owner.setter
    def owner(self, value):
        self._owner.value = value

    @property
    def owner_id(self):
        return self._owner_id.value

    @owner_id.setter
    def owner_id(self, value):
        self._owner_id.value = value

    @property
    def permalink(self):
        return self._permalink.value

    @permalink.setter
    def permalink(self, value):
        self._permalink.value = value

    @property
    def project_settings(self):
        return self._project_settings.value

    @project_settings.setter
    def project_settings(self, value):
        self._project_settings.value = value

    @property
    def read_only(self):
        return self._read_only.value

    @read_only.setter
    def read_only(self, value):
        self._read_only.value = value

    @property
    def resource_management_enabled(self):
        return self._resource_management_enabled.value

    @resource_management_enabled.setter
    def resource_management_enabled(self, value):
        self._resource_management_enabled.value = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows.load(value)

    @property
    def show_parent_rows_for_filters(self):
        return self._show_parent_rows_for_filters.value

    @show_parent_rows_for_filters.setter
    def show_parent_rows_for_filters(self, value):
        self._show_parent_rows_for_filters.value = value

    @property
    def source(self):
        return self._source.value

    @source.setter
    def source(self, value):
        self._source.value = value

    @property
    def summary(self):
        return self._summary.value

    @summary.setter
    def summary(self, value):
        self._summary.value = value

    @property
    def total_row_count(self):
        return self._total_row_count.value

    @total_row_count.setter
    def total_row_count(self, value):
        self._total_row_count.value = value

    @property
    def user_permissions(self):
        return self._user_permissions.value

    @user_permissions.setter
    def user_permissions(self, value):
        self._user_permissions.value = value

    @property
    def user_settings(self):
        return self._user_settings.value

    @user_settings.setter
    def user_settings(self, value):
        self._user_settings.value = value

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value

    @property
    def workspace(self):
        return self._workspace.value

    @workspace.setter
    def workspace(self, value):
        self._workspace.value = value

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

    def list_shares(self, page_size=100, page=1, include_all=False, include_workspace_shares=False, access_api_level=0):
        return self._base.Sheets.list_shares(self.id, page_size, page, include_all, include_workspace_shares, access_api_level)

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
