import json
import time

from setup.setup import teardown_class, setup_class, session, url, data


class Test():
    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    #@pytest.mark.skip
    def test_profile_basic(self):  # +
        time.sleep(1)
        name = "{} {}".format(data.get("first_name"), data.get("last_name"))
        expect = {
            "data": {
                "full_name": name
            },
            "msg": "OK",
            "status": 200
        }
        response = session.get("{}/api/v1/customer/profile/basic".format(url))
        actual = json.loads(response.text)
        duration = response.elapsed.total_seconds()
        assert duration <= 0.5
        assert response.status_code == 200
        assert expect == actual
        print(response.text)

    #@pytest.mark.skip
    def test_get_customer_profile(self):  # +
        time.sleep(1)
        response = session.get("{}/api/customer".format(url))
        res = json.loads(response.text)
        duration = response.elapsed.total_seconds()
        assert response.status_code == 200
        assert res["data"]["active"] == True
        assert res["data"]["active_credits"] > 0
        assert res["data"]["city"] == data.get("city")
        assert res["data"]["company"] == data.get("company")
        assert res["data"]["first_name"] == data.get("first_name")
        assert res["data"]["last_name"] == data.get("last_name")
        assert res["data"]["zip"] == data.get("zip")
        assert res["data"]["work_phone"] == data.get("work_phone")
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_update_user(self):  # +
        time.sleep(1)
        payload = {
            "first_name": "newname",
            "last_name": "newlastname"
        }

        response = session.patch("{}/api/customer".format(url), json=payload)
        d = json.loads(response.text)
        duration = response.elapsed.total_seconds()
        print(d)
        assert response.status_code == 200
        assert d["data"]["first_name"] == payload.get("first_name")
        assert d["data"]["last_name"] == payload.get("last_name")
        assert d["msg"] == "Customer Details Updated"
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_get_picture(self):  # if no picture --> 400
        time.sleep(1)
        payload = {'type': 'profile_pic'}
        files = [
            ('profile', ('user-avatar.png', open('tests/user-avatar.png', 'rb'), 'image/jpeg'))
        ]
        headers = {}

        upload = session.post("{}/api/customer/profile-picture".format(url), headers=headers, data=payload,
                              files=files)

        response = session.get("{}/api/customer/profile-picture".format(url), headers=headers, data=payload)
        duration = response.elapsed.total_seconds()
        assert response.status_code == 200
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_bills(self):  # +
        time.sleep(1)
        response = session.get("{}/api/bills/?page_num=1&page_size=2".format(url))

        print(response.text)
        duration = response.elapsed.total_seconds()
        assert duration <= 0.5
        assert response.status_code == 200
        # need funct

    #@pytest.mark.skip
    def test_update_customers_picture(self):
        time.sleep(1)
        payload = {'type': 'profile_pic'}
        files = [
            ('profile', ('user-avatar.png', open('tests/user-avatar.png', 'rb'), 'image/jpeg'))
        ]
        headers = {}

        response = session.post("{}/api/customer/profile-picture".format(url), headers=headers, data=payload,
                                files=files)

        assert response.status_code == 200
        duration = response.elapsed.total_seconds()
        assert duration <= 0.5
