import json
from setup.setup import setup_class, teardown_class, session, url


class Test():

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    def test_get_filters(self, create_filter):
        data = create_filter
        print(data[0])
        get = session.get("{}/api/v1/customer/saved-filters?project_id={}".format(url, data[2]))
        r = json.loads(get.text)
        r2 = data[0]
        print(r)
        fname1 = r["data"]["saved_filters"][0]["filter_name"]
        is_common1 = r["data"]["saved_filters"][0]["is_common"]
        fname2 = r2["filter_name"]
        is_common2 = r2["is_common"]
        assert fname2 == fname1
        assert is_common2 == is_common1
        assert get.status_code == 200

    def test_addfilter(self, create_filter):
        create = create_filter[1]
        assert create["msg"] == "OK"
        assert create["status"] == 201

    def test_update_filter(self, create_filter):
        create = create_filter
        filter_id = create[1]["data"]["id"]
        body = {
            "filter_name": "Updated Buildings Filter",
            "filter_data": {
                "easy_filters": {
                    "address_search_key": "new_search_key",
                    "city_values": [
                        "new_cities"
                    ],
                    "state_values": [
                        "new_states"
                    ],
                    "zip_values": [
                        "new_zips"
                    ]
                },
                "advanced_filters": None
            },
            "is_common": True
        }
        update = session.patch("{}/api/v1/customer/saved-filters/{}".format(url, filter_id),json=body)
        response = json.loads(update.text)
        print(response)
        assert update.status_code==200
        assert response["data"]["filter_name"]==body.get("filter_name")
        assert response["data"]["is_common"]== body.get("is_common")


    def test_delete_filter(self, create_filter):
        create = create_filter
        filter_id = create[1]["data"]["id"]
        delete =session.delete("{}/api/v1/customer/saved-filters/{}".format(url,filter_id))
        assert delete.status_code==204
