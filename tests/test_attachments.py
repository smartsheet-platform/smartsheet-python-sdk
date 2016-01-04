import pytest
import smartsheet
import os.path

_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.usefixtures("smart_setup")
class TestAttachments:
    row_url_attachment = None
    sheet_file_attachment = None

    # SEE TestDiscussions for this test
    # def test_attach_url_to_comment(self, smart_setup):
    #     smart = smart_setup['smart']

    def test_attach_url_to_sheet(self, smart_setup):
        smart = smart_setup['smart']
        url = smart.models.Attachment({
            'name': 'find stuff',
            'description': 'Maybe you have heard of this.',
            'url': 'http://www.google.com/',
            'attachment_type': 'LINK'
        })
        action = smart_setup['sheet_b'].attach_url(url)
        assert action.message == 'SUCCESS'

    def test_attach_url_to_row(self, smart_setup):
        smart = smart_setup['smart']
        url = smart.models.Attachment({
            'name': 'find stuff',
            'description': 'Maybe you have heard of this.',
            'url': 'http://www.google.com/',
            'attachment_type': 'LINK'
        })
        action = smart.Attachments.attach_url_to_row(
            smart_setup['sheet_b'].id,
            smart_setup['sheet_b'].rows[0].id,
            url
        )
        assert action.message == 'SUCCESS'
        TestAttachments.row_url_attachment = action.result

    def test_attach_file_to_sheet(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.attach_file_to_sheet(
            smart_setup['sheet_b'].id,
            ('stooges.jpg', open(_dir + '/fixtures/stooges_v1.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'
        TestAttachments.sheet_file_attachment = action.result

    def test_list_all_attachments(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.list_all_attachments(
            smart_setup['sheet_b'].id
        )
        assert action.total_count > 0

    def test_attach_new_version(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.attach_new_version(
            smart_setup['sheet_b'].id,
            TestAttachments.sheet_file_attachment.id,
            ('stooges.jpg', open(_dir + '/fixtures/stooges_v2.jpg', 'rb'), 'image/jpeg')
        )
        assert action.message == 'SUCCESS'

    def test_list_attachment_versions(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.list_attachment_versions(
            smart_setup['sheet_b'].id,
            TestAttachments.sheet_file_attachment.id
        )
        assert action.total_count > 0
        vlist = action.result
        assert isinstance(action.result[0], smart.models.attachment.Attachment)

    def test_delete_attachment(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.delete_attachment(
            smart_setup['sheet_b'].id,
            TestAttachments.row_url_attachment.id
        )
        assert action.message == 'SUCCESS'

    def test_get_attachment(self, smart_setup):
        smart = smart_setup['smart']
        file = smart.Attachments.get_attachment(
            smart_setup['sheet_b'].id,
            TestAttachments.sheet_file_attachment.id
        )
        assert file.name == 'stooges.jpg'

    def test_delete_attachment_versions(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Attachments.delete_attachment_versions(
            smart_setup['sheet_b'].id,
            TestAttachments.sheet_file_attachment.id
        )
        assert action.message == 'SUCCESS'
