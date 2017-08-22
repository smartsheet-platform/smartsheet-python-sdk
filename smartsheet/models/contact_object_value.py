# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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

from .contact import Contact
from .object_value import *
import json


class ContactObjectValue(Contact, ObjectValue):
    """Smartsheet ContactObjectValue data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ContactObjectValue model."""
        super(ContactObjectValue, self).__init__(props, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        if not props:
            self.object_type = CONTACT

        self.__initialized = True

    def to_dict(self, op_id=None, method=None):
        obj = super(ContactObjectValue, self).to_dict(op_id, method)
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())