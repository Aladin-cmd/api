import json
import time

import pytest
import requests

from setup.setup import url

session= requests.session()
class Test():
    @classmethod
    def setup_class(cls):
        login=session.post("{}/api/v1/admin/login".format(url),json={"email":"test@test.cc","password":"123456"})
        print("setup!!!!")

    @classmethod
    def teardown_class(cls):
        logout= session.post("{}/api/auth/logout".format(url),headers={"token":session.cookies.get("token")})
        print("teardown~~~")


    #@pytest.mark.skip
    def test_fetch_customers(self):
        time.sleep(0.8)
        customers = session.get("{}/api/v1/admin/customers?page_num=1&page_size=10".format(url))
        customers_json = json.loads(customers.text)
        #print(customers_json)
        duration = customers.elapsed.total_seconds()
        assert customers.status_code==200
        assert duration <= 0.5

    #@pytest.mark.skip
    def test_fetch_plans(self):
        time.sleep(0.8)
        plans =session.get("{}/api/v1/admin/plans".format(url))
        plans_json=json.loads(plans.text)
        #print(plans_json)
        duration = plans.elapsed.total_seconds()
        assert plans.status_code == 200
        assert duration <= 0.5

    def test_fetch_projects(self):
        time.sleep(0.8)
        projects = session.get("{}/api/v1/admin/projects?page_num=1&page_size=10".format(url))
        projects_json = json.loads(projects.text)
        #print(projects_json)
        duration = projects.elapsed.total_seconds()
        assert projects.status_code == 200
        assert duration <= 0.5

    def test_fetch_orders(self):
        time.sleep(0.8)
        orders = session.get("{}/api/v1/admin/orders?page_num=1&page_size=10".format(url))
        orders_json = json.loads(orders.text)
        #print(orders_json)
        duration = orders.elapsed.total_seconds()
        assert orders.status_code == 200
        assert duration <= 0.5

    def test_fetch_contact_us_records(self):
        time.sleep(0.8)
        cus = session.get("{}/api/v1/admin/contact-us".format(url))
        cus_json = json.loads(cus.text)
        #print(cus_json)
        duration = cus.elapsed.total_seconds()
        assert cus.status_code == 200
        assert duration <= 0.5

    def test_fetch_coupons(self):
        time.sleep(0.8)
        coupons = session.get("{}/api/v1/admin/coupons?page_num=1&page_size=10".format(url))
        cus_json = json.loads(coupons.text)
        #print(cus_json)
        duration = coupons.elapsed.total_seconds()
        assert coupons.status_code == 200
        assert duration <= 0.5

    def test_fetch_login(self):
        time.sleep(0.8)
        activity = session.get("{}/api/v1/admin/login-activity".format(url))
        l_json = json.loads(activity.text)
        #print(l_json)
        duration = activity.elapsed.total_seconds()
        assert activity.status_code == 200
        assert duration <= 0.5

    def test_bills(self):
        time.sleep(0.8)
        bill = session.get("{}/api/v1/admin/bill".format(url))
        l_json = json.loads(bill.text)
        #print(l_json)
        duration = bill.elapsed.total_seconds()
        assert bill.status_code == 200
        assert duration <= 0.5
