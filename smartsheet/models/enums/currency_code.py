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


class CurrencyCode(Enum):
    ARS = 1
    AUD = 2
    BRL = 3
    CAD = 4
    CLP = 5
    EUR = 6
    GBP = 7
    ILS = 8
    INR = 9
    JPY = 10
    MXN = 11
    RUB = 12
    USD = 13
    ZAR = 14
    CHF = 15
    NY = 16
    DKK = 17
    HKD = 18
    KRW = 19
    NOK = 20
    NZD = 21
    SEK = 22
    SGD = 23
