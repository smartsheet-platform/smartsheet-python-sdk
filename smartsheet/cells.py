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
from . import fresh_operation
from io import BytesIO
import os


class Cells(object):

    """Class for handling Cells operations."""

    def __init__(self, smartsheet_obj):
        """Init Cells with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get_cell_history(self, sheet_id, row_id, column_id, include=None,
                         page_size=100, page=1, include_all=False):
        """Get the Cell modification history.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            column_id (int): Column ID
            include (str): When specified with a value of
                \"columnType\", response will include the columnType
                attribute for each Cell.
            page_size (int): The maximum number of items to
                return per page. Defaults to 100.
            page (int): Which page to return. Defaults to 1
                if not specified.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            IndexResult
        """
        if not all(val is not None for val in ['sheet_id', 'row_id',
                                               'column_id']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        _op = fresh_operation('get_cell_history')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(
            row_id) + '/columns/' + str(column_id) + '/history'
        _op['query_params']['include'] = include
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all

        expected = ['IndexResult', 'CellHistory']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_image_to_cell(self, sheet_id, row_id, column_id, file, file_type):
        """Uploads an image to the specified cell.

        Args:
            sheet_id (int): Sheet ID
            row_id (int): Row ID
            column_id (int): Column ID
            file (string): path to image file.
            file_type (string): content type of image file

        Returns:
            Result
        """
        if not all(val is not None for val in ['sheet_id', 'row_id',
                                               'column_id', 'file', 'file_type']):
            raise ValueError(
                ('One or more required values '
                 'are missing from call to ' + __name__))

        return self._attach_file_to_cell(sheet_id, row_id, column_id, file, file_type)

    def _attach_file_to_cell(self, sheet_id, row_id, column_id, file, file_type):

        _data = open(file, 'rb').read()

        _op = fresh_operation('attach_file_to_row')
        _op['method'] = 'POST'
        _op['path'] = '/sheets/' + str(sheet_id) + '/rows/' + str(row_id) + \
                      '/columns/' + str(column_id) + '/cellimages'
        _op['headers'] = {'content-type':file_type,
                          'content-disposition':'attachment; filename="' + file + '"'}
        _op['form_data'] = _data

        expected = 'Result'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response