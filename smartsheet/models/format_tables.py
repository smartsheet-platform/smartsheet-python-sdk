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

from .currency import Currency
from .font_family import FontFamily
from ..types import TypedList
from ..util import prep
from datetime import datetime
import json
import logging
import six

class FormatTables(object):

    """Smartsheet FormatTables data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the FormatTables model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None

        self._bold = TypedList(str)
        self._color = TypedList(str)
        self._currency = TypedList(Currency)
        self._decimal_count = TypedList(str)
        self._defaults = None
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
            # account for alternate variable names from raw API response
            if 'bold' in props:
                self.bold = props['bold']
            if 'color' in props:
                self.color = props['color']
            if 'currency' in props:
                self.currency = props['currency']
            if 'decimalCount' in props:
                self.decimal_count = props['decimalCount']
            if 'decimal_count' in props:
                self.decimal_count = props['decimal_count']
            if 'defaults' in props:
                self.defaults = props['defaults']
            if 'fontFamily' in props:
                self.font_family = props['fontFamily']
            if 'font_family' in props:
                self.font_family = props['font_family']
            if 'fontSize' in props:
                self.font_size = props['fontSize']
            if 'font_size' in props:
                self.font_size = props['font_size']
            if 'horizontalAlign' in props:
                self.horizontal_align = props['horizontalAlign']
            if 'horizontal_align' in props:
                self.horizontal_align = props[
                    'horizontal_align']
            if 'italic' in props:
                self.italic = props['italic']
            if 'numberFormat' in props:
                self.number_format = props['numberFormat']
            if 'number_format' in props:
                self.number_format = props['number_format']
            if 'strikethrough' in props:
                self.strikethrough = props['strikethrough']
            if 'textWrap' in props:
                self.text_wrap = props['textWrap']
            if 'text_wrap' in props:
                self.text_wrap = props['text_wrap']
            if 'thousandsSeparator' in props:
                self.thousands_separator = props[
                    'thousandsSeparator']
            if 'thousands_separator' in props:
                self.thousands_separator = props[
                    'thousands_separator']
            if 'underline' in props:
                self.underline = props['underline']
            if 'verticalAlign' in props:
                self.vertical_align = props['verticalAlign']
            if 'vertical_align' in props:
                self.vertical_align = props['vertical_align']

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value):
        if isinstance(value, list):
            self._bold.purge()
            self._bold.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._bold.purge()
            self._bold = value.to_list()
        elif isinstance(value, str):
            self._bold.purge()
            self._bold.append(value)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, list):
            self._color.purge()
            self._color.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._color.purge()
            self._color = value.to_list()
        elif isinstance(value, str):
            self._color.purge()
            self._color.append(value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if isinstance(value, list):
            self._currency.purge()
            self._currency.extend([
                (Currency(x, self._base)
                 if not isinstance(x, Currency) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._currency.purge()
            self._currency = value.to_list()
        elif isinstance(value, Currency):
            self._currency.purge()
            self._currency.append(value)

    @property
    def decimal_count(self):
        return self._decimal_count

    @decimal_count.setter
    def decimal_count(self, value):
        if isinstance(value, list):
            self._decimal_count.purge()
            self._decimal_count.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._decimal_count.purge()
            self._decimal_count = value.to_list()
        elif isinstance(value, str):
            self._decimal_count.purge()
            self._decimal_count.append(value)

    @property
    def defaults(self):
        return self._defaults

    @defaults.setter
    def defaults(self, value):
        if isinstance(value, six.string_types):
            self._defaults = value

    @property
    def font_family(self):
        return self._font_family

    @font_family.setter
    def font_family(self, value):
        if isinstance(value, list):
            self._font_family.purge()
            self._font_family.extend([
                (FontFamily(x, self._base)
                 if not isinstance(x, FontFamily) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._font_family.purge()
            self._font_family = value.to_list()
        elif isinstance(value, FontFamily):
            self._font_family.purge()
            self._font_family.append(value)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        if isinstance(value, list):
            self._font_size.purge()
            self._font_size.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._font_size.purge()
            self._font_size = value.to_list()
        elif isinstance(value, str):
            self._font_size.purge()
            self._font_size.append(value)

    @property
    def horizontal_align(self):
        return self._horizontal_align

    @horizontal_align.setter
    def horizontal_align(self, value):
        if isinstance(value, list):
            self._horizontal_align.purge()
            self._horizontal_align.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._horizontal_align.purge()
            self._horizontal_align = value.to_list()
        elif isinstance(value, str):
            self._horizontal_align.purge()
            self._horizontal_align.append(value)

    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, value):
        if isinstance(value, list):
            self._italic.purge()
            self._italic.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._italic.purge()
            self._italic = value.to_list()
        elif isinstance(value, str):
            self._italic.purge()
            self._italic.append(value)

    @property
    def number_format(self):
        return self._number_format

    @number_format.setter
    def number_format(self, value):
        if isinstance(value, list):
            self._number_format.purge()
            self._number_format.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._number_format.purge()
            self._number_format = value.to_list()
        elif isinstance(value, str):
            self._number_format.purge()
            self._number_format.append(value)

    @property
    def strikethrough(self):
        return self._strikethrough

    @strikethrough.setter
    def strikethrough(self, value):
        if isinstance(value, list):
            self._strikethrough.purge()
            self._strikethrough.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._strikethrough.purge()
            self._strikethrough = value.to_list()
        elif isinstance(value, str):
            self._strikethrough.purge()
            self._strikethrough.append(value)

    @property
    def text_wrap(self):
        return self._text_wrap

    @text_wrap.setter
    def text_wrap(self, value):
        if isinstance(value, list):
            self._text_wrap.purge()
            self._text_wrap.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._text_wrap.purge()
            self._text_wrap = value.to_list()
        elif isinstance(value, str):
            self._text_wrap.purge()
            self._text_wrap.append(value)

    @property
    def thousands_separator(self):
        return self._thousands_separator

    @thousands_separator.setter
    def thousands_separator(self, value):
        if isinstance(value, list):
            self._thousands_separator.purge()
            self._thousands_separator.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._thousands_separator.purge()
            self._thousands_separator = value.to_list()
        elif isinstance(value, str):
            self._thousands_separator.purge()
            self._thousands_separator.append(value)

    @property
    def underline(self):
        return self._underline

    @underline.setter
    def underline(self, value):
        if isinstance(value, list):
            self._underline.purge()
            self._underline.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._underline.purge()
            self._underline = value.to_list()
        elif isinstance(value, str):
            self._underline.purge()
            self._underline.append(value)

    @property
    def vertical_align(self):
        return self._vertical_align

    @vertical_align.setter
    def vertical_align(self, value):
        if isinstance(value, list):
            self._vertical_align.purge()
            self._vertical_align.extend([
                (str(x)
                 if not isinstance(x, str) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._vertical_align.purge()
            self._vertical_align = value.to_list()
        elif isinstance(value, str):
            self._vertical_align.purge()
            self._vertical_align.append(value)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'bold': prep(self._bold),
            'color': prep(self._color),
            'currency': prep(self._currency),
            'decimalCount': prep(self._decimal_count),
            'defaults': prep(self._defaults),
            'fontFamily': prep(self._font_family),
            'fontSize': prep(self._font_size),
            'horizontalAlign': prep(self._horizontal_align),
            'italic': prep(self._italic),
            'numberFormat': prep(self._number_format),
            'strikethrough': prep(self._strikethrough),
            'textWrap': prep(self._text_wrap),
            'thousandsSeparator': prep(self._thousands_separator),
            'underline': prep(self._underline),
            'verticalAlign': prep(self._vertical_align)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
