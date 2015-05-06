'''
Library for working with Smartsheet's version 1.1 API.

This is HORRIBLY incomplete at the moment.

Author:  Scott Wimer <scott.wimer@smartsheet.com>
'''

import json
import os

from smartsheet_exceptions import SmartsheetClientError
from base import ContainedThing

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



class Attachment(ContainedThing, object):
    '''
    Information about an attachment.
    There is no reason for an SDK user to create instances of this class.
    '''
    # TODO: Consider renaming this class:  AttachmentInfo or AttachmentMetadata
    # TODO: Check the Example Response secton from Get Row Attachments.
    # I think the use of "parent" instead of "parentType" is an error.
    # TODO: Check the Attachment Object section.
    # I think that url and urlExpiresMillis are actually part of the
    # attachment download info, and not of the attachment information object.
    # Probably, the API docs need to describe this as two different objects,
    # Attachment Information, and the other Attachment Download Information.
    # Otherwise, they're describing an object that does not have a fixed set
    # of fields.
    field_names = '''attachmentType attachmentSubType createdAt createdBy
                    id mimeType name sizeInKb parentType parentId
                    url urlExpiresMillis'''.split()


    def __init__(self, sheet, id, name, attachmentType, attachmentSubType,
            createdAt, createdBy, parentType, parentId, mimeType=None,
            url=None, urlExpiresMillis=None, sizeInKb=None):
        self.sheet = sheet
        self.parent = sheet
        self._id = id
        self._name = name
        self._attachmentType = attachmentType   # TODO: validate this
        self._attachmentSubType = attachmentSubType # TODO: validate this
        self._createdAt = createdAt
        self._createdBy = createdBy
        self._parentType = parentType   # TODO: validate this
        self._parentId = parentId
        self._mimeType = mimeType
        self._url = url                 # I'm not sure this even belongs here.
        self._urlExpiresMillis = urlExpiresMillis   # probably doesn't belong
        self._sizeInKb = sizeInKb
        self._fields = {}       # For consistency with newFromAPI().

    @classmethod
    def newFromAPI(self, fields, sheet):
        params = slicedict(fields, self.field_names, include_missing_keys=True)
        att = Attachment(sheet, **params)
        self._fields = fields

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def attachmentType(self):
        return self._attachmentType

    @property
    def attachmentSubType(self):
        return self._attachmentSubType

    @property
    def createdAt(self):
        return self._createdAt

    @property
    def createdBy(self):
        return SimpleUser(self._createdBy)

    @property
    def parentType(self):
        return self._parentType

    @property
    def parentId(self):
        return self._parentId

    @property
    def mimeType(self):
        return self._mimeType

   @property
    def url(self):
        return self._url

    @property
    def urlExpiresMillis(self):
        return self._urlExpiresMillis

    @property
    def sizeInKb(self):
        return self._sizeInKb
 
    @property
    def fetchPath(self):
        return '/sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))

    @property
    def replacePath(self):
        # I'm not sure that this is the right approach.
        # It might be that Sheet.replaceAttachment() would be the way to go.
        # Or, perhaps, we should just let the user of the library do it by
        # uploading a new attachment and deleting the old one.  That seems
        # like the simplest approach.
        raise NotImplementedError("Attachment.replacePath() not implemented")

    @property
    def newVersionPath(self):
        # TODO:  Support limiitiations on where a new version can be uploaded
        # Attachments on Discussion Comments can not have new versions uploaded
        # for them.  If we don't detect that in the SDK, it will result in an
        # error from the server.
        # A new version is only supported for FILE attachments to Sheets or
        # Rows, at least according to the current API docs (I haven't checked).
        return '/sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))

    @property
    def sourceInfo(self):
        '''
        Human usable information about the source of the attachment.
        '''
        raise NotImplementedError("Attachment.sourceInfo not implemented.")

    def getVersionList(self):
        '''
        Get a list of all versions of the attachment.
        Returns the list of Attachment objects.
        NOTE:  these Attachment objects have additional fields that regular
        Attachment objects don't: 'parentType' and 'parentId'
        '''
        path = 'sheet/%s/attachment/%s/versions' % (str(self.sheet.id),
                str(self.id))
        name = "%s.getVersionList()" % self
        body = self.client.GET(path, name=name)
        return [Attachment(a, self.sheet) for a in body]

    def getDownloadInfo(self):
        '''
        Fetch the AttachmentDownloadInfo for this Attachment.
        Return the URL used to fetch the attachment.
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        name = "%s.getDownloadInfo()" % self
        body = self.client.GET(path, name=name)
        return AttachmentDownloadInfo(body, self.sheet)

    def download(self):
        '''
        Download the attachment, into a populated AttachmentDownloadInfo object.
        The attachment contents are available at .data on the returned object.
        '''
        di = self.getDownloadInfo()
        di.download()
        return di

    def downloadAndStore(self, base_path=''):
        '''
        Download and store an attachment.
        The attachment contents are also available at .data on the returned
        AttachmentDownloadInfo object.
        '''
        di = self.download()
        di.save(base_path)
        return di

    def uploadNewVersion(self, content, content_type=None):
        '''
        Upload a new version of the attachment.
        The new version has the same file name, and will, by default have
        the same Content-Type, but with the new content.

        Note that uploading an attachment is an "expensive" operation,
        and as such may fail because too many operations have been performed
        within a small time window.  At present, only 300 operations are
        permitted per minute, and uploading an attachment counts as 10
        operations.
        '''
        if self.attachmentType != 'FILE':
            err = ("Attachment.uploadNewVersion() Can only replace 'FILE' " +
                    "Attachment types")
            self.logger.error(err)
            raise SmartsheetClientError(err)
        path = 'sheet/%s/attachment/%s/versions' % (
                str(self.sheet.id), str(self.id))
        headers = {'Content-Type': self.mimeType,
                    'Content-Length': str(len(content)),
                    'Content-Disposition': 
                            'attachment; filename="%s"' % (self.name),
                  }
        name = "%s.uploadNewVersion()" % self
        body = self.client.POST(path, extra_headers=headers, body=content,
                name=name)
        return Attachment(body['result'], sheet=self.sheet)
                 
    def __str__(self):
        return '<Attachment id:%r, name:%r, type:%r:%r created:%r>' % (
                self.id, self.name, self.attachmentType, self.mimeType,
                self.createdAt)

    def __repr__(self):
        return str(self)



class AttachmentDownloadInfo(ContainedThing, object):
    '''
    Information about downloading an attachment.
    '''
    field_names = '''name url attachmentType mimeType id
                    urlExpiresInMillis'''.split()
    # NOTE: Presently (January, 2015), the API only supports Attachments that
    #       are attached to a Sheet directly or indirectly (Row or
    #       Discussion comment).  The application supports Workspace-level
    #       attachments.  It may be that the AttachmentDownloadInfo object
    #       will need to take an AncillarySourceObject in the future if the
    #       API expands to support other Attachments.

    def __init__(self, fields, sheet):
        self.fields = fields
        self.sheet = sheet
        self.parent = sheet     # Owned by a sheet.
        self._data = None   # The downloaded attachment.
        self._download_response = None

    @property
    def name(self):
        return self.fields['name']

    @property
    def url(self):
        return self.fields['url']

    @property
    def attachmentType(self):
        return self.fields['attachmentType']

    @property
    def mimeType(self):
        return self.fields['mimeType']

    @property
    def id(self):
        return self.fields['id']

    @property
    def urlExpiresInMillis(self):
        return self.fields.get('urlExpiresInMillis')

    @property
    def data(self):
        return self._data
    
    def checkAttachment(self, client=None):
        '''
        Issue a HEAD request on the attachment -- this will let us get the
        etag, which is an MD5 checksum of the attachment's contents (assuming
        the attachment was stored in Amazon S3 using PUT or POST Object
        operations.
        Sadly, the Signature in the URL this doesn't work
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        resp, body = client.rawRequest(self.url, '', 'HEAD')
        self.logger.debug("HTTP HEAD request for attachment, resp: %r", resp)
        self.logger.debug("HTTP HEAD request for attachment, body: %r", body)

    def download(self, client=None):
        '''
        Download the attachment, and store it in self._data
        '''
        path = 'sheet/%s/attachment/%s' % (str(self.sheet.id), str(self.id))
        client = client or self.client
        resp, self._data = client.rawRequest(self.url, '', 'GET')
        self._download_resp = resp
        resp = HttpResponse(resp)
        if resp.isOK():
            return True
        err = ("AttachmentDownloadInfo.download(%s) failed: %s" %
                (self, resp.hdr))
        self.logger.error(err)
        raise SmartsheetClientError(err)

    def save(self, base_path=''):
        '''
        Write the download attachment to disk.
        '''
        path = os.path.join(base_path, self.name)
        with file(path, 'w') as fh:
            fh.write(self.data)
        return True

    def getEtag(self):
        '''
        After the attachment has been downloaded, we can get the etag, which
        contains the MD5 hash (as of December 2014).
        Returns the etag , or ''.
        '''
        if self._download_response:
            return self._download_response.get('etag', '')
        return ''

    def __str__(self):
        return ('<AttachmentDownloadInfo id:%r, name:%r, url:%r, has_data:%r>' %
                (self.id, self.name, self.url, (not self._data is None)))

    def __repr__(self):
        return str(self)



