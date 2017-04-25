# pylint: disable=C0111,C0413
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

__api_base__ = 'https://api.smartsheet.com/2.0'
__api_version__ = '2.0'

try:
    from .version import version
    __version__ = version
except ImportError:
    from setuptools_scm import get_version
    __version__ = get_version()

from .smartsheet import Smartsheet, fresh_operation, AbstractUserCalcBackoff  # NOQA
