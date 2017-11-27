import pytest


@pytest.mark.usefixtures("smart_setup")
class TestRegression:

    def test_passthrough(self, smart_setup):
        smart = smart_setup['smart']

        json = smart.models.JSONObject();
        json.data = {"name": "my new sheet",
                     "columns": [
                         {"title": "Favorite", "type": "CHECKBOX", "symbol": "STAR"},
                         {"title": "Primary Column", "primary": True, "type": "TEXT_NUMBER"}
                     ]
                     }
        json = smart.Passthrough.post('/sheets', json)
        assert json.data['message'] == 'SUCCESS'

        # get the newly created sheet using the passthrough
        json = smart.Passthrough.get('/sheets/' + str(json.data['result']['id']),
                                                  {'include': ['format', 'ownerInfo']})
        assert json.data['id'] is not None

        json = smart.Passthrough.put('/sheets/' + str(json.data['id']),
                                                  smart.models.JSONObject({'name': 'my new new sheet'}))
        assert json.data['message'] == 'SUCCESS'
        assert json.data['result']['name'] == 'my new new sheet'

        json = smart.Passthrough.delete('/sheets/' + str(json.data['result']['id']))
        assert json.data['message'] == 'SUCCESS'
