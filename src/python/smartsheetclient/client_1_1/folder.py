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


class Folder(object):
    # FIXME:  This class is massively incomplete.
    def __init__(self, folderId):
        self.folderId = folderId
        self.location = '/folder/%s' % str(self.folderId)

