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

from .contact_object_value import ContactObjectValue
from .object_value import *
from ..types import *
from ..util import deserialize


class MultiContactObjectValue(ObjectValue):
    """Smartsheet MultiContactObjectValue data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the MultiContactObjectValue model."""
        ObjectValue.__init__(self, MULTI_CONTACT, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._values = TypedList(ContactObjectValue)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values.load(value)
