# pylint: disable=C0111,R0902,R0913
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

from .models import DownloadedFile
from .models import Error, ErrorResult
import requests
import logging
import os.path
import six
from . import fresh_operation


class Attachments(object):

    """Class for handling Attachments operations."""

    def __init__(self, smartsheet_obj):
        """Init Attachments with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def attach_file_to_comment(self, sheet_id, comment_id, _file):
        """Add a file to a Comment.

        Args:
            sheet_id (int): Sheet ID
            comment_id (int): Comment ID
            _file (file): String or file stream object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'comment_id',
                                               '_file']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('attach_file_to_comment')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/comments/' + str(
            comment_id) + '/attachments'
        _op['files'] = {}
        _op['files']['file'] = _file

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def attach_file_to_row(self, sheet_id, row_id, _file):
        """Add a file to the row.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            _file (file): String or file stream object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'row_id', '_file']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('attach_file_to_row')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/attachments'
        _op['files'] = {}
        _op['files']['file'] = _file

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def attach_file_to_sheet(self, sheet_id, _file):
        """Attach a file to the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            _file (file): String or file stream object.

        Returns:
            Result
        """
        _op = fresh_operation('attach_file_to_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments'
        _op['files'] = {}
        _op['files']['file'] = _file

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def attach_new_version(self, sheet_id, attachment_id, _file):
        """Upload a new version of a file to a Sheet or Row.

        Args:
            sheet_id (int): Sheet ID
            attachment_id (int): Attachment ID
            _file (file): String or file stream object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'attachment_id',
                                               '_file']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('attach_new_version')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments/' + str(
            attachment_id) + '/versions'
        _op['files'] = {}
        _op['files']['file'] = _file

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def attach_url_to_comment(self, sheet_id, comment_id, attachment_obj):
        """Add a URL to a Comment.

        Attachment object for this request should be limited to the
        following attributes: name, description, url, attachmentType,
        attachmentSubType.

        The URL and attachmentType can be any of the following:

        A Normal URL. attachmentType is LINK.

        A Google Drive URL. attachmentType is LINK. Supports
        attachmentSubType values of DOCUMENT, SPREADSHEET, PRESENTATION,
        PDF and DRAWING.

        A Box.com URL. attachmentType is BOX_COM.

        A Dropbox URL. attachmentType is DROPBOX.

        An Evernote URL. attachmentType is EVERNOTE.

        An Egnyte URL. attachmentType is EGNYTE. Supports attachmentSubType
        of FOLDER.

        Args:
            sheet_id (int): Sheet ID
            comment_id (int): Comment ID
            attachment_obj (Attachment): Attachment object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'comment_id',
                                               'attachment_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('attach_url_to_comment')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/comments/' + str(
            comment_id) + '/attachments'
        _op['json'] = attachment_obj
        # filter before we go
        _op['json'].pre_request_filter = 'attach_url_to_comment'

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def attach_url_to_row(self, sheet_id, row_id, attachment_obj):
        """Add a URL to a Row.

        Attachment object for this request should be limited to the
        following attributes: name, description, url, attachmentType,
        attachmentSubType.

        The URL and attachmentType can be any of the following:

        A Normal URL. attachmentType is LINK.

        A Google Drive URL. attachmentType is LINK. Supports
        attachmentSubType values of DOCUMENT, SPREADSHEET, PRESENTATION,
        PDF and DRAWING.

        A Box.com URL. attachmentType is BOX_COM.

        A Dropbox URL. attachmentType is DROPBOX.

        An Evernote URL. attachmentType is EVERNOTE.

        An Egnyte URL. attachmentType is EGNYTE. Supports attachmentSubType
        of FOLDER.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            attachment_obj (Attachment): Attachment object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'row_id',
                                               'attachment_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('attach_url_to_row')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/attachments'
        _op['json'] = attachment_obj
        # filter before we go
        _op['json'].pre_request_filter = 'attach_url_to_row'

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def attach_url_to_sheet(self, sheet_id, attachment_obj):
        """Add a URL to a Sheet.

        Attachment object for this request should be limited to the
        following attributes: name, description, url, attachmentType,
        attachmentSubType.

        The URL and attachmentType can be any of the following:

        A Normal URL. attachmentType is LINK.

        A Google Drive URL. attachmentType is LINK. Supports
        attachmentSubType values of DOCUMENT, SPREADSHEET, PRESENTATION,
        PDF and DRAWING.

        A Box.com URL. attachmentType is BOX_COM.

        A Dropbox URL. attachmentType is DROPBOX.

        An Evernote URL. attachmentType is EVERNOTE.

        An Egnyte URL. attachmentType is EGNYTE. Supports attachmentSubType
        of FOLDER.

        Args:
            sheet_id (int): Sheet ID
            attachment_obj (Attachment): Attachment object.

        Returns:
            Result
        """
        _op = fresh_operation('attach_url_to_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments'
        _op['json'] = attachment_obj
        # filter before we go
        _op['json'].pre_request_filter = 'attach_url_to_sheet'

        expected = ['Result', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_attachment(self, sheet_id, attachment_id):
        """Delete the specified Attachment.

        Args:
            sheet_id (int): Sheet ID
            attachment_id (int): Attachment ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_attachment')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments/' + str(
            attachment_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_attachment_versions(self, sheet_id, attachment_id):
        """Delete all versions of the specified Attachment.

        Delete all versions of the attachment corresponding to the
        specified Attachment ID.

        Args:
            sheet_id (int): Sheet ID
            attachment_id (int): Attachment ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_attachment_versions')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments/' + str(
            attachment_id) + '/versions'

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_attachment(self, sheet_id, attachment_id):
        """Fetch the specified Attachment.

        Args:
            sheet_id (int): Sheet ID
            attachment_id (int): Attachment ID

        Returns:
            Attachment
        """
        _op = fresh_operation('get_attachment')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments/' + str(
            attachment_id)

        expected = 'Attachment'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_all_attachments(self, sheet_id, page_size=100, page=1,
                             include_all=False):
        """Get a list of Attachments for a Sheet.

        Get a list of all Attachments for the specified Sheet,
        including Sheet, Row, and Discussion level Attachments.

        Args:
            sheet_id (int): Sheet ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_all_attachments')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_attachment_versions(self, sheet_id, attachment_id,
                                 page_size=100, page=1, include_all=False):
        """Get a list of versions for an Attachment.

        Get a list of all versions of the given Attachment ID, in
        order from newest to oldest.

        Args:
            sheet_id (int): Sheet ID
            attachment_id (int): Attachment ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_attachment_versions')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/attachments/' + str(
            attachment_id) + '/versions'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_discussion_attachments(self, sheet_id, discussion_id,
                                    page_size=100, page=1, include_all=False):
        """Get a list of Attachments for the Sheet Discussion.

        Get a list of all Attachments for the specified Sheet
        Discussion.

        Args:
            sheet_id (int): Sheet ID
            discussion_id (int): Discussion ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_discussion_attachments')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/discussions/' + str(
            discussion_id) + '/attachments'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_row_attachments(self, sheet_id, row_id, page_size=100, page=1,
                             include_all=False):
        """Get a list of all Attachments for the specified Sheet Row.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_row_attachments')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/attachments'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Attachment']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def download_attachment(self, attachment_obj, download_path,
                            alternate_file_name=None):
        """Download the specified attachment as a file.

        This method wraps the Requests module and performs
        a streaming file download to the specified location.

        Args:
            attachment_obj (Attachment): Attachment object
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            DownloadedFile
        """
        if not os.path.isdir(download_path):
            raise ValueError('download_path must be a directory.')

        resp = requests.get(
            attachment_obj.url,
            stream=True
        )

        if 200 <= resp.status_code <= 299:
            response = DownloadedFile({
                'result_code': 0,
                'message': 'SUCCESS',
                'resp': resp,
                'filename': attachment_obj.name,
                'download_directory': download_path
            })

            if alternate_file_name is not None:
                response.filename = alternate_file_name

            response.save_to_file()
            return response
        else:
            return Error({
                'result': ErrorResult({
                    'status_code': resp.status_code
                }),
                'request_response': resp
            })
