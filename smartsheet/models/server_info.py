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

from .format_tables import FormatTables
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class ServerInfo(object):

    """Smartsheet ServerInfo data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ServerInfo model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._formats = None
        self._supported_locales = TypedList(str)

        if props:
            # account for alternate variable names from raw API response
            if 'formats' in props:
                self.formats = props['formats']
            if 'supportedLocales' in props:
                self.supported_locales = props[
                    'supportedLocales']
            if 'supported_locales' in props:
                self.supported_locales = props[
                    'supported_locales']
        # requests package Response object
        self.request_response = None

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, value):
        if isinstance(value, FormatTables):
            self._formats = value
        else:
            self._formats = FormatTables(value, self._base)

    @property
    def supported_locales(self):
        return self._supported_locales

    @supported_locales.setter
    def supported_locales(self, value):
        if isinstance(value, list):
            self._supported_locales.purge()
            self._supported_locales.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._supported_locales.purge()
            self._supported_locales = value.to_list()
        elif isinstance(value, str):
            self._supported_locales.purge()
            self._supported_locales.append(value)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'formats': prep(self._formats),
            'supportedLocales': prep(self._supported_locales)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
