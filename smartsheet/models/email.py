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

from .recipient import Recipient
from ..types import *
from ..util import serialize
from ..util import deserialize


class Email(object):

    """Smartsheet Email data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Email model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._cc_me = Boolean()
        self._message = String()
        self._send_to = TypedList(Recipient)
        self._subject = String()

        if props:
            deserialize(self, props)

    @property
    def cc_me(self):
        return self._cc_me.value

    @cc_me.setter
    def cc_me(self, value):
        self._cc_me.value = value

    @property
    def message(self):
        return self._message.value

    @message.setter
    def message(self, value):
        self._message.value = value

    @property
    def send_to(self):
        return self._send_to

    @send_to.setter
    def send_to(self, value):
        self._send_to.load(value)

    @property
    def subject(self):
        return self._subject.value

    @subject.setter
    def subject(self, value):
        self._subject.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
