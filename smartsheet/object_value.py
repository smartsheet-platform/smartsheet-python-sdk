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

from .models.boolean_object_value import BooleanObjectValue
from .models.contact_object_value import ContactObjectValue
from .models.date_object_value import DateObjectValue
from .models.datetime_object_value import DatetimeObjectValue
from .models.duration import Duration
from .models.multi_contact_object_value import MultiContactObjectValue
from .models.multi_picklist_object_value import MultiPicklistObjectValue
from .models.number_object_value import NumberObjectValue
from .models.object_value import *
from .models.predecessor_list import PredecessorList
from .models.string_object_value import StringObjectValue


def assign_to_object_value(value):

    if isinstance(value, ObjectValue):
        return value
    elif isinstance(value, dict):
        object_type = value['objectType']
        if object_type in OBJECT_VALUE['object_type']:
            enum_object_type = enum_object_value_type(object_type)
            if enum_object_type == DURATION:
                return Duration(value)
            elif enum_object_type == PREDECESSOR_LIST:
                return PredecessorList(value)
            elif enum_object_type == CONTACT:
                return ContactObjectValue(value)
            elif enum_object_type == DATE:
                return DateObjectValue(value)
            elif enum_object_type == DATETIME or \
                    enum_object_type == ABSTRACT_DATETIME:
                return DatetimeObjectValue(value, enum_object_value_type)
            elif enum_object_type == MULTI_CONTACT:
                return MultiContactObjectValue(value)
            elif enum_object_type == MULTI_PICKLIST:
                return MultiPicklistObjectValue(value)
            else:
                return None
        else:
            raise ValueError(
                ("`{0}` is an invalid value for ObjectValue`object_type`,"
                 " must be one of {1}").format(
                    object_type, OBJECT_VALUE['object_type']))
    elif isinstance(value, six.string_types):
        return StringObjectValue(value)
    elif isinstance(value, bool):
        return BooleanObjectValue(value)
    elif isinstance(value, (six.integer_types, float)):
        return NumberObjectValue(value)
