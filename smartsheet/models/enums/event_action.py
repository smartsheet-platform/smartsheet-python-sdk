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

from enum import Enum


class EventAction(Enum):
    CREATE = 1
    UPDATE = 2
    LOAD = 3
    DELETE = 4
    PURGE = 5
    RESTORE = 6
    RENAME = 7
    ACTIVATE = 8
    DEACTIVATE = 9
    EXPORT = 10
    MOVE = 11
    MOVE_ROW = 12
    COPY_ROW = 13
    SAVE_AS_NEW = 14
    SAVE_AS_TEMPLATE = 15
    ADD_PUBLISH = 16
    REMOVE_PUBLISH = 17
    ADD_SHARE = 18
    REMOVE_SHARE = 19
    ADD_SHARE_MEMBER = 20
    REMOVE_SHARE_MEMBER = 21
    ADD_WORKSPACE_SHARE = 22
    REMOVE_WORKSPACE_SHARE = 23
    ADD_MEMBER = 24
    REMOVE_MEMBER = 25
    TRANSFER_OWNERSHIP = 26
    CREATE_CELL_LINK = 27
    REMOVE_SHARES = 28
    TRANSFER_OWNED_GROUPS = 29
    TRANSFER_OWNED_ITEMS = 30
    DOWNLOAD_SHEET_ACCESS_REPORT = 31
    DOWNLOAD_USER_LIST = 32
    DOWNLOAD_LOGIN_HISTORY = 33
    DOWNLOAD_PUBLISHED_ITEMS_REPORT = 34
    UPDATE_MAIN_CONTACT = 35
    IMPORT_USERS = 36
    BULK_UPDATE = 37
    LIST_SHEETS = 38
    REQUEST_BACKUP = 39
    CREATE_RECURRING_BACKUP = 40
    UPDATE_RECURRING_BACKUP = 41
    DELETE_RECURRING_BACKUP = 42
    REMOVE_FROM_GROUPS = 43
    SEND_AS_ATTACHMENT = 44
    SEND_ROW = 45
    SEND = 46
    SEND_COMMENT = 47
    SEND_INVITE = 48
    DECLINE_INVITE = 49
    ACCEPT_INVITE = 50
    SEND_PASSWORD_RESET = 51
    REMOVE_FROM_ACCOUNT = 52
    ADD_TO_ACCOUNT = 53
    AUTHORIZE = 54
    REVOKE = 55
