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

from .models.column import Column
from .models.row import Row
from .types import TypedList
import logging
import os.path
from datetime import datetime
from .util import deprecated
from . import fresh_operation


class Sheets(object):

    """Class for handling Sheets operations."""

    def __init__(self, smartsheet_obj):
        """Init Sheets with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_columns(self, sheet_id, list_of_columns):
        """Insert one or more Columns into the specified Sheet

        Args:
            sheet_id (int): Sheet ID
            list_of_columns (list[Column]): One or more
                Column objects.

        Returns:
            Result
        """
        if isinstance(list_of_columns, (dict, Column)):
            arg_value = list_of_columns
            list_of_columns = TypedList(Column)
            list_of_columns.append(arg_value)

        _op = fresh_operation('add_columns')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/columns'
        _op['json'] = list_of_columns
        # filter before we go
        for item in _op['json']:
            item.pre_request_filter = 'add_columns'

        expected = ['Result', 'Column']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_rows(self, sheet_id, list_of_rows):
        """Insert one or more Rows into the specified Sheet.

        If multiple rows are specified in the request, all rows
        must be inserted at the same location (i.e. the **toTop**,
        **toBottom**, **parentId**, **siblingId**, and **above** attributes
        must be the same for all rows in the request.)

        In a parent row, values of the following fields will be
        auto-calculated based upon values in the child rows (and therefore
        cannot be updated using the API): Start Date, End Date, Duration, %
        Complete.

        Args:
            sheet_id (int): Sheet ID
            list_of_rows (list[Row]): An array of Row objects with the following attributes:

               One or more location-specifier attributes (optional)

               format (optional)

               expanded (optional)

               locked (optional)

               A cells attribute set to an array of Cell objects.
               To insert an empty row, set the cells attribute to empty or null.
               Each Cell object may contain the following attributes:

                   columnId (required)

                   value (required)

                   strict (optional)

                   format (optional)

                   hyperlink (optional)

        Returns:
            Result
        """
        if isinstance(list_of_rows, (dict, Row)):
            arg_value = list_of_rows
            list_of_rows = TypedList(Row)
            list_of_rows.append(arg_value)

        _op = fresh_operation('add_rows')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows'
        _op['json'] = list_of_rows
        # filter before we go
        for item in _op['json']:
            item.pre_request_filter = 'add_rows'

        expected = ['Result', 'Row']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_rows_with_partial_success(self, sheet_id, list_of_rows):
        """Insert one or more Rows into the specified Sheet.

        If multiple rows are specified in the request, all rows
        must be inserted at the same location (i.e. the **toTop**,
        **toBottom**, **parentId**, **siblingId**, and **above** attributes
        must be the same for all rows in the request.)

        In a parent row, values of the following fields will be
        auto-calculated based upon values in the child rows (and therefore
        cannot be updated using the API): Start Date, End Date, Duration, %
        Complete.

        Args:
            sheet_id (int): Sheet ID
            list_of_rows (list[Row]): An array of Row objects with the following attributes:

                One or more location-specifier attributes (optional)

                format (optional)

                expanded (optional)

                locked (optional)

                A cells attribute set to an array of Cell objects.
                To insert an empty row, set the cells attribute to empty or null.
                Each Cell object may contain the following attributes:

                    columnId (required)

                    value (required)

                    strict (optional)

                    format (optional)

                    hyperlink (optional)

        Returns:
            Result
        """
        if isinstance(list_of_rows, (dict, Row)):
            arg_value = list_of_rows
            list_of_rows = TypedList(Row)
            list_of_rows.append(arg_value)

        _op = fresh_operation('add_rows')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows'
        _op['json'] = list_of_rows
        _op['query_params']['allowPartialSuccess'] = 'true'

        # filter before we go
        for item in _op['json']:
            item.pre_request_filter = 'add_rows'

        expected = ['BulkItemResult', 'Row']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def copy_rows(self, sheet_id, copy_or_move_row_directive_obj,
                  include=None, ignore_rows_not_found=False):
        """Copies Row(s) from the specified Sheet to the bottom of another
        Sheet.

        Args:
            sheet_id (int): Sheet ID
            copy_or_move_row_directive_obj
                (CopyOrMoveRowDirective): CopyOrMoveRowDirective object.
            include (list[str]): A comma-separated list of
                row elements to copy in addition to the cell data. Valid
                list values: attachments, discussions, children, all.
            ignore_rows_not_found (bool): If set to `true`,
                specifying row ids that do not exist within the source sheet
                will not cause an error response. If omitted or set to false
                (the default), specifying row ids that do not exist within
                the source sheet will cause an error response (and no rows
                will be altered).

        Returns:
            CopyOrMoveRowResult
        """
        _op = fresh_operation('copy_rows')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/copy'
        _op['query_params']['include'] = include
        _op['query_params']['ignoreRowsNotFound'] = ignore_rows_not_found
        _op['json'] = copy_or_move_row_directive_obj

        expected = 'CopyOrMoveRowResult'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def copy_sheet(self, sheet_id, container_destination_obj,
                   include=None):
        """Creates a copy of the specified Sheet

        Args:
            sheet_id (int): Sheet ID
            container_destination_obj
                (ContainerDestination): Container Destination object.
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: data, attachments, discussions, cellLinks, forms,
                all.

        Returns:
            Result
        """
        _op = fresh_operation('copy_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/copy'
        _op['query_params']['include'] = include
        _op['json'] = container_destination_obj

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_column(self, sheet_id, column_id):
        """Delete the specified Column.

        Args:
            sheet_id (int): Sheet ID
            column_id (int): Column ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_column')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/columns/' + str(
            column_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_rows(self, sheet_id, ids, ignore_rows_not_found=False):
        """Deletes one or more Row(s) from the specified Sheeet.

        Args:
            sheet_id (int): Sheet ID
            ids (list[int]): a comma-separated list of
                object IDs representing the items to work on.
            ignore_rows_not_found (bool): If set to `true`,
                specifying row ids that do not exist within the source sheet
                will not cause an error response. If omitted or set to false
                (the default), specifying row ids that do not exist within
                the source sheet will cause an error response (and no rows
                will be altered).

        Returns:
            Result
        """
        _op = fresh_operation('delete_rows')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows'
        _op['query_params']['ids'] = ids
        _op['query_params']['ignoreRowsNotFound'] = ignore_rows_not_found

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_share(self, sheet_id, share_id):
        """Delete the specified Share.

        Args:
            sheet_id (int): Sheet ID
            share_id (str): Share ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_share')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/shares/' + str(share_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_sheet(self, sheet_id):
        """Delete the specified Sheet.

        Args:
            sheet_id (int): Sheet ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_sheet')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_column(self, sheet_id, column_id, include=None):
        """Get the specified Column.

        Args:
            sheet_id (int): Sheet ID
            column_id (int): Column ID
            include (str): When specified with a value of
                'filters', response will include the Filter the user has
                applied (if any).

        Returns:
            Column
        """
        _op = fresh_operation('get_column')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/columns/' + str(
            column_id)
        _op['query_params']['include'] = include

        expected = 'Column'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_columns(self, sheet_id, include=None, page_size=100, page=1,
                    include_all=False):
        """Get all columns belonging to the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            include (str): When specified with a value of
                'filters', response will include the Filter the user has
                applied (if any).
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('get_columns')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/columns'
        _op['query_params']['include'] = include
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'Column']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_publish_status(self, sheet_id):
        """Get the Publish status of the Sheet.

        Get the status of the Publish settings of the Sheet,
        including URLs of any enabled publishings.

        Args:
            sheet_id (int): Sheet ID

        Returns:
            SheetPublish
        """
        _op = fresh_operation('get_publish_status')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/publish'

        expected = 'SheetPublish'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_row(self, sheet_id, row_id, include=None, exclude=None):
        """Get the specified Row of the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            include (list[str]): A comma-separated list of
                flags that indicate additional attributes to be included in
                each Row object within the response. Valid list values:
                discussions, attachments, format, filters, columnType,
                rowPermalink, rowWriterInfo.
            exclude (str): Response will not include cells
                that have never contained any data.

        Returns:
            Row
        """
        _op = fresh_operation('get_row')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(row_id)
        _op['query_params']['include'] = include
        _op['query_params']['exclude'] = exclude

        expected = 'Row'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_share(self, sheet_id, share_id):
        """Get the specified Share.

        Args:
            sheet_id (int): Sheet ID
            share_id (str): Share ID

        Returns:
            Share
        """
        _op = fresh_operation('get_share')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/shares/' + str(share_id)

        expected = 'Share'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_sheet(self, sheet_id, include=None, exclude=None, row_ids=None,
                  row_numbers=None, column_ids=None, page_size=100, page=1):
        """Get the specified Sheet.

        Get the specified Sheet. Returns the Sheet, including Rows,
        and optionally populated with Discussion and Attachment
        objects.

        Args:
            sheet_id (int): Sheet ID
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: attachments, discussions, format, filters,
                ownerInfo, source, rowWriterInfo.
            exclude (str): Response will not include cells
                that have never contained any data.
            row_ids (list[int]): comma-separated list of Row
                IDs on which to filter the rows included in the result.
            row_numbers (list[int]): comma-separated list of
                Row numbers on which to filter the rows included in the
                result. Non-existent row numbers are ignored.
            column_ids (list[int]): comma-separated list of
                Column IDs. The response will contain only the specified
                columns in the 'columns' array, and individual rows' 'cells'
                array will only contain cells in the specified columns.
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.

        Returns:
            Sheet
        """
        _op = fresh_operation('get_sheet')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id)
        _op['query_params']['include'] = include
        _op['query_params']['exclude'] = exclude
        _op['query_params']['rowIds'] = row_ids
        _op['query_params']['rowNumbers'] = row_numbers
        _op['query_params']['columnIds'] = column_ids
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page

        expected = 'Sheet'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_sheet_as_csv(self, sheet_id, download_path,
                         alternate_file_name=None):
        """Get the specified Sheet as a CSV file.

        Args:
            sheet_id (int): Sheet ID
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            DownloadedFile
        """
        if not os.path.isdir(download_path):
            raise ValueError('download_path must be a directory.')

        _op = fresh_operation('get_sheet_as_csv')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id)
        _op['header_params']['Accept'] = 'text/csv'
        _op['dl_path'] = download_path

        expected = 'DownloadedFile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def get_sheet_as_excel(self, sheet_id, download_path,
                           alternate_file_name=None):
        """Get the specified Sheet as an Excel .xls file.

        Args:
            sheet_id (int): Sheet ID
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            DownloadedFile
        """
        if not os.path.isdir(download_path):
            raise ValueError('download_path must be a directory.')

        _op = fresh_operation('get_sheet_as_excel')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id)
        _op['header_params']['Accept'] = 'application/vnd.ms-excel'
        _op['dl_path'] = download_path

        expected = 'DownloadedFile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def get_sheet_as_pdf(self, sheet_id, download_path, paper_size=None,
                         alternate_file_name=None):
        """Get the specified Sheet as a PDF file.

        Args:
            sheet_id (int): Sheet ID
            download_path (str): Directory path on local
                machine to save file.
            paper_size (str): Applies to PDF only. One of:
                LETTER, LEGAL, WIDE, ARCHD, A4, A3, A2, A1, A0
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            DownloadedFile
        """
        if not os.path.isdir(download_path):
            raise ValueError('download_path must be a directory.')

        _op = fresh_operation('get_sheet_as_pdf')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id)
        _op['header_params']['Accept'] = 'application/pdf'
        _op['query_params']['paperSize'] = paper_size
        _op['dl_path'] = download_path

        expected = 'DownloadedFile'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def get_sheet_version(self, sheet_id):
        """Get the Sheet version without loading the entire Sheet.

        Args:
            sheet_id (int): Sheet ID

        Returns:
            Version
        """
        _op = fresh_operation('get_sheet_version')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/version'

        expected = 'Version'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    @deprecated
    def list_org_sheets(self):
        """Get a list of all Sheets owned by an organization.

        Get the list of all Sheets owned by the members of the
        account (organization).
        Returns:
            IndexResult
        """
        _op = fresh_operation('list_org_sheets')
        _op['method'] = 'GET'
        _op['path'] = '/users/sheets'

        expected = ['IndexResult', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_shares(self, sheet_id, page_size=100, page=1,
                    include_all=False, include_workspace_shares=False):
        """Get the list of all Users and Groups to whom the specified Sheet is
        shared, and their access level.

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
        _op = fresh_operation('list_shares')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/shares'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if include_workspace_shares:
            _op['query_params']['include'] = 'workspaceShares'

        expected = ['IndexResult', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_sheets(self, include=None, page_size=100, page=1,
                    include_all=False, modified_since=None):
        """Get the list of all Sheets the User has access to, in alphabetical
        order, by name.

        Args:
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list
                values: ownerInfo, source.
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_sheets')
        _op['method'] = 'GET'
        _op['path'] = '/sheets'
        _op['query_params']['include'] = include
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        if isinstance(modified_since, datetime):
            _op['query_params']['modifiedSince'] = modified_since.isoformat()

        expected = ['IndexResult', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def move_rows(self, sheet_id, copy_or_move_row_directive_obj,
                  include=None, ignore_rows_not_found=False):
        """Moves Row(s) to the bottom of another Sheet.

        Up to 5,000 row IDs can be specified in the request, but if
        the total number of rows in the destination Sheet after the move
        exceeds the Smartsheet row limit, an error response will be
        returned.

        Any child rows of the rows specified in the request will also be
        moved. Parent-child relationships amongst rows will be preserved
        within the destination Sheet.

        Args:
            sheet_id (int): Sheet ID
            copy_or_move_row_directive_obj
                (CopyOrMoveRowDirective): CopyOrMoveRowDirective object.
            include (list[str]): A comma-separated list of
                row elements to move in addition to the cell data. Valid
                list values: attachments, discussions.
            ignore_rows_not_found (bool): If set to `true`,
                specifying row ids that do not exist within the source sheet
                will not cause an error response. If omitted or set to false
                (the default), specifying row ids that do not exist within
                the source sheet will cause an error response (and no rows
                will be altered).

        Returns:
            CopyOrMoveRowResult
        """
        _op = fresh_operation('move_rows')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/move'
        _op['query_params']['include'] = include
        _op['query_params']['ignoreRowsNotFound'] = ignore_rows_not_found
        _op['json'] = copy_or_move_row_directive_obj

        expected = 'CopyOrMoveRowResult'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def move_sheet(self, sheet_id, container_destination_obj):
        """Move the specified Sheet to a new location.

        Args:
            sheet_id (int): Sheet ID
            container_destination_obj
                (ContainerDestination): Container Destination object.

        Returns:
            Result
        """
        _op = fresh_operation('move_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/move'
        _op['json'] = container_destination_obj
        # filter before we go
        _op['json'].pre_request_filter = 'move_sheet'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def search_sheet(self, sheet_id, query):
        """Search the specified Sheet for the specified text.

        Args:
            sheet_id (int): Sheet ID
            query (str): Text with which to perform the
                search.

        Returns:
            SearchResult
        """
        _op = fresh_operation('search_sheet')
        _op['method'] = 'GET'
        _op['path'] = '/search/sheets/' + str(sheet_id)
        _op['query_params']['query'] = query

        expected = 'SearchResult'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def send_rows(self, sheet_id, multi_row_email_obj):
        """Send one or more rows via email

        Args:
            sheet_id (int): Sheet ID
            multi_row_email_obj (MultiRowEmail):
                MultiRowEmail object.

        Returns:
            Result
        """
        _op = fresh_operation('send_rows')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/emails'
        _op['json'] = multi_row_email_obj

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def send_sheet(self, sheet_id, sheet_email_obj):
        """Sends the sheet as an attachment via email to the designated
        recipients.

        Args:
            sheet_id (int): Sheet ID
            sheet_email_obj (SheetEmail): SheetEmail object.

        Returns:
            Result
        """
        _op = fresh_operation('send_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/emails'
        _op['json'] = sheet_email_obj

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    @deprecated
    def send_update_request(self, sheet_id, multi_row_email_obj):
        """Create an Update Request for the specified Row(s) within the
        Sheet. An email notification (containing a link to the
        update request) will be asynchronously send to the specified
        recipient(s).

        Args:
            sheet_id (int): Sheet ID
            multi_row_email_obj (MultiRowEmail):
                MultiRowEmail object.

        Returns:
            Result
        """
        _op = fresh_operation('send_update_request')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/updaterequests'
        _op['json'] = multi_row_email_obj

        expected = ['Result', 'UpdateRequest']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def set_publish_status(self, sheet_id, sheet_publish_obj):
        """Set the publish status of the Sheet and returns the new status,
        including the URLs of any enabled publishings.

        Args:
            sheet_id (int): Sheet ID
            sheet_publish_obj (SheetPublish): SheetPublish
                object.

        Returns:
            Result
        """
        attributes = ['read_only_lite_enabled', 'read_only_full_enabled',
                      'read_write_enabled', 'ical_enabled']

        fetch_first = False
        # check for incompleteness, fill in from current status if necessary
        for attribute in attributes:
            val = getattr(sheet_publish_obj, attribute, None)
            if val is None:
                fetch_first = True
                break

        if fetch_first:
            current_status = self.get_publish_status(sheet_id).to_dict()
            current_status.update(sheet_publish_obj.to_dict())
            sheet_publish_obj = self._base.models.SheetPublish(current_status)

        _op = fresh_operation('set_publish_status')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/publish'
        _op['json'] = sheet_publish_obj
        # filter before we go
        _op['json'].pre_request_filter = 'set_publish_status'

        expected = ['Result', 'SheetPublish']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def share_sheet(self, sheet_id, share_obj, send_email=False):
        """Share the specified Sheet.

        Share the specified Sheet with the specified Users and
        Groups.

        Args:
            sheet_id (int): Sheet ID
            share_obj (Share): Share object.
            send_email (bool): Either true or false to
                indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Result
        """
        _op = fresh_operation('share_sheet')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/shares'
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = share_obj
        # filter before we go
        _op['json'].pre_request_filter = 'share_sheet'

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_column(self, sheet_id, column_id, column_obj):
        """Update properties of the specified Column.

        Args:
            sheet_id (int): Sheet ID
            column_id (int): Column ID
            column_obj (Column): A Column object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'column_id',
                                               'column_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        if isinstance(column_obj, dict):
            column_obj = Column(column_obj)

        _op = fresh_operation('update_column')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/columns/' + str(
            column_id)
        _op['json'] = column_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_column'

        expected = ['Result', 'Column']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_rows(self, sheet_id, list_of_rows):
        """Update properties of the specified Row.

        Updates cell values in the specified row(s),
        expands/collapses the specified row(s), and/or modifies the
        position of the specified rows (including indenting/outdenting).

        If a row's position is updated, all child rows are moved with the
        row.

        In a parent row, values of the following fields are auto-calculated
        based upon values in the child rows (and therefore cannot be
        updated using the API): Start Date, End Date, Duration, % Complete.

        Args:
            sheet_id (int): Sheet ID
            list_of_rows (list[Row]): Array containing one
                or more Row objects.

        Returns:
            Result
        """
        _op = fresh_operation('update_rows')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows'
        _op['json'] = list_of_rows
        # filter before we go
        for item in _op['json']:
            item.pre_request_filter = 'update_rows'

        expected = ['Result', 'Row']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_rows_with_partial_success(self, sheet_id, list_of_rows):
        """Update properties of the specified Row(s).

        Updates cell values in the specified row(s),
        expands/collapses the specified row(s), and/or modifies the
        position of the specified rows (including indenting/outdenting).

        If a row's position is updated, all child rows are moved with the
        row.

        In a parent row, values of the following fields are auto-calculated
        based upon values in the child rows (and therefore cannot be
        updated using the API): Start Date, End Date, Duration, % Complete.

        Args:
            sheet_id (int): Sheet ID
            list_of_rows (list[Row]): Array containing one
                or more Row objects.

        Returns:
            Result
        """
        _op = fresh_operation('update_rows')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows'
        _op['json'] = list_of_rows
        _op['query_params']['allowPartialSuccess'] = 'true'

        # filter before we go
        for item in _op['json']:
            item.pre_request_filter = 'update_rows'

        expected = ['BulkItemResult', 'Row']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_share(self, sheet_id, share_id, share_obj):
        """Update the access level of a User or Group for the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            share_id (str): Share ID
            share_obj (Share): Share object.

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'share_id',
                                               'share_obj']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('update_share')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/shares/' + str(share_id)
        _op['json'] = share_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_share'

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_sheet(self, sheet_id, sheet_obj):
        """Updates the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            sheet_obj (Sheet): Sheet object.

        Returns:
            Result
        """
        _op = fresh_operation('update_sheet')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id)
        _op['json'] = sheet_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_sheet'

        expected = ['Result', 'Sheet']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_update_requests(self, sheet_id, page_size=100, page=1,
                        include_all=False):
        """Get the list of all Sheet UpdateRequests.

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
        _op = fresh_operation('list_update_requests')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/updaterequests'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'UpdateRequest']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_update_request(self, sheet_id, update_request_id):
        """Get the UpdateRequest for Sheet that has a future schedule.

        Args:
            sheet_id (int): Sheet ID
            update_request_id (int): UpdateRequest ID

        Returns:
            UpdateRequest
        """
        _op = fresh_operation('get_update_request')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/updaterequests/' + str(update_request_id)

        expected = 'UpdateRequest'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_update_request(self, sheet_id, update_request_obj):
        """Creates an UpdateRequest for the specified Rows(s) within the Sheet.

        Args:
            sheet_id (int): Sheet ID
            update_request_obj (UpdateRequest): UpdateRequest object

        Returns:
            Result
        """
        _op = fresh_operation('create_update_request')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/updaterequests'
        _op['json'] = update_request_obj
        # filter before we go
        _op['json'].pre_request_filter = 'create_update_request'

        expected = ['Result', 'UpdateRequest']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_update_request(self, sheet_id, update_request_id):
        """Deletes an UpdateRequest for the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            update_request_id (int): UpdateRequest ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_update_request')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/updaterequests/' + str(update_request_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_update_request(self, sheet_id, update_request_obj):
        """Updates an UpdateRequest for the specified Rows(s) within the Sheet.

        Args:
            sheet_id (int): Sheet ID
            update_request_obj (UpdateRequest): UpdateRequest object

        Returns:
            Result
        """
        _op = fresh_operation('create_update_request')
        _op['method'] = 'PUT'
        _op['path'] = '/sheets/' + str(sheet_id) + '/updaterequests/' + str(update_request_obj.id)
        _op['json'] = update_request_obj
        # filter before we go
        _op['json'].pre_request_filter = 'update_update_request'

        expected = ['Result', 'UpdateRequest']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_sent_update_requests(self, sheet_id, page_size=100, page=1,
                        include_all=False):
        """Get the list of all Sent UpdateRequests.

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
        _op = fresh_operation('list_update_requests')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/sentupdaterequests'
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'SentUpdateRequest']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_sent_update_request(self, sheet_id, sent_update_request_id):
        """Get the SentUpdateRequest for Sheet.

        Args:
            sheet_id (int): Sheet ID
            sent_update_request_id (int): SentUpdateRequest ID

        Returns:
            UpdateRequest
        """
        _op = fresh_operation('get_sent_update_request')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/sentupdaterequests/' + str(sent_update_request_id)

        expected = 'SentUpdateRequest'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_sent_update_request(self, sheet_id, sent_update_request_id):
        """Deletes a SentUpdateRequest for the specified Sheet.

        Args:
            sheet_id (int): Sheet ID
            sent_update_request_id (int): SentUpdateRequest ID

        Returns:
            Result
        """
        _op = fresh_operation('delete_update_request')
        _op['method'] = 'DELETE'
        _op['path'] = '/sheets/' + str(sheet_id) + '/sentupdaterequests/' + str(sent_update_request_id)

        expected = 'Result'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_column_by_title(self, sheet_id, title, include=None):
        """For those times when you don't know the Column Id.

        Note: returns the first matching title found.

        Args:
            include (str): When specified with a value of
                'filters', response will include the Filter the user has
                applied (if any).
        """
        all_columns = self.get_columns(sheet_id, include_all=True)
        for _c in all_columns.data:
            if _c.title == title:
                return self.get_column(sheet_id, _c.id, include=include)
        return False

    def get_sheet_by_name(self, name, include=None, exclude=None,
                          row_ids=None, row_numbers=None, column_ids=None,
                          page_size=100, page=1):
        """For those times when you don't know the Sheet Id.

        Note: returns the first matching name found.

        Args:
            See arguments for get_sheet()
        """
        all_sheets = self.list_sheets(include_all=True)
        for _s in all_sheets.data:
            if _s.name == name:
                return self.get_sheet(_s.id, include=include,
                                      exclude=exclude, row_ids=row_ids,
                                      row_numbers=row_numbers,
                                      column_ids=column_ids,
                                      page_size=page_size, page=page)
        return False
