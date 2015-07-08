'''
This is where the TopLevelThing and ContainedThing relationships are handled.

Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import json
import time
import collections
import types
import sys

class TopLevelThing(object):
    '''
    Some objects in the Smartsheet API more "naturally" have a client
    associated with them than others.  In general, the objects that can
    contain other objects are TopLevelThings.  Naturally, all objects
    exposed by the API can be fetched directly, but most are encountered
    as the result of fetching some other object (such as a Sheet, a
    Container, or a Workspace).

    The principal aspect of a TopLevelThing is that it has direct access
    to a SmartsheetClient instance.  Non-TopLevelThings that need a client
    must either be provided the client instance by the caller or "get to"
    a client instance.
    '''
    # TODO:  This class needs a better name than 'TopLevelThing'
    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client
        return self._client

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, parent):
        raise Exception("Can't set .parent on a TopLevelThing")

    @property
    def logger(self):
        if self.client is not None and self.client.logger is not None:
            return self.client.logger
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def markDirty(self):
        '''
        Mark this object as having a new value that should be saved.
        If this is a composite object, it may contain objects to be saved.
        '''
        self._dirty = True
        return self

    def isDirty(self):
        '''
        Return True if this object should be saved.
        '''
        return self._dirty

    def markClean(self):
        '''
        Mark this object as clean -- it doesn't need to be saved.
        '''
        self._dirty = False
        return self



class ContainedThing(object):
    '''
    Most objects in the Smartsheet API are "naturally" contained within
    other objects.  A ContainedThing that needs a client instance must
    either be passed it by the caller or "get to" a client instance by 
    traversing "up" (or down, depending on how you see object trees being
    rooted) to the TopLevelThing instance that has a client instance.
    '''
    # TODO:  This class needs a better name than 'ContainedThing'.
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        return self._parent

    @property
    def client(self):
        return self.parent.client

    @client.setter
    def client(self, client):
        # NOTE:  This might be incorrect.
        raise Exception("Can't set .client on a ContainedThing")

    @property
    def logger(self):
        return self.client.logger

    @logger.setter
    def logger(self, logger):
        raise Exception("Can't set .logger on a ContainedThing")

    def markDirty(self):
        '''
        Mark this object as having a new value that should be saved.
        '''
        self._dirty = True
        self.parent.markDirty()
        return self

    def isDirty(self):
        '''
        Return True if this object is dirty and should be saved.
        '''
        return self._dirty

    def markClean(self):
        '''
        Mark this object as clean -- it doesn't need to be saved.
        '''
        self._dirty = False
        return self




class AncillaryObjectSource(ContainedThing, object):
    '''
    Specify the source of an ancillary object (attachment, discussion, etc.).
    '''
    @property
    def sheetId(self):
        raise NotImplementedError("AncillaryObjectSource specialization error")

    @property
    def infoForHuman(self):
        raise NotImplementedError("AncillaryObjectSource specialization error")

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, self.infoForHuman)

    def __repr__(self):
        return str(self)



class AncillaryObjectSourceSheet(AncillaryObjectSource):
    '''
    Source information for Sheet-level ancillary objects.
    '''
    def __init__(self, sheet):
        self.sheet = sheet
        self.parent = sheet     # This belongs to a sheet.

    @property
    def sheetId(self):
        return self.sheet.id

    @property
    def infoForHuman(self):
        return "Sheet '%s'" % self.sheet.name
    


class AncillaryObjectSourceRow(AncillaryObjectSource):
    '''
    Source information for Row-level ancillary objects.
    '''
    def __init__(self, sheet, row):
        self.sheet = sheet
        self.row = row
        self.parent = row       # This belongs to a row.

    @property
    def sheetId(self):
        return self.sheet.id

    @property
    def infoForHuman(self):
        return "Sheet '%s', Row # %d" % (self.sheet.name, self.row.rowNumber)


def string_trim(value, max_len):
    '''
    Return a version of value that fits within max_len characters.
    '''
    if len(str(value)) > max_len:
        return str(value)[:max_len-3] + '...'
    else:
        return value


def maybeAssignFromDict(src_dict, dst_obj, src_name, dst_name=None):
    '''
    If the specified src_name is in the src_dict, assign it in dst_obj.
    The attribute name is the ('_' + src_name) unless dst_name is given.
    '''
    if src_name in src_dict:
        attr_name = dst_name or '_' + src_name
        setattr(dst_obj, attr_name, src_dict[src_name])
    return


def slicedict(src_dict, keys, include_missing_keys=True, default_value=None):
    '''
    Create a new dict from the specified keys in src_dict.
    If a key is not found in src_dict, it will not be included in the output
    unless include_missing_keys is True.  When including a missing key, the
    value of default is used for the key's value.

    @param src_dict The source dict to copy from.
    @param keys The list of keys to copy.
    @param include_missing_keys True to include them, False otherwise.
    @param default_value The value to use with keys that were not found.
    @return A dict of the selected keys from src_dict.
    '''
    acc = {}
    for key in keys:
        if key in src_dict:
            acc[key] = src_dict[key]
        else:
            if include_missing_keys:
                acc[key] = default_value
    return acc


def isList(items):
    '''
    Return True if items a list or something that is iterable like a list.
    In particular, a string is not a list, even if it is iterable.
    '''
    if isScalar(items):
        return False
    if isinstance(items, collections.Mapping):
        return False
    return isinstance(items, (collections.Sequence))


def isGenerator(items):
    '''
    Return True if items is a generator.
    '''
    return type(items) == types.GeneratorType


def isScalar(item):
    '''
    Return True if item is a scalar (number or string, bytes).
    False otherwise.
    '''
    if sys.version_info.major == 2 and isinstance(item, (int, float, long, str,
        unicode, basestring, bytes)):
            return True
    elif sys.version_info.major == 3 and isinstance(item, (int, float, str,
        bool, bytes)):
            return True
    return False

def isMapping(item):
    return isinstance(item, collections.Mapping)

def isInteger(item):
    if sys.version_info.major == 2:
        return isinstance(item, (int, long))
    elif sys.version_info.major == 3:
        return isinstance(item, int)
    else:
        return isinstance(item, int)
