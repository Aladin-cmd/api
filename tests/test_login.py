import json
import time
import pytest
import requests
from tests.conftest import url

class Tests:

    body={
        "valid_user":
            {
                "email": "sund@gmail.com",
                "password": "123"
            },
        "non-ex_user":
            {
                "email": "notthere@gmail.com",
                "password": "123456"
            },
        "no_email":
            {
                "email": "",
                "password": "123456"
            },
        "no_password":
            {
                "email": "sund@gmail.com",
                "password": ""
            },
        "empty_full":
            {
                "email": "",
                "password": ""
            },
        "wrong_email_format":
            {
                "email": "sund.com",
                "password": "123456"
            },
        "wrong_password":
            {
                "email": "sund@gmail.com",
                "password": "234521323"
            }
    }

    #create test data for login user
    data = [(body.get("valid_user"), 200, "OK"),
            (body.get("non-ex_user"), 400, "No customer found with given email"),
            (body.get("wrong_password"), 400, "Incorrect email/password"),
            (body.get("no_email"), 400, "Required parameters missing"),
            (body.get("no_password"), 400, "Required parameters missing"),
            (body.get("empty_full"), 400, "Required parameters missing"),
            (body.get("wrong_email_format"), 400, "No customer found with given email")
            ]
    @pytest.mark.parametrize("payload, status, msg", data)
    def test_login(self, payload, status, msg):
        time.sleep(0.5)
        response = requests.post("{}/api/login".format(url), json=payload)
        json_response = json.loads(response.text)
        assert response.status_code == status
        assert json_response["msg"] == msg
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5
        #redirect after login

    def test_logout(self):
        expect = {
            "data": None,
            "msg": "You are logged out successfully",
            "status": 200
        }
        session= requests.session()
        response = session.post("{}/api/login".format(url), json={"email":"sund@gmail.com","password":"123"})
        token = session.cookies.get("token")
        resp_logout = session.post("{}/api/auth/logout".format(url), headers={"token": token})
        actual=json.loads(resp_logout.text)
        assert resp_logout.status_code == 200
        assert expect == actual






