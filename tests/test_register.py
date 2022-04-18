import json

import pytest
import requests
from setup.setup import url


class Test():
    # Out of which following fields are mandatory:
    # city
    # billing_address
    # password
    # organization
    # company
    # zip
    # work_phone
    # country
    # first_name
    # email
    # last_name
    new_user_data = {
        "valid_user":
            {
                "password": "123456",
                "first_name": "James",
                "last_name": "Lastname",
                "email": "james@gmail.com",
                "organization": "Think&Co.",
                "billing_address": "somewhere",
                "work_phone": "9166123456",
                "company": "Think&Co.",
                "city": "Lisad",
                "country": "Canada",
                "zip": "77020"
            },
        "no_email":
            {
                "password": "123456",
                "first_name": "James",
                "last_name": "Lastname",
                "email": "",
                "organization": "Think&Co.",
                "billing_address": "somewhere",
                "work_phone": "9166123456",
                "company": "Think&Co.",
                "city": "Lisad",
                "country": "Canada",
                "zip": "77020"
            }

    }

    data = [(new_user_data.get("valid_user"), 200),
            (new_user_data.get("no_email"), 400)
            ]

    @pytest.mark.parametrize("payload, status", data)
    def test_registration(self,payload,status):

        session = requests.session()

        new_user = session.post("{}/api/register".format(url), json=payload)
        print(new_user.text)
        user_json=json.loads(new_user.text)
        response = json.loads(new_user.text)
        print(response)
        duration = new_user.elapsed.total_seconds()
        assert new_user.status_code==status
        assert duration <= 0.5
        if new_user.status_code == 200:
            print(response)
            id = response["data"]["id"]
            print(id)
            delete = session.delete("{}/api/delete/customer/{}".format(url, id))
            assert delete.status_code == 204
            print("User was deleted")
        else:
            print("User wasn`t created")
            print(response)
