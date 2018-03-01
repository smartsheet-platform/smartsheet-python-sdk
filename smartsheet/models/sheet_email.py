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

from .email import Email
from .enums import SheetEmailFormat
from .format_details import FormatDetails
from ..types import *
from ..util import serialize
from ..util import deserialize


class SheetEmail(Email):

    """Smartsheet SheetEmail data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetEmail model."""
        super(SheetEmail, self).__init__(None, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._format_ = EnumeratedValue(SheetEmailFormat)
        self._format_details = TypedObject(FormatDetails)

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self.format_
        else:
            raise AttributeError(key)
        
    def __setattr__(self, key, value):
        if key == 'format':
            self.format_ = value
        else:
            super(SheetEmail, self).__setattr__(key, value)

    @property
    def format_(self):
        return self._format_

    @format_.setter
    def format_(self, value):
        self._format_.set(value)

    @property
    def format_details(self):
        return self._format_details.value

    @format_details.setter
    def format_details(self, value):
        self._format_details.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
