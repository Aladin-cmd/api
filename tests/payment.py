import pytest

import requests

from setup.setup import session, url


class Test():
    s= requests.session()
    url2="http://stage.geoxhome.com"
    l_data={
        "email":"testaccmail1d@gmail.com",
        "password":"123456"
    }
    login = s.post("{}/api/login".format(url2),data=l_data)

    @pytest.mark.skip
    def test_get_payment(self):
        token = session.cookies.get("token")
        get = session.get("{}/api/payment-method-card".format(url), headers={"token": token})
        print(get.text)


    #@pytest.mark.skip #not for this url
    def test_add_payment_method(self):
        body = {
            "account_holder_name": "Jenny Rosene",
            "account_number": "000123456789",
            "sort_code": "110000000",
            "bank_name": "STRIPE TEST BANK"
        }
        expect = {
            "data": None,
            "msg": "OK",
            "status": 200
        }
        add = session.post("http://stage.geoxhome.com/api/customer/payment-method",json=body)
        print(add.text)

