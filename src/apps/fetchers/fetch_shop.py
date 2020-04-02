import os
import traceback
from src.databases.connection import db_engine, bind_session
from src.services import UpsertShop, PancakeApi
from src.databases.repositories import (
    ShopRepository, FbPageRepository,
)

engine = db_engine(os.getenv('DATABASE_URI'))
session = bind_session(engine)

shop_repo = ShopRepository(session)
fb_page_repo = FbPageRepository(session)

upsert_shop = UpsertShop(
    shop_repository=shop_repo,
    fb_page_repository=fb_page_repo,
)
pancake_api = PancakeApi('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI0YWFhMTQzZS1iM2VjLTQ1YzUtOWQ2Ni01YmNlOTY2NDM1MGIiLCJpYXQiOjE1ODU2MzA4NTAsImZiX25hbWUiOiJWxakgSG_DoG5nIiwiZmJfaWQiOiIxMzY4Njg3MTk5ODY5NTMxIiwiZXhwIjoxNTkzNDA2ODUwfQ.qAPpFdfdZBOFQVqdk6lIbbfyrXVfFXXwbwzoYk4kfRo')


def fetch_shop():
    shops = pancake_api.list_shop()

    for shop in shops:
        print(f'Store {shop["name"]}')
        try:
            upsert_shop.execute(shop)
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()
            traceback.print_exc()
