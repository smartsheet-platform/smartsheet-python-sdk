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

from .enums import WidgetType
from .widget_content import WidgetContent
from .widget_hyperlink import WidgetHyperlink
from ..types import *
from ..util import serialize
from ..util import deserialize


class ReportWidgetContent(WidgetContent):
    """Smartsheet ReportWidgetContent data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportWidgetContent model."""
        super(ReportWidgetContent, self).__init__(WidgetType.GRIDGANTT, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        """Represents the ReportWidgetContent object."""
        self._html_content = String()
        self._hyperlink = TypedObject(WidgetHyperlink)
        self._report_id = Number()

        if props:
            deserialize(self, props)

        self.__initialized = True

    """Represents the ReportWidgetContent object."""
    @property
    def html_content(self):
        return self._html_content.value

    @html_content.setter
    def html_content(self, value):
        self._html_content.value = value

    @property
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

    @property
    def report_id(self):
        return self._report_id.value

    @report_id.setter
    def report_id(self, value):
        self._report_id.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
