import time, json, pytest
from setup.setup import setup_class, get_pid, teardown_class, session, url
import datetime

class Test():

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    @pytest.mark.skip
    def test_get_projects(self, create_newp):
        time.sleep(0.8)
        project = create_newp
        response = session.get("{}/api/projects".format(url))
        d = json.loads(response.text)
        assert response.status_code == 200
        assert d["data"]["total_projects"] > 0
        assert d["data"]["projects"][0]["project_name"] == project[1]
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_get_project_details(self, create_newpwith_addresses):
        time.sleep(0.8)
        data = create_newpwith_addresses
        response = session.get("{}/api/project/details?project_id={}&response_type=list".format(url, data[0]))
        d = json.loads(response.text)
        assert response.status_code == 200
        assert d["data"]["addresses_in_project"] > 0
        # assert d["data"]["project_name"] ==data[0]
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_check_project_name(self, create_newp):  ##add negative test if project is not unique
        time.sleep(0.8)
        expect = {
            "data": {
                "is_project_name_unique": True
            },
            "msg": "OK",
            "status": 200
        }
        project = create_newp
        check = session.get("{}/api/v1/projects/check-name?project_name={}".format(url, project[1]))
        check_json= json.loads(check.text)
        print(check_json)
        assert expect==check_json
        duration = check.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5


    @pytest.mark.skip
    def test_project_exist(self, create_newpwith_addresses):
        time.sleep(0.8)
        id = create_newpwith_addresses
        data_response = {
            "data": {
                "project_exists": True
            },
            "msg": "OK",
            "status": 200
        }
        token = session.cookies.get("token")
        response = session.get("{}/api/v1/customer/project-exists".format(url),headers={"token":token})
        d = json.loads(response.text)
        assert response.status_code == 200
        assert d == data_response
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_project_stats(self, create_newpwith_addresses):
        time.sleep(0.8)
        data = create_newpwith_addresses
        response = session.get("{}/api/v1/project/{}/stats".format(url, data[0]))
        d = json.loads(response.text)
        assert response.status_code == 200
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_search_via_address(self, create_newpwith_addresses):
        time.sleep(0.8)
        data = create_newpwith_addresses
        search = "35 Riverside Rd"
        response = session.get("{}/api/v1/projects/search-via-address?search_text={}".format(url, search))
        d = json.loads(response.text)
        print(d)
        assert response.status_code == 200
        assert d["data"]["projects"][0]["addresses_in_project"] > 0
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    n = str(datetime.date)
    data_newp = [
        ("{}-test".format(n), "OK", 200)
        # ("{}-test".format(n), "OK", 200),
        # ("duplicate", "Project with given name already exists!", 400),
        # ("", "", 400)
    ]
    @pytest.mark.skip
    @pytest.mark.parametrize("name, msg, status", data_newp)
    def test_create_project(self, name, msg, status):
        time.sleep(0.8)
        session.post("{}/api/projects".format(url), json={"project_name": "duplicate"})
        response = session.post("{}/api/projects".format(url), json={"project_name": name})
        d = json.loads(response.text)
        assert d["msg"] == msg
        assert name == d["data"]["project_name"]
        assert response.status_code == status
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_delete_project(self):
        time.sleep(0.8)
        n_p = str(datetime.time)
        session.post("{}/api/projects".format(url), json={"project_name": "{}-project".format(n_p)})
        before = get_pid()
        after = []
        token = session.cookies.get("token")
        headers = {
            'token': token
        }
        idlist = get_pid()
        for id in idlist:
            response = session.delete("{}/api/v1/projects/{}".format(url, id), headers=headers)
            print(response.text)
        after = get_pid()
        print(before)
        print(after)
        assert before != after
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5

    @pytest.mark.skip
    def test_update_project_order(self):
        time.sleep(0.8)
        projects = [
            {"project_name": "test1"},
            {"project_name": "test3"},
            {"project_name": "test2"}
        ]
        ordered = []
        unordered = []
        temp=[]
        for e in range(len(projects)):
            session.post("{}/api/projects".format(url), json=projects[e])
            unordered = get_pid()
        expected = {
            "data": None,
            "msg": "OK",
            "status": 200
        }
        temp.extend(unordered)
        temp.sort()
        response = session.post("{}/api/v1/customer/projects-order".format(url), json={"projects_order": temp})
        ordered = get_pid()
        print(ordered)
        print(unordered)
        assert response.status_code==200
        assert ordered == temp
        assert unordered != ordered
        duration = response.elapsed.total_seconds()
        print("Duration is: {}".format(duration))
        assert duration <= 0.5
