'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import httplib2
import json
import os
import copy
import time
import logging
import collections
import operator
import datetime
import traceback

class Workspace(object):
    # FIXME:  This class is massively incomplete.
    # FIXME:  This should be a TopLevelThing.
    def __init__(self, workspaceId):
        self.workspaceId = workspaceId
        self.location = '/workspace/%s' % str(self.workspaceId)
