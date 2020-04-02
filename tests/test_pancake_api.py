# flake8: noqa
from src.services.pancake_api import PancakeApi

access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI0YWFhMTQzZS1iM2VjLTQ1YzUtOWQ2Ni01YmNlOTY2NDM1MGIiLCJpYXQiOjE1ODU2MzA4NTAsImZiX25hbWUiOiJWxakgSG_DoG5nIiwiZmJfaWQiOiIxMzY4Njg3MTk5ODY5NTMxIiwiZXhwIjoxNTkzNDA2ODUwfQ.qAPpFdfdZBOFQVqdk6lIbbfyrXVfFXXwbwzoYk4kfRo'


class TestPancakeApi():
    def test_list_shop(self):
        pancake_api = PancakeApi(
            access_token=access_token
        )

        result = pancake_api.list_shop()
        # import pdb; pdb.set_trace()
        # pass

    def test_list_order(self):
        pancake_api = PancakeApi(
            access_token=access_token
        )

        result = pancake_api.list_order(shop_id=1339971)
        result = pancake_api.list_order(shop_id=1339971, page=2)
        result = pancake_api.list_order(shop_id=1339971, page_size=100)
        # import pdb; pdb.set_trace()
        # pass
