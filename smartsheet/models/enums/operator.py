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


class Operator(Enum):
    EQUAL = 1
    NOT_EQUAL = 2
    GREATER_THAN = 3
    GREATER_THAN_OR_EQUAL = 4
    LESS_THAN = 5
    LESS_THAN_OR_EQUAL = 6
    CONTAINS = 7
    DOES_NOT_CONTAIN = 8
    BETWEEN = 9
    NOT_BETWEEN = 10
    TODAY = 11
    NOT_TODAY = 12
    PAST = 13
    NOT_PAST = 14
    FUTURE = 15
    NOT_FUTURE = 16
    LAST_N_DAYS = 17
    NOT_LAST_N_DAYS = 18
    NEXT_N_DAYS = 19
    NOT_NEXT_N_DAYS = 20
    IS_BLANK = 21
    IS_NOT_BLANK = 22
    IS_NUMBER = 23
    IS_NOT_NUMBER = 24
    IS_DATE = 25
    IS_NOT_DATE = 26
    IS_CHECKED = 27
    IS_NOT_CHECKED = 28
    IS_ONE_OF = 29
    IS_NOT_ONE_OF = 30
    IS_CURRENT_USER = 31
    IS_NOT_CURRENT_USER = 32
    ON_CRITICAL_PATH = 33
    NOT_ON_CRITICAL_PATH = 34
    HAS_ATTACHMENTS = 35
    NO_ATTACHMENTS = 36
    HAS_COMMENTS = 37
    NO_COMMENTS = 38
    HAS_ANY_OF = 39
    HAS_NONE_OF = 40
    HAS_ALL_OF = 41
    NOT_ALL_OF = 42