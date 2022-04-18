import json
class User:
    with open(r"D:\python\api_testing\JSON_info_for_tests\user_info.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()


    #create test data for login user
    data = [(jsonObject['valid_user'], 200, "OK"),
            (jsonObject['non-ex_user'], 400, "No customer found with given email"),
            (jsonObject['wrong_password'], 400, "Incorrect email/password"),
            (jsonObject['no_email'], 400, "Required parameters missing"),
            (jsonObject['no_password'], 400, "Required parameters missing"),
            (jsonObject['empty_full'], 400, "Required parameters missing"),
            (jsonObject['wrong_email_format'], 400, "No customer found with given email")
            ]

