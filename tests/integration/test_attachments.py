import pytest
import smartsheet
import os.path
import threading

_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.usefixtures("smart_setup")
class TestAttachments:
    row_url_attachment = None
    sheet_file_attachment = None

    # SEE TestDiscussions for this test
    # def test_attach_url_to_comment(self, smart_setup):
    #     smart = smart_setup['smart']

    def test_get_to_rate_limit(self, smart_setup):
        smart = smart_setup['smart']

        class loop_thread(threading.Thread):
            def __init__(self, counter):
                threading.Thread.__init__(self)
                self.counter = counter

            def run(self):
                print("Starting " + self.name)
                loop_call(self.counter)
                print("Exiting " + self.name)

        def loop_call(count):
            for x in range(0,count):
                action = smart.Sheets.get_sheet_version(smart_setup['sheet'].id)
                if action.request_response is None or action.request_response.status_code != 200:
                    return

        threadLock = threading.Lock()
        threads = []

        for x in range(0, 5):
            thread1 = loop_thread(100)
            threads.append(thread1)

        for t in threads:
            t.start()

        x = 0
        for t in threads:
            x = x + 100
            t.join()

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
