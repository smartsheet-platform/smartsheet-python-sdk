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

from .email import Email
from .format_details import FormatDetails
from .recipient import Recipient
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class SheetEmail(Email):

    """Smartsheet SheetEmail data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetEmail model."""
        super(SheetEmail, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self.allowed_values = {
            '_format': [
                'PDF',
                'PDF_GANTT',
                'EXCEL']}

        self._message = None
        self._send_to = TypedList(Recipient)
        self._subject = None
        self._format_details = None
        self.__format = None
        self._cc_me = False

        if props:
            # account for alternate variable names from raw API response
            if 'message' in props:
                self.message = props['message']
            if 'sendTo' in props:
                self.send_to = props['sendTo']
            if 'send_to' in props:
                self.send_to = props['send_to']
            if 'subject' in props:
                self.subject = props['subject']
            if 'formatDetails' in props:
                self.format_details = props['formatDetails']
            if 'format_details' in props:
                self.format_details = props['format_details']
            if 'format' in props:
                self._format = props['format']
            if '_format' in props:
                self._format = props['_format']
            if 'ccMe' in props:
                self.cc_me = props['ccMe']
            if 'cc_me' in props:
                self.cc_me = props['cc_me']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self._format
        else:
            raise AttributeError(key)

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
    def _format(self):
        return self.__format

    @_format.setter
    def _format(self, value):
        if isinstance(value, six.string_types):
            if value not in self.allowed_values['_format']:
                raise ValueError(
                    ("`{0}` is an invalid value for SheetEmail`_format`,"
                     " must be one of {1}").format(
                         value, self.allowed_values['_format']))
            self.__format = value

    @property
    def cc_me(self):
        return self._cc_me

    @cc_me.setter
    def cc_me(self, value):
        if isinstance(value, bool):
            self._cc_me = value

    def to_dict(self, op_id=None, method=None):
        parent_obj = super(SheetEmail, self).to_dict(op_id, method)
        obj = {
            'message': prep(self._message),
            'sendTo': prep(self._send_to),
            'subject': prep(self._subject),
            'formatDetails': prep(self._format_details),
            'format': prep(self.__format),
            'ccMe': prep(self._cc_me)}
        combo = parent_obj.copy()
        combo.update(obj)
        return combo

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
