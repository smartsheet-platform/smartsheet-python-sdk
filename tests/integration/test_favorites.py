import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestFavorites:

    def test_add_favorites(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Favorites.add_favorites([
            smart.models.Favorite({
                'object_id': smart_setup['folder'].id,
                'type': 'folder'
            }),
            smart.models.Favorite({
                'object_id': smart_setup['sheet'].id,
                'type': 'sheet'
            })
        ])
        favs = action.result
        assert action.message == 'SUCCESS'

    def test_list_favorites(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Favorites.list_favorites()
        favs = action.result
        assert action.request_response.status_code == 200
        assert action.total_count > 0
        assert isinstance(favs[0], smart.models.favorite.Favorite)

    def test_remove_favorites(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Favorites.remove_favorites('sheet', smart_setup['sheet'].id)
        assert action.message == 'SUCCESS'