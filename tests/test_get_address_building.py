import pytest
from setup.setup import setup_class, teardown_class, session, url


class Test():
    @pytest.mark.skip
    def test_get_building(self):
        session.post("{}/api/login".format(url), json={"email": "test@test.cc", "password": "123456"})
        get = session.get(
            "{}/api/project/address/buildings?project_id=5fc8be0ad3d13599fc6127e5&address_id=59".format(url))
        print(get.text)

    @pytest.mark.skip
    def test_export_parcel_address_record(self):
        session.post("{}/api/login".format(url), json={"email": "test@test.cc", "password": "123456"})
        export = session.get("{}/api/v1/parcels/59/export".format(url))
        print(export.text)

    @pytest.mark.skip
    def test_filter_project_addresses_basic(self):
        session.post("{}/api/login".format(url), json={"email": "test@test.cc", "password": "123456"})
        body = {
            "filters": {
                "roof_type": ["Mix "],
                "roof_condition": ["UNKNOWN"],
                "pool": False,
                "lot_size": {
                    "min": 1000
                },
                "is_approved": False,
                "is_unusual": False
            }
        }
        filter = session.post("{}/api/project/addresses-filtered?project_id=5fc8be0ad3d13599fc6127e5".format(url),data=body)
        print(filter.text)

    def test_filtered_detail(self):
        session.post("{}/api/login".format(url), json={"email": "test@test.cc", "password": "123456"})
        body = {
            "filters": {
                "roof_type": ["Mix "],
                "roof_condition": ["UNKNOWN"],
                "pool": False,
                "lot_size": {
                    "min": 1000
                },
                "is_approved": False,
                "is_unusual": False
            }
        }
        filter = session.post("{}/api/project/addresses-filtered-detail?project_id=5fc8be0ad3d13599fc6127e5".format(url),
                              data=body)
        print(filter.text)
