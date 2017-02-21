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

import logging
import os.path
from datetime import datetime
from . import fresh_operation


class Reports(object):

    """Class for handling Reports operations."""

    def __init__(self, smartsheet_obj):
        """Init Reports with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def delete_share(self, report_id, share_id):
        """Deletes the specified Share

        Args:
            report_id (int): Report ID
            share_id (str): Share ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_share')
        _op['method'] = 'DELETE'
        _op['path'] = '/reports/' + str(report_id) + '/shares/' + str(
            share_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_report(self, report_id, page_size=100, page=1, include=None):
        """Get the specified Report, including one page of Rows.

        Get the specified Report, including one page of Rows, and
        optionally populated with Discussions, Attachments, and
        Source Sheets.

        Args:
            report_id (int): Report ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: discussions, attachments, format, sourceSheets.

        Returns:
            Report
        """
        _op = fresh_operation('get_report')
        _op['method'] = 'GET'
        _op['path'] = '/reports/' + str(report_id)
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['include'] = include

        expected = 'Report'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_report_as_csv(self, report_id, download_path,
                          alternate_file_name=None):
        """Get the specified Report as a CSV file.

        Args:
            report_id (int): Report ID
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            DownloadedFile
        """
        if not os.path.isdir(download_path):
            raise ValueError('download_path must be a directory.')

        _op = fresh_operation('get_report_as_csv')
        _op['method'] = 'GET'
        _op['path'] = '/reports/' + str(report_id)
        _op['header_params']['Accept'] = 'text/csv'
        _op['dl_path'] = download_path

        expected = 'DownloadedFile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def get_report_as_excel(self, report_id, download_path,
                            alternate_file_name=None):
        """Get the specified Report as an Excel .xls document.

        Args:
            report_id (int): Report ID
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            DownloadedFile
        """
        if not os.path.isdir(download_path):
            raise ValueError('download_path must be a directory.')

        _op = fresh_operation('get_report_as_excel')
        _op['method'] = 'GET'
        _op['path'] = '/reports/' + str(report_id)
        _op['header_params']['Accept'] = 'application/vnd.ms-excel'
        _op['dl_path'] = download_path

        expected = 'DownloadedFile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def get_share(self, report_id, share_id):
        """Get the specified Share.

        Args:
            report_id (int): Report ID
            share_id (str): Share ID

        Returns:
            Share
        """
        _op = fresh_operation('get_share')
        _op['method'] = 'GET'
        _op['path'] = '/reports/' + str(report_id) + '/shares/' + str(
            share_id)

        expected = 'Share'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_reports(self, page_size=100, page=1, include_all=False, modified_since=None):
        """Get the list of all Reports accessible by the User.

        Get the list of all Reports that the User has access to, in
        alphabetical order by name.

        Args:
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_reports')
        _op['method'] = 'GET'
        _op['path'] = '/reports'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if isinstance(modified_since, datetime):
            _op['query_params']['modifiedSince'] = modified_since.isoformat()

        expected = ['IndexResult', 'Report']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_shares(self, report_id, page_size=100, page=1,
                    include_all=False, include_workspace_shares=False):
        """Get a list of all Users and Groups to whom the specified Report is
        shared, and their access level.

        Args:
            report_id (int): Report ID
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_shares')
        _op['method'] = 'GET'
        _op['path'] = '/reports/' + str(report_id) + '/shares'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if include_workspace_shares:
            _op['query_params']['include'] = 'workspaceShares'

        expected = ['IndexResult', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def send_report(self, report_id, sheet_email_obj):
        """Send the specified Report as a PDF attachment via email to the
        designated recipients.

        Args:
            report_id (int): Report ID
            sheet_email_obj (SheetEmail): SheetEmail object.

        Returns:
            Result
        """
        _op = fresh_operation('send_report')
        _op['method'] = 'POST'
        _op['path'] = '/reports/' + str(report_id) + '/emails'
        _op['json'] = sheet_email_obj

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def share_report(self, report_id, share_obj, send_email=False):
        """Shares a Report with the specified Users and Groups.

        Args:
            report_id (int): Report ID
            share_obj (Share): Share object.
            send_email (bool): Either true or false to
                indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Result
        """
        _op = fresh_operation('share_report')
        _op['method'] = 'POST'
        _op['path'] = '/reports/' + str(report_id) + '/shares'
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = share_obj

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_share(self, report_id, share_id, share_obj):
        """Update the access level of a User or Group for the specified Report

        Args:
            report_id (int): Report ID
            share_id (str): Share ID
            share_obj (Share): Share object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['report_id', 'share_id',
                                               'share_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('update_share')
        _op['method'] = 'PUT'
        _op['path'] = '/reports/' + str(report_id) + '/shares/' + str(
            share_id)
        _op['json'] = share_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_share'

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_publish_status(self, report_id):
        """Get the Publish status of the Report.

        Get the status of the Publish settings of the Report,
        including URLs of any enabled publishings.

        Args:
            report_id (int): Report ID

        Returns:
            ReportPublish
        """
        _op = fresh_operation('get_publish_status')
        _op['method'] = 'GET'
        _op['path'] = '/reports/' + str(report_id) + '/publish'

        expected = 'ReportPublish'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def set_publish_status(self, report_id, report_publish_obj):
        """Set the publish status of the Report and returns the new status,
        including the URLs of any enabled publishings.

        Args:
            report_id (int): Report ID
            report_publish_obj (ReportPublish): ReportPublish
                object.

        Returns:
            Result
        """
        attributes = ['read_only_full_enabled','read_only_full_accessible_by']

        fetch_first = False
        # check for incompleteness, fill in from current status if necessary
        for attribute in attributes:
            val = getattr(report_publish_obj, attribute, None)
            if val is None:
                fetch_first = True
                break

        if fetch_first:
            current_status = self.get_publish_status(report_id).to_dict()
            current_status.update(report_publish_obj.to_dict())
            report_publish_obj = self._base.models.ReportPublish(current_status)

        _op = fresh_operation('set_publish_status')
        _op['method'] = 'PUT'
        _op['path'] = '/reports/' + str(report_id) + '/publish'
        _op['json'] = report_publish_obj
        # filter before we go
        _op['json'].pre_request_filter = 'set_publish_status'

        expected = ['Result', 'ReportPublish']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response