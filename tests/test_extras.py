import json
import time

import pytest

from setup.setup import setup_class, teardown_class, url, session


class Test():

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    def test_report_types(self):
        time.sleep(0.8)
        token = session.cookies.get("token")
        get = session.get("{}/api/report_types".format(url), headers={"token": token})
        get_data = json.loads(get.text)
        for repo in range(len(get_data["data"]["report_types"])):
            assert get_data["data"]["report_types"][repo]["reporting_class_name"] in ["Professional", "Basic",
                                                                                      "Advanced"]
            print(get_data["data"]["report_types"][repo]["reporting_class_name"])
        assert get.status_code == 200
        duration = get.elapsed.total_seconds()
        assert duration <= 0.5

    def test_image_provider(self):
        time.sleep(1)
        get = session.get("{}/api/image-providers".format(url))
        print(get.text)
        get_data = json.loads(get.text)
        for repo in range(len(get_data["data"]["image_providers"])):
            assert get_data["data"]["image_providers"][repo]["image_provider_name"] in ["Image provider 1",
                                                                                        "Image provider 2"]
            print(get_data["data"]["image_providers"][repo]["image_provider_name"])
        assert get.status_code == 200
        duration = get.elapsed.total_seconds()
        assert duration <= 0.5

    def test_get_api_docs(self):
        time.sleep(1)
        get_api = session.get("{}/api/v1/docs".format(url))
        assert get_api.status_code == 200
        duration = get_api.elapsed.total_seconds()
        assert duration <= 0.5

    @pytest.mark.skip
    def test_contact_us(self):
        pass

    def test_get_api_key(self):
        time.sleep(1)
        get_customer_data = session.get("{}/api/customer".format(url))
        customer_data = json.loads(get_customer_data.text)
        api_key_old = customer_data["data"]["api_key"]
        api_secret_old = customer_data["data"]["api_secret"]
        new_api_key = session.post("{}/api/customer/generate-key".format(url), json={
            "renew": False
        })
        new_cust_data=json.loads(new_api_key.text)
        api_key_new=new_cust_data["data"]["api_key"]
        api_secret_new=new_cust_data["data"]["api_secret"]
        print(customer_data)
        print(new_cust_data)
        assert api_secret_new!=api_secret_old
        assert api_key_new!=api_key_old
        duration = new_api_key.elapsed.total_seconds()
        assert duration <= 0.5
    @pytest.mark.skip
    def test_validate_coupon(self):
        pass