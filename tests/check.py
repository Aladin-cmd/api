from setup.setup import setup_class, teardown_class, session, url
import json, time


class Test():
    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    def test_getprojects(self, create_project):
        time.sleep(0.5)
        response = session.get("{}/api/projects".format(url))
        json_response = json.loads(response.text)
        print(json_response)