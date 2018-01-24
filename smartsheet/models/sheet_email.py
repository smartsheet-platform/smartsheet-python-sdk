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

import six
import json

from .email import Email
from .format_details import FormatDetails
from .recipient import Recipient
from ..types import TypedList
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

        self.allowed_values = {
            '_format': [
                'PDF',
                'PDF_GANTT',
                'EXCEL']}

        self._format_ = None
        self._format_details = None

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
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_format']:
                raise ValueError(
                    ("`{0}` is an invalid value for SheetEmail`_format`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_format']))
            self._format_ = value

    @property
    def format_details(self):
        return self._format_details

    @format_details.setter
    def format_details(self, value):
        if isinstance(value, FormatDetails):
            self._format_details = value
        else:
            self._format_details = FormatDetails(value, self._base)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
