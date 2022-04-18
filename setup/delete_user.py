import requests
url = "http://stage.geoxanalytics.com"
id="62585596d417bb7e7c943334"
ck = {"isLogin":"true"}
def deleteUser():
    session = requests.session()
    login =session.post(url + "/api/login", json={"email": "ui@fff.ddl", "password":"123456"})
    delete = session.delete("{}/api/delete/customer/{}".format(url, id))
    print(login.status_code)
    print(login.text)
    print("-----------------")
    print(delete.status_code)
    print(delete.text)
deleteUser()


