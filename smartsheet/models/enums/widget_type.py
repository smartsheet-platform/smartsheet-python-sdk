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
from enum import Enum


class WidgetType(Enum):
    CHART = 1
    IMAGE = 2
    METRIC = 3
    GRIDGANTT = 4
    RICHTEXT = 5
    SHORTCUT = 6
    TITLE = 7
    WEBCONTENT = 8
    # NOTE: These are level=0 widget types that should be supported for now
    SHORTCUTLIST = 9   # SHORTCUTLIST --> SHORTCUT
    SHORTCUTICON = 10  # SHORTCUTICON --> SHORTCUT
    SHEETSUMMARY = 11  # SHEETSUMMARY --> METRIC
