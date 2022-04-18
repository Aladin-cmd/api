import time, json

import pytest

from setup.setup import setup_class, teardown_class, session, url


class Test():

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    #@pytest.mark.skip
    def test_add_address(self, create_newp):
        time.sleep(0.8)
        data_project = create_newp
        addresses = {
            "project_id": data_project[0],
            "addresses": [
                {
                    "address": "35 Riverside Rd",
                    "city": "Mesquite",
                    "state": "NV",
                    "zip": "89027"
                },
                {
                    "lat": "27.173722",
                    "long": "-80.145446"
                },
                {
                    "lat": "11.173722"
                },
                {
                    "address": "11 Riverside Rd",
                    "city": "Mesquite",
                    "state": "NV"
                }
            ]
        }
        expect = {
            "data": {
                "duplicate_in_file": 0,
                "duplicate_in_system": 0,
                "invalid_addresses": 2,
                "valid_addresses": 2
            },
            "msg": "OK",
            "status": 200
        }
        add = session.post("{}/api/projects/addresses".format(url), json=addresses)
        add_json = json.loads(add.text)
        assert add_json == expect
        duration = add.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_project_addresses(self, create_newpwith_addresses):  # not complete assertions
        time.sleep(0.8)
        address = create_newpwith_addresses
        response = session.get(
            "{}/api/project/addresses?project_id={}&page_num=1&page_size=3&sort_key=last_updated&sort_direction=down".format(
                url, address[0]))
        d = json.loads(response.text)
        assert response.status_code == 200
        q = len(d["data"]["addresses"])
        assert q > 0
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_get_csv(self, create_newpwith_addresses):
        time.sleep(0.8)
        data = create_newpwith_addresses
        response = session.get("{}/api/project/details/csv?project_id={}".format(url, data[0]))
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "text/csv; charset=utf-8"
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_get_xlsx(self, create_newpwith_addresses):
        time.sleep(0.8)
        data = create_newpwith_addresses
        response = session.get("{}/api/project/details/excel?project_id={}".format(url, data[0]))
        assert response.status_code == 200
        assert response.headers.get(
            "Content-Type") == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_get_address(self, create_newpwith_addresses):
        id = create_newpwith_addresses
        response = session.get(
            "{}/api/project/addresses?project_id={}&page_num=1&page_size=3&sort_key=last_updated&sort_direction=down".format(
                url, id))
        d = json.loads(response.text)
        address_id = d["data"]["addresses"][0]["id"]
        getaddress = session.get("{}/api/project/address?project_id={}&address_id={}".format(url, id, address_id))
        da = json.loads(getaddress.text)
        assert getaddress.status_code == 200

    #@pytest.mark.skip
    def test_upload_project_excel(self, create_newp):  # add negative tests
        time.sleep(0.8)
        data = create_newp
        files = [
            ('file', ('excel_addresses.xlsx', open('tests/u1.xlsx', 'rb'),
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        response = session.post("{}/api/project/upload/excel?project_id={}".format(url, data[0]), files=files)
        expect = {
            "data": {
                "duplicate_in_file": 0,
                "duplicate_in_system": 0,
                "invalid_addresses": 0,
                "valid_addresses": 4
            },
            "msg": "OK",
            "status": 200
        }
        response_json = json.loads(response.text)
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert expect == response_json
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_upload_project_csv(self, create_newp):  # add negative tests
        time.sleep(0.8)
        data = create_newp
        files = [
            ('file', ('address.csv', open('tests/u1.csv', 'rb'), 'text/csv'))
        ]

        response = session.post("{}/api/project/upload/csv?project_id={}".format(url, data[0]), files=files)
        expect = {
            "data": {
                "duplicate_in_file": 0,
                "duplicate_in_system": 0,
                "invalid_addresses": 0,
                "valid_addresses": 4
            },
            "msg": "OK",
            "status": 200
        }
        response_json = json.loads(response.text)
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert expect == response_json
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_get_project_address(self, project_address):
        time.sleep(0.8)
        project_id = project_address[0]
        address_id = project_address[1]
        get = session.get("{}/api/project/address?project_id={}&address_id={}".format(url, project_id, address_id))
        get_json = json.loads(get.text)
        duration = get.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        print(get_json)
        # data={'data': {'address': '35 Riverside Rd', 'city': 'Mesquite', 'id': 'a8187bc3-ef2e-4d11-8b84-86a6fcb82e7b', 'is_approved': False, 'is_complete': True, 'is_favorite': False, 'is_flagged': False, 'last_updated': 'Sun, 17 Apr 2022 17:32:32 GMT', 'lat': '', 'long': '', 'state': 'NV', 'status': '', 'zip': '89027'}, 'msg': 'OK', 'status': 200}
        assert get.status_code == 200
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_delete_address(self, project_address):
        time.sleep(0.8)
        project_id = project_address[0]
        address_id = project_address[1]
        expect = {
            "data": None,
            "msg": "Deleted Successfully",
            "status": 200
        }
        delete = session.delete(
            "{}/api/project/address?project_id={}&address_id={}".format(url, project_id, address_id))
        delete_json = json.loads(delete.text)
        duration = delete.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert delete_json == expect
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_upload_csv_and_excel(self, create_newp):
        time.sleep(0.8)
        data = create_newp

        payload = {'file_keys': 'excel_file,csv_file'}
        files = [
            ('excel_file', (
                'u1.xlsx', open('tests/u1.xlsx', 'rb'),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
            ('csv_file', (
                'u1.csv', open('tests/u1.csv', 'rb'), 'text/csv'))
        ]

        response = session.post("{}/api/v1/project/upload?project_id={}".format(url, data[0]), data=payload,
                                files=files)
        res = json.loads(response.text)
        expect = {
            "data": {
                "duplicate_in_file": 4,
                "duplicate_in_system": 0,
                "invalid_addresses": 0,
                "valid_addresses": 4
            },
            "msg": "OK",
            "status": 200
        }
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert res == expect
        assert duration <= 0.5

    @pytest.mark.skip
    def test_get_filter_val(self, create_newpwith_addresses):
        id = create_newpwith_addresses
        response = session.get("{}/api/address/filter?project_id={}".format(url, id))
        d = json.loads(response.text)
        print(d)
        assert response.status_code == 200
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_filter_user_project_address(self, create_newpwith_addresses):
        time.sleep(0.8)
        project_id=create_newpwith_addresses[0]
        body = {
            "address_search_key": "35",
            "state_values": [
                "NV"
            ],
            "city_values": [
                "Mesquite"
            ],
            "zip_values": [
                "89027"
            ],
            "approved_filter": "all",
            "favorite_filter": "all",
            "sort_key": "address",
            "sort_reverse": True,
            "page_number": 1,
            "page_size": 10
        }
        filter= session.post("{}/api/v1/projects/{}/user-addresses".format(url,project_id),headers={"token":session.cookies.get("token")},data=body)
        filter_json=json.loads(filter.text)
        duration = filter.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert filter.status_code==200
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_filter_values_user_project_addresses(self,create_newpwith_addresses):
        time.sleep(0.8)
        project_id=create_newpwith_addresses[0]
        body={
            "state_values": ["NV"],
            "city_values": ["Mesquite"],
            "zip_values": ["89027"]
        }
        get_f=session.post("{}/api/v1/projects/{}/user-addresses/filter-values".format(url,project_id),headers={"token":session.cookies.get("token")},data=body)
        get_f_json= json.loads(get_f.text)
        expect ={'data': {'city_values': { 'Mesquite': 1}, 'state_values': { 'NV': 1}, 'zip_values': { '89027': 2}}, 'msg': 'OK', 'status': 200}
        duration = get_f.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert get_f.status_code == 200
       # assert expect == get_f_json
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_order_project(self, create_newpwith_addresses):
        headers = {
            "token": session.cookies.get("token")
        }
        id = create_newpwith_addresses[0]
        response = session.post("{}/api/order/place?project_id={}".format(url, id), headers=headers)
        d = json.loads(response.text)
        assert response.status_code == 200
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_order_project_version2(self, create_newpwith_addresses):
        headers = {
            "token": session.cookies.get("token")
        }
        id = create_newpwith_addresses[0]
        response = session.post("{}/api/order/place/v2?project_id={}".format(url, id), headers=headers)
        d = json.loads(response.text)
        assert response.status_code == 200
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5
