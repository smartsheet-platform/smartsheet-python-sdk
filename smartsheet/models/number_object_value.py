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

from .primitive_object_value import PrimitiveObjectValue
from .object_value import *


class NumberObjectValue(PrimitiveObjectValue):
    """Smartsheet NumberObjectValue data model."""

    def __init__(self, value=None, base_obj=None):
        """Initialize the NumberObjectValue model."""
        super(NumberObjectValue, self).__init__(value, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self.__initialized = True

    @property
    def object_type(self):
        return NUMBER
