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

from ..types import TypedList
from ..util import prep
from datetime import datetime
import contextlib
import json
import logging
import os.path
import six

class DownloadedFile(object):

    """Smartsheet DownloadedFile data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DownloadedFile model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._download_directory = None
        self._filename = None
        self._message = None
        self._resp = None
        self._result_code = None

        if props:
            # account for alternate variable names from raw API response
            if 'downloadDirectory' in props:
                self.download_directory = props[
                    'downloadDirectory']
            if 'download_directory' in props:
                self.download_directory = props[
                    'download_directory']
            if 'filename' in props:
                self.filename = props['filename']
            if 'message' in props:
                self.message = props['message']
            if 'resp' in props:
                self.resp = props['resp']
            # read only
            if 'resultCode' in props:
                self.result_code = props['resultCode']
        # requests package Response object
        self.request_response = None

    @property
    def download_directory(self):
        return self._download_directory

    @download_directory.setter
    def download_directory(self, value):
        if isinstance(value, six.string_types):
            self._download_directory = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if isinstance(value, six.string_types):
            self._filename = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

    @property
    def resp(self):
        return self._resp

    @resp.setter
    def resp(self, value):
        if isinstance(value, object):
            self._resp = value
        else:
            self._resp = object(value, self._base)

    @property
    def result_code(self):
        return self._result_code

    @result_code.setter
    def result_code(self, value):
        if isinstance(value, six.integer_types):
            self._result_code = value

    def save_to_file(self, chunksize=2**16):
        download_path = os.path.join(self.download_directory, self.filename)
        with open(download_path, 'wb') as dlfile:
            with contextlib.closing(self.resp):
                for chunk in self.resp.iter_content(chunksize):
                    dlfile.write(chunk)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'downloadDirectory': prep(self._download_directory),
            'filename': prep(self._filename),
            'message': prep(self._message),
            'resp': prep(self._resp),
            'resultCode': prep(self._result_code)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
