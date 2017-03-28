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

from ..util import prep
from .error_result import ErrorResult
import json
import logging
import six

class ImageUrl(object):

    """Smartsheet ImageUrl data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ImageUrl model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._log = logging.getLogger(__name__)

        self._image_id = None
        self._width = 0
        self._height = 0
        self._url = None
        self._error = None

        if props:
            # account for alternate variable names from raw API response
            if 'imageId' in props:
                self.image_id = props['imageId']
            if 'image_id' in props:
                self.image_id = props['image_id']
            if 'width' in props:
                self.width = props['width']
            if 'height' in props:
                self.height = props['height']
            if 'url' in props:
                self.url = props['url']
            if 'error' in props:
                self.error = props['error']

    @property
    def image_id(self):
        return self._image_id

    @image_id.setter
    def image_id(self, value):
        if isinstance(value, six.string_types):
            self._image_id = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, six.integer_types):
            self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, six.integer_types):
            self._height = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if isinstance(value, six.string_types):
            self._url = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if isinstance(value, dict):
            self._error = self._result = ErrorResult(value, self._base)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'imageId': prep(self._image_id),
            'width': prep(self._width),
            'height': prep(self._height),
            'url' : prep(self._url),
            'error' : prep(self._error)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        permitted = ['imageId', 'width', 'height']
        all_keys = list(obj.keys())
        for key in all_keys:
            if key not in permitted:
                self._log.debug(
                    'deleting %s from obj', key)
                del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())