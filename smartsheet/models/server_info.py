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
from ..types import *
from ..util import serialize
from ..util import deserialize


class ServerInfo(object):

    """Smartsheet ServerInfo data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ServerInfo model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._formats = TypedObject(FormatTables)
        self._supported_locales = TypedList(str)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None

    @property
    def formats(self):
        return self._formats.value

    @formats.setter
    def formats(self, value):
        self._formats.value = value

    @property
    def supported_locales(self):
        return self._supported_locales

    @supported_locales.setter
    def supported_locales(self, value):
        self._supported_locales.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
