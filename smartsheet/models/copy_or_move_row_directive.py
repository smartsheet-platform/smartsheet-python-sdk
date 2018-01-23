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

import json

from .copy_or_move_row_destination import CopyOrMoveRowDestination
from ..types import TypedList
from ..util import serialize
from ..util import deserialize


class CopyOrMoveRowDirective(object):

    """Smartsheet CopyOrMoveRowDirective data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CopyOrMoveRowDirective model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._row_ids = TypedList(int)
        self._to = None

        if props:
            deserialize(self, props)

    @property
    def row_ids(self):
        return self._row_ids

    @row_ids.setter
    def row_ids(self, value):
        self._row_ids.load(value)

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        if isinstance(value, CopyOrMoveRowDestination):
            self._to = value
        else:
            self._to = CopyOrMoveRowDestination(value, self._base)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
