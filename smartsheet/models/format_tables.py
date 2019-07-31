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

from .currency import Currency
from .font_family import FontFamily
from ..types import *
from ..util import serialize
from ..util import deserialize


class FormatTables(object):

    """Smartsheet FormatTables data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the FormatTables model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._bold = TypedList(str)
        self._color = TypedList(str)
        self._currency = TypedList(Currency)
        self._date_format = TypedList(str)
        self._decimal_count = TypedList(str)
        self._defaults = String()
        self._font_family = TypedList(FontFamily)
        self._font_size = TypedList(str)
        self._horizontal_align = TypedList(str)
        self._italic = TypedList(str)
        self._number_format = TypedList(str)
        self._strikethrough = TypedList(str)
        self._text_wrap = TypedList(str)
        self._thousands_separator = TypedList(str)
        self._underline = TypedList(str)
        self._vertical_align = TypedList(str)

        if props:
            deserialize(self, props)

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value):
        self._bold.load(value)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color.load(value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency.load(value)

    @property
    def date_format(self):
        return self._date_format

    @date_format.setter
    def date_format(self, value):
        self._date_format.load(value)

    @property
    def decimal_count(self):
        return self._decimal_count

    @decimal_count.setter
    def decimal_count(self, value):
        self._decimal_count.load(value)

    @property
    def defaults(self):
        return self._defaults.value

    @defaults.setter
    def defaults(self, value):
        self._defaults.value = value

    @property
    def font_family(self):
        return self._font_family

    @font_family.setter
    def font_family(self, value):
        self._font_family.load(value)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size.load(value)

    @property
    def horizontal_align(self):
        return self._horizontal_align

    @horizontal_align.setter
    def horizontal_align(self, value):
        self._horizontal_align.load(value)

    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, value):
        self._italic.load(value)

    @property
    def number_format(self):
        return self._number_format

    @number_format.setter
    def number_format(self, value):
        self._number_format.load(value)

    @property
    def strikethrough(self):
        return self._strikethrough

    @strikethrough.setter
    def strikethrough(self, value):
        self._strikethrough.load(value)

    @property
    def text_wrap(self):
        return self._text_wrap

    @text_wrap.setter
    def text_wrap(self, value):
        self._text_wrap.load(value)

    @property
    def thousands_separator(self):
        return self._thousands_separator

    @thousands_separator.setter
    def thousands_separator(self, value):
        self._thousands_separator.load(value)

    @property
    def underline(self):
        return self._underline

    @underline.setter
    def underline(self, value):
        self._underline.load(value)

    @property
    def vertical_align(self):
        return self._vertical_align

    @vertical_align.setter
    def vertical_align(self, value):
        self._vertical_align.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
