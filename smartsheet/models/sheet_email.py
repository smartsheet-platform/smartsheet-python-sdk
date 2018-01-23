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
        super(SheetEmail, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.allowed_values = {
            '_format': [
                'PDF',
                'PDF_GANTT',
                'EXCEL']}

        self._cc_me = False
        self.__format = None
        self._format_details = None
        self._message = None
        self._send_to = TypedList(Recipient)
        self._subject = None

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
    def cc_me(self):
        return self._cc_me

    @cc_me.setter
    def cc_me(self, value):
        if isinstance(value, bool):
            self._cc_me = value

    @property
    def format_(self):
        return self.__format

    @format_.setter
    def format_(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_format']:
                raise ValueError(
                    ("`{0}` is an invalid value for SheetEmail`_format`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_format']))
            self.__format = value

    @property
    def format_details(self):
        return self._format_details

    @format_details.setter
    def format_details(self, value):
        if isinstance(value, FormatDetails):
            self._format_details = value
        else:
            self._format_details = FormatDetails(value, self._base)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, six.string_types):
            self._message = value

    @property
    def send_to(self):
        return self._send_to

    @send_to.setter
    def send_to(self, value):
        if isinstance(value, list):
            self._send_to.purge()
            self._send_to.extend([
                (Recipient(x, self._base)
                 if not isinstance(x, Recipient) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._send_to.purge()
            self._send_to = value.to_list()
        elif isinstance(value, Recipient):
            self._send_to.purge()
            self._send_to.append(value)

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, six.string_types):
            self._subject = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
