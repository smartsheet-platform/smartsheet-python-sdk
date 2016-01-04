import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestServerInfo:

    def test_server_info(self, smart_setup):
        smart = smart_setup['smart']
        info = smart.Server.server_info()
        assert 'en_US' in info.supported_locales