# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
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

import contextlib
import os.path
import six
import json

from ..util import serialize
from ..util import deserialize


class DownloadedFile(object):

    """Smartsheet DownloadedFile data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DownloadedFile model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._download_directory = None
        self._filename = None
        self._message = None
        self._resp = None
        self._result_code = None

        if props:
            deserialize(self, props)

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

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
