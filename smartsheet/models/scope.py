# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2019 Smartsheet.com, Inc.
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

from .sheet import Sheet
from ..types import *
from ..util import serialize
from ..util import deserialize


class Scope(object):
    """Smartsheet Scope data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Scope model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        # Workspace creates a circular import dependency, so, as much as I'm not a fan of moving the import
        # into the __init__, its the most pragmatic approach for this simple problem.
        from .workspace import Workspace

        self._sheets = TypedList(Sheet)
        self._workspaces = TypedList(Workspace)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def sheets(self):
        return self._sheets

    @sheets.setter
    def sheets(self, value):
        self._sheets.load(value)

    @property
    def workspaces(self):
        return self._workspaces

    @workspaces.setter
    def workspaces(self, value):
        self._workspaces.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
