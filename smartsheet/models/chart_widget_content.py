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
from .selection_range import SelectionRange
from .widget_content import WidgetContent
from .widget_hyperlink import WidgetHyperlink
from ..types import *
from ..util import serialize
from ..util import deserialize


class ChartWidgetContent(WidgetContent):
    """Smartsheet ChartWidgetContent data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ChartWidgetContent model."""
        super(ChartWidgetContent, self).__init__(WidgetType.CHART, base_obj)
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        """Represents the ChartWidgetContent object"""
        self._report_id = Number()
        self._sheet_id = Number()
        self._axes = TypedObject(object)
        self._hyperlink = TypedObject(WidgetHyperlink)
        self._included_column_ids = TypedList(six.integer_types)
        self._legend = TypedObject(object)
        self._selection_ranges = TypedList(SelectionRange)
        self._series = TypedObject(object)

        if props:
            deserialize(self, props)

        self.__initialized = True

    """Represents the ChartWidgetContent object"""
    @property
    def report_id(self):
        return self._report_id.value

    @report_id.setter
    def report_id(self, value):
        self._report_id.value = value

    @property
    def sheet_id(self):
        return self._sheet_id.value

    @sheet_id.setter
    def sheet_id(self, value):
        self._sheet_id.value = value

    @property
    def axes(self):
        return self._axes.value

    @axes.setter
    def axes(self, value):
        self._axes.value = value

    @property
    def hyperlink(self):
        return self._hyperlink.value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink.value = value

    @property
    def included_column_ids(self):
        return self._included_column_ids

    @included_column_ids.setter
    def included_column_ids(self, value):
        self._included_column_ids.load(value)

    @property
    def legend(self):
        return self._legend.value

    @legend.setter
    def legend(self, value):
        self._legend.value = value

    @property
    def selection_ranges(self):
        return self._selection_ranges

    @selection_ranges.setter
    def selection_ranges(self, value):
        self._selection_ranges.load(value)

    @property
    def series(self):
        return self._series.value

    @series.setter
    def series(self, value):
        self._series.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
