import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestZSearch:
    """Sometimes these pass, sometimes they don't.
    As the documentation says, items recently created may not
    be searchable right away.
    So, we test for successful request, successful creation of
    SearchResult object, and that's it.
    Non-automated testing can be used with these two methods
    to ensure functionality.
    """

    def test_search_sheet(self, smart_setup):
        smart = smart_setup['smart']
        result = smart.Search.search_sheet(
            smart_setup['sheet_b'].id,
            'Nike'
        )
        assert result.request_response.status_code == 200
        assert result.total_count >= 0
        assert isinstance(result, smart.models.search_result.SearchResult)

    def test_search(self, smart_setup):
        smart = smart_setup['smart']
        result = smart.Search.search('Google')
        assert result.request_response.status_code == 200
        assert result.total_count >= 0
        assert isinstance(result, smart.models.search_result.SearchResult)
