import json, string, pytest, null, random, requests


def random_email(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


session = requests.session()
email = random_email(7) + "@gmail.com"
password = "123456"
url = "http://stage.geoxanalytics.com"
data = {
    "email": email,
    "password": password,
    "city": 'Test',
    "billing_address": 'Test',
    "organization": 'Test',
    "company": 'Test',
    "zip": '12345',
    "work_phone": '55555555',
    "country": 'United States',
    "first_name": 'Test',
    "last_name": 'Test'
}
address=[
        {
            "address": "35 Riverside Rd",
            "city": "Mesquite",
            "state": "NV",
            "zip": "89027"
        },
        {
            "lat": "27.173722",
            "long": "-80.145446"
        },
        {
            "address": "11 Riverside Rd",
            "city": "Mesquite",
            "state": "NV"
        }
    ]

def create_project():
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
    js_response=[]
    for p in range(len(payload)):
        response_p = session.post("{}/api/projects".format(url), headers=headers, json=payload[p])
        js_response.append(json.loads(response_p.text))
    return js_response




def get_pid():
    pr = []
    response_projects = session.get("{}/api/projects".format(url))
    js_response = json.loads(response_projects.text)
    r = js_response["data"]["projects"]
    for er in range(len(r)):
        id = r[er]["id"]
        pr.append(id)
    return pr

def add_addresses_to_projects():
    create_project()
    list_id = get_pid()
    for er in list_id:
        cr = session.post("{}/api/projects/addresses".format(url), json={"project_id": str(er),
                                                        "addresses": address
                                                        })


def delete_project():
    res=[]
    token = session.cookies.get("token")
    headers = {
        'token': token
    }
    idlist=get_pid()
    for id in idlist:
        response = session.delete("{}/api/v1/projects/{}".format(url,id), headers=headers)
        print(response.text)
        res.append(response.text)
    return res

def setup_class():
    print("--------------------------Setup --> Create User --> Login--------------------------")
    print(email)
    response = session.post(url + "/api/register", json=data)
    if response.status_code == 200:
        print("User was created")
    else:
        print("\nUser wasn`t created --> something went wrong " + str(response.status_code))


def setup_admin():
    print("------------------Setup for admin panel--------------------")
    body={
        "email":"test@test.cc",
        "password":"123456"
    }
    login = session.post("{}/api/v1/admin/login".format(url),data=body)
    if login.status_code==200:
        print("User logged in")
    else:
        print("User wasn`t logged in")
def teardown_admin():
    logout= session.post("{}/api/auth/logout".format(url),headers={"token":session.cookies.get("token")})
def teardown_class():
    print("\n--------------------------Teardown --> Delete User--------------------------")
    # respLogin = requests.post(url+"/api/login",json={"email":email,"password":password})
    respID = session.get(url + "/api/customer")
    json_response = json.loads(respID.text)
    id = json_response["data"]["id"]
    delete = session.delete("{}/api/delete/customer/{}".format(url, id))
    print(delete.status_code)
    if delete.status_code==204:
        print('\nUser deleted successfully!')
    else:
        print("\nSomething went wrong... Check user with such data: "+email+"and\n"+id)
    print('\nDONE!!!!!')

# def setup_method():
#     print("Setup Each test case")
#
# def teardown_method():
#     print("Teardown Each test case")
