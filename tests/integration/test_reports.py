import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestReports:
    reports = None
    share = None
    shares = None

    def test_list_reports(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Reports.list_reports(page_size=20, page=1)
        assert action.request_response.status_code == 200
        TestReports.reports = action.result

    def test_get_report(self, smart_setup):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.get_report(
                TestReports.reports[0].id
            )
            assert isinstance(action, smart.models.Report)
        except IndexError:
            pytest.skip('no reports in test account')

    @pytest.mark.usefixtures('tmpdir')
    def test_get_report_as_csv(self, smart_setup, tmpdir):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.get_report_as_csv(
                TestReports.reports[0].id,
                tmpdir.strpath
            )
            assert action.message == 'SUCCESS'
            assert isinstance(action, smart.models.DownloadedFile)
        except IndexError:
            pytest.skip('no reports in test account')

    @pytest.mark.usefixtures('tmpdir')
    def test_get_report_as_excel(self, smart_setup, tmpdir):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.get_report_as_excel(
                TestReports.reports[0].id,
                tmpdir.strpath
            )
            assert action.message == 'SUCCESS'
            assert isinstance(action, smart.models.DownloadedFile)
        except IndexError:
            pytest.skip('no reports in test account')

    def test_send_report(self, smart_setup):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.send_report(
                TestReports.reports[0].id,
                smart.models.SheetEmail({
                    'send_to': smart.models.Recipient({
                        'email': 'john.doe@smartsheet.com'
                    }),
                    'subject': 'Get a load of report!',
                    'format': 'PDF',
                    'format_details': smart.models.FormatDetails({
                        'paper_size': 'WIDE'
                    }),
                    'message': 'You will love this.',
                    'ccMe': False
                })
            )
            assert action.message == 'SUCCESS'
        except IndexError:
            pytest.skip('no reports in test account')

    def test_share_report(self, smart_setup):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.share_report(
                TestReports.reports[0].id,
                smart.models.Share({
                    'access_level': 'EDITOR',
                    'email': smart_setup['users']['larry'].email
                })
            )
            assert action.message == 'SUCCESS'
            TestReports.share = action.result
        except IndexError:
            pytest.skip('no reports in test account')

    def test_list_shares(self, smart_setup):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.list_shares(
                TestReports.reports[0].id
            )
            assert action.total_count > 0
            TestReports.shares = action.result
        except IndexError:
            pytest.skip('no reports found in test account')

    def test_get_share(self, smart_setup):
        smart = smart_setup['smart']
        try:
            share = smart.Reports.get_share(
                TestReports.reports[0].id,
                TestReports.share.id
            )
            assert isinstance(share, smart.models.Share)
        except IndexError:
            pytest.skip('no reports found in test account')

    def test_update_share(self, smart_setup):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.update_share(
                TestReports.reports[0].id,
                TestReports.share.id,
                smart.models.Share({
                    'access_level': 'EDITOR_SHARE'
                })
            )
            assert action.message == 'SUCCESS'
        except IndexError:
            pytest.skip('no reports found in test account')

    def test_delete_share(self, smart_setup):
        smart = smart_setup['smart']
        try:
            action = smart.Reports.delete_share(
                TestReports.reports[0].id,
                TestReports.share.id,
            )
            assert action.message == 'SUCCESS'
        except IndexError:
            pytest.skip('no reports found in test account')
