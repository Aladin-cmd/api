import json
import time

from setup.setup import setup_class, teardown_class, url, session


class Test():
    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    #@pytest.mark.skip
    def test_check_notification(self):
        time.sleep(1)
        token = session.cookies.get("token")
        headers = {
            'token': token
        }
        responseN = {
            "data": {
                "new_notifications_available": False
            },
            "msg": "OK",
            "status": 200
        }
        response = session.get("{}/api/notifications".format(url), headers=headers)
        js = json.loads(response.text)
        assert js == responseN
        duration = response.elapsed.total_seconds()
        assert duration <= 0.5

    def test_fetch_notifications(self):
        time.sleep(1)
        expect = {
            "data": {
                "customer_notifications": []
            },
            "msg": "OK",
            "status": 200
        }
        token = session.cookies.get("token")
        response = session.post("{}/api/notifications".format(url))
        res=json.loads(response.text)
        assert res==expect
        duration = response.elapsed.total_seconds()
        assert duration <= 0.5

    # one more test and complete previos one
    # def test_push_notification(self):
    #     time.sleep(1)
    #     response=session.get("{}/api/push-notifications".format(url))
    #     print(response.text)