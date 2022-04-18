import datetime
import time
import sys,os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(r"setup\setup.py")))
sys.path.insert(0, BASE)
from setup.setup import *

url = "http://stage.geoxanalytics.com"


def create_projectwithaddress():
    headers = {
        'token': session.cookies.get("token")
    }
    payload = [
        {"project_name": "test1"},
        {"project_name": "test2"},
        {"project_name": "test3"},
        {"project_name": "test4"},
        {"project_name": "test5"}
    ]
    js_response = []
    for p in range(len(payload)):
        response_p = session.post("{}/api/projects".format(url), headers=headers, json=payload[p])
        js_response.append(json.loads(response_p.text))
        list_id = get_pid()
        resaddress = []
        for er in list_id:
            cr = session.post("{}/api/projects/addresses".format(url), json={"project_id": str(er),
                                                                             "addresses": address
                                                                             })
            resaddress.append(json.loads(cr.text))

    return ({resaddress, js_response})  # 0->detailed 1-> only project


def deleteprojects():
    res = []
    token = session.cookies.get("token")
    headers = {
        'token': token
    }
    idlist = get_pid()
    for id in idlist:
        response = session.delete("{}/api/v1/projects/{}".format(url, id), headers=headers)
        print(response.text)
        res.append(response.text)
    return res


@pytest.fixture(scope="function")
def create_project():
    result = create_projectwithaddress()
    return result
    delete_project()


@pytest.fixture()
def create_newp():
    headers = {
        'token': session.cookies.get("token")
    }
    a=random_email(5);
    name="testnameproject1{}".format(a)
    payload = {"project_name": name}
    response_p = session.post("{}/api/projects".format(url), headers=headers, json=payload)
    res = json.loads(response_p.text)
    id = res["data"]["id"]
    project_name=res["data"]["project_name"]
    return [id,project_name]
    delete = session.delete("{}/api/v1/projects/{}".format(url,id),headers=headers)


@pytest.fixture(scope="class")
def create_newpwith_addresses():
    word = str(datetime.date)
    name = "{}-new project".format(word)
    headers = {
        'token': session.cookies.get("token")
    }
    payload = {"project_name": name}
    response_p = session.post("{}/api/projects".format(url), headers=headers, json=payload)
    data = json.loads(response_p.text)
    id = data["data"]["id"]
    cr = session.post("{}/api/projects/addresses".format(url), json={"project_id": str(id),
                                                                     "addresses": address
                                                                     })
    return [id,name]
    delete = session.delete("{}/api/v1/projects/{}".format(url,id),headers=headers)

@pytest.fixture()
def project_address(create_newpwith_addresses):
    project_id=create_newpwith_addresses[0]
    header={"token":session.cookies.get("token")}
    get_addresses= session.get("{}/api/project/addresses?project_id={}&page_num=1&page_size=3&sort_key=last_updated&sort_direction=down".format(url,project_id),headers=header)
    get_addresses_json= json.loads(get_addresses.text)
    address_id=get_addresses_json["data"]["addresses"][0]["id"]
    return [project_id,address_id]


@pytest.fixture(scope="class")
def get_card_id():
    body = {
        "account_holder_name": "Jenny Rosen",
        "account_number": "000123456789",
        "sort_code": "110000000",
        "bank_name": "STRIPE TEST BANK"
    }
    response = session.post("{}/api/customer/payment-method".format(url), json=body)
    card_id = []
    if response.status_code == 200:
        token = session.cookies.get("token")
        headers = {
            'token': token
        }
        get = session.get("{}/api/payment-method-card".format(url), headers=headers)
        data = json.loads(get.text)
        arr = data["data"]

        for d in range(len(arr)):
            card_id.append(arr[d]["card_id"])
    else:
        print("Something went wrong...")
        print(response.text)
    return card_id


@pytest.fixture(scope="class")
def create_filter():
    name = str(datetime.date)
    headers = {
        'token': session.cookies.get("token")
    }
    session.post("{}/api/projects".format(url), headers=headers, json={"project_name": "{}-project".format(name)})
    id = get_pid()
    c_id=id[0]
    body = {
        "project_id": c_id,
        "filter_name": "Common Filter",
        "filter_data": {
            "easy_filters": {
                "address_search_key": "address_search_key",
                "city_values": [
                    "test_cities"
                ],
                "state_values": [
                    "test_states"
                ],
                "zip_values": [
                    "test_zips"
                ],
                "favorite_filter": "all",
                "approved_filter": "all"
            },
            "advanced_filters": None
        },
        "is_common": True
    }
    rep = session.post("{}/api/v1/customer/saved-filters".format(url),json=body)

    response=json.loads(rep.text)

    return [body,response,c_id]

@pytest.fixture(scope="class")
def create_project_and_order(create_newpwith_addresses):
    project_id = create_newpwith_addresses
    order=session.post("{}/api/order/place?project_id={}".format(url,project_id),headers={"token":session.cookies.get("token")})
    time.sleep(3)
    return project_id


