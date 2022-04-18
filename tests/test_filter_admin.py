import json
import time

import pytest
import requests

from setup.setup import url

session = requests.session()


class Test():
    @classmethod
    def setup_class(cls):
        login = session.post("{}/api/v1/admin/login".format(url), json={"email": "test@test.cc", "password": "123456"})
        print("setup!!!!")

    @classmethod
    def teardown_class(cls):
        logout = session.post("{}/api/auth/logout".format(url), headers={"token": session.cookies.get("token")})
        print("teardown~~~")

    @pytest.mark.skip
    def test_filter_customers(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "filters": {
                "first_name": "Marko",
                "active_credits": {
                    "min": 0

                }
            }
        }
        customer = session.post("{}/api/v1/admin/customers/filter".format(url), json=filter_data)
        print(customer.text)

    @pytest.mark.skip
    def test_filter_customers(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "search_query": "",
            "filters": {
                "status": ["progress"]
            }
        }
        customer = session.post("{}/api/v1/admin/projects/filter".format(url), json=filter_data)
        print(customer.text)

    @pytest.mark.skip
    def test_filter_orders(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "search_query": "",
            "filters": {
                "order_status": ["finished"]
            }
        }
        customer = session.post("{}/api/v1/admin/orders/filter".format(url), json=filter_data)
        print(customer.text)

    @pytest.mark.skip
    def test_filter_contact_us_record(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "search_query": "",
            "filters": {
                "first_name": "Nitin",
                "text": "enterprise",
                "company": ["GeoX"]
            }
        }
        customer = session.post("{}/api/v1/admin/contact-us/filter".format(url), json=filter_data)
        print(customer.text)

    @pytest.mark.skip
    def test_filter_coupons(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "search_query": "GEOX_15",
            "filters": {
                "discount_type": ["percentage"],
                "is_active": [True],
                "max_apply_count": {
                    "min": 100,
                    "max": 200
                },
                "discount_value": {
                    "min": 10,
                    "max": 20
                },
                "end_date": {
                    "min": "2021-01-31",
                    "max": "2022-07-01"
                }

            }
        }
        customer = session.post("{}/api/v1/admin/coupons/filter".format(url), json=filter_data)
        print(customer.text)

    @pytest.mark.skip
    def test_filter_login_activity(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "search_query": "test@test.cc",
            "filters": {
                "customer_first_name": "Nitin",
                "customer_email": "test@test.cc",
                "customer_last_name": "Chetwani",
                "current_sign_in_ip_address": "195.22",
                "previous_sign_in_ip_address": "195.192",
                "current_sign_in_date": {
                    "min": "2021-07-01",
                    "max": "2021-09-15"
                },
                "previous_sign_in_date": {
                    "min": "2021-07-01",
                    "max": "2021-09-08"
                },
                "sigin_in_count": {
                    "min": 2,
                    "max": 100
                }
            }
        }
        customer = session.post("{}/api/v1/admin/login-activity/filter".format(url), json=filter_data)
        print(customer.text)

    @pytest.mark.skip
    def test_filter_login_activity(self):
        filter_data = {
            "page_num": 1,
            "page_size": 30,
            "search_query": "test@test.cc",
            "filters": {
                "customer_first_name": "Nitin",
                "customer_email": "test@test.cc",
                "customer_last_name": "Chetwani",
                "status": [
                    "Success"
                ],
                "subscription_type": [
                    "Monthly"
                ],
                "plan_name": [
                    "Business",
                    "Starter"
                ],
                "purchase_date": {
                    "min": "2021-07-01",
                    "max": "2021-10-01"
                }
            }
        }
        customer = session.post("{}/api/v1/admin/bill/filter".format(url), json=filter_data)
        print(customer.text)
