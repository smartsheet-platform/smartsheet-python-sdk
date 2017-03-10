# pylint: disable=C0111,R0902,R0913
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

import logging
from . import fresh_operation
from .models.image_url import ImageUrl
from .types import TypedList


class Images(object):

    """Class for handling Images operations."""

    def __init__(self, smartsheet_obj):
        """Init Images with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get_image_urls(self, list_of_images):
        """Get URLs that can be used to retrieve specified cell images.

        Args:
            list_of_images (list[ImageURL]): Array containing one
                or more ImageURL objects.

        Returns:
            ImageURLMap
        """
        if isinstance(list_of_images, (dict, ImageUrl)):
            arg_value = list_of_images
            list_of_images = TypedList(ImageUrl)
            list_of_images.append(arg_value)

        _op = fresh_operation('get_image_urls')
        _op['method'] = 'POST'
        _op['path'] = '/imageurls'
        _op['json'] = list_of_images

        expected = 'ImageUrlMap'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
