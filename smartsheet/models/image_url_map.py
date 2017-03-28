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
from ..types import TypedList
from .image_url import ImageUrl
import json
import logging
import six

class ImageUrlMap(object):

    """Smartsheet ImageUrlMap data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ImageUrlMap model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._url_expires_in_millis = 0
        self._image_urls = TypedList(ImageUrl)

        if props:
            # account for alternate variable names from raw API response
            if 'urlExpiresInMillis' in props:
                self.url_expires_in_millis = props['urlExpiresInMillis']
            if 'url_expires_in_millis' in props:
                self.url_expires_in_millis = props['url_expires_in_millis']
            if 'imageUrls' in props:
                self.image_urls = props['imageUrls']
            if 'image_urls' in props:
                self.image_urls = props['image_urls']
        # requests package Response object
        self.request_response = None
        self.__initialized = True

    @property
    def url_expires_in_millis(self):
        return self._url_expires_in_millis

    @url_expires_in_millis.setter
    def url_expires_in_millis(self, value):
        if isinstance(value, six.integer_types):
            self._url_expires_in_millis = value

    @property
    def image_urls(self):
        return self._image_urls

    @image_urls.setter
    def image_urls(self, value):
        if isinstance(value, list):
            self._image_urls.purge()
            self._image_urls.extend([
                (ImageUrl(x, self._base)
                 if not isinstance(x, ImageUrl) else x) for x in value
            ])
        elif isinstance(value, TypedList):
            self._image_urls.purge()
            self._image_urls = value.to_list()
        elif isinstance(value, ImageUrl):
            self._image_urls.purge()
            self._image_urls.append(value)

    def to_dict(self, op_id=None, method=None):
        obj = {
            'urlExpiresInMillis': prep(self._url_expires_in_millis),
            'imageUrls': prep(self._image_urls)}
        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())