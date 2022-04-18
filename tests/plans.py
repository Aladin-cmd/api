import json

from setup.setup import teardown_class, setup_class, session, url


class Test():

    @classmethod
    def setup_class(cls):
        setup_class()

    @classmethod
    def teardown_class(cls):
        teardown_class()

    def test_assign_plan(self, get_card_id):
        card = get_card_id
        token = session.cookies.get("token")
        getPlan = session.get("{}/api/plans".format(url), headers={"token": token})
        plan_data = json.loads(getPlan.text)
        plan_id = []
        pd=plan_data["data"]["plans"]
        # for plan in range(len(pd)):
        #     plan_id.append(pd[plan]["id"])
        # payload = {
        #     "plan_id": plan_id[0],
        #     "card_id": card[0],
        #     "coupon_code": "GEOX_30"
        # }
        # assign_plan = session.post("{}/api/customer/assign-plan".format(url), headers={"token": token}, json=payload)
        # expect = {
        #     "data": None,
        #     "msg": "OK",
        #     "status": 200
        # }
        # d = json.loads(assign_plan.text)
        # assert d == expect
        print(pd)
