import json
import time
import pytest
import requests

from setup.setup import setup_class, teardown_class, url, session, email


class Test():
    with open(r"D:\python\api_testing\JSON_info_for_tests\passwords") as jsonFile:
        ps = json.load(jsonFile)
        jsonFile.close()
    data = [
        (ps["valid_update"], 200, "Password Updated successfully"),
        (ps["old_password_wrong"], 400, "You have entered incorrect password"),
        (ps["equal_new_and_old"], 400, "Old password and current passwords are same")
    ]

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    @pytest.mark.skip
    @pytest.mark.parametrize("payload, status, msg", data)
    def test_updatepassword(self, payload, status, msg):
        time.sleep(0.8)
        response = session.post("{}/api/customer/password".format(url), json=payload)
        json_response = json.loads(response.text)
        assert response.status_code == status
        assert json_response["msg"] == msg
        duration = response.elapsed.total_seconds()
        print("\n" + str(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_refreshtoken(self):
        time.sleep(0.8)
        refresh = session.cookies.get("refresh_token")
        r = {
            "data": None,
            "msg": "OK",
            "status": 200
        }
        resp_t = session.post("{}/api/auth/refresh-token".format(url), headers={"token": refresh})
        d = json.loads(resp_t.text)
        assert d == r
        assert resp_t.status_code == 200
        duration = resp_t.elapsed.total_seconds()
        print("\n" + str(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_send_email(self):
        send = requests.post("{}/api/v1/auth/send-reset-password-email".format(url), json={"email": email})
        r = {
            "data": None,
            "msg": "An email will be sent to given email id if it exists in our database. Please follow that for further instructions",
            "status": 200
        }
        d = json.loads(send.text)
        assert r == d
        duration = send.elapsed.total_seconds()
        print("\n" + str(duration))
        assert duration <= 0.5

    @pytest.mark.skip  # ??
    def test_validate_assert_ps_token(self):
        token = session.cookies.get("token")
        data = {
            "data": {
                "token": token
            },
            "msg": "OK",
            "status": 200
        }
        response = session.post("{}/api/v1/auth/validate-reset-password-token".format(url), json={"token": token})
        d = json.loads(response.text)
        print(d)
        assert response.status_code == 200
        duration = response.elapsed.total_seconds()
        print("\n" + str(duration))
        assert duration <= 0.5
    @pytest.mark.skip #???
    def test_login_with_google(self):
        payload = {
            "auth_code": "4/0AX4XfWhWW7hiFD0Q3IhCiuqVAGwMW9_2bfiaxITIjsqfxA8YO35JLK9anfLFNUnwhY1VrA"
        }
        google = requests.post("{}/api/connect/google".format(url), json=payload)
        expect = {
            "data": None,
            "msg": "OK",
            "status": 200
        }
        google_json= json.loads(google.text)
        print(google_json)
        assert expect==google_json
