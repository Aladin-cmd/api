import pytest
from setup.setup import setup_class, teardown_class, session, url


class Test():

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    @pytest.mark.skip
    def test_get_address_building(self, create_project_and_order):
        id = create_project_and_order
        get = session.get("{}/api/project/address/buildings?project_id={}&address_id=1".format(url, id))
        print(get.text)

    def test_get_address_insights(self):
        body = {
            "lat": 31.0514132,
            "lng": -85.8993835
        }
        response = session.post("{}/api/v1/location-insights".format(url), json=body)
        print(response.text)
