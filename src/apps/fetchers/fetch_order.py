import os
import time
import traceback
from src.databases.connection import db_engine, bind_session
from src.services import UpsertOrder, PancakeApi
from src.databases.repositories import (
    RawOrderRepository, ShopRepository
)

engine = db_engine(os.getenv('DATABASE_URI'))
session = bind_session(engine)

shop_repo = ShopRepository(session)
raw_order_repo = RawOrderRepository(session)

upsert_order = UpsertOrder(
    raw_order_repository=raw_order_repo,
)
pancake_api = PancakeApi('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI0YWFhMTQzZS1iM2VjLTQ1YzUtOWQ2Ni01YmNlOTY2NDM1MGIiLCJpYXQiOjE1ODU2MzA4NTAsImZiX25hbWUiOiJWxakgSG_DoG5nIiwiZmJfaWQiOiIxMzY4Njg3MTk5ODY5NTMxIiwiZXhwIjoxNTkzNDA2ODUwfQ.qAPpFdfdZBOFQVqdk6lIbbfyrXVfFXXwbwzoYk4kfRo')


def fetch_order():
    shops = shop_repo.find()

    for shop in shops:
        print(f'Fetch order from {shop.name}')
        _fetch_order(shop.pancake_id)


def _fetch_order(shop_id, page=1, page_size=100):
    try:
        result = pancake_api.list_order(
            shop_id=shop_id,
            page=page,
            page_size=page_size,
        )
    except Exception:
        traceback.print_exc()
        return

    for order in result['orders']:
        print(f'    Store order {order["id"]}')
        try:
            upsert_order.execute(order)
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()
            traceback.print_exc()

    time.sleep(1)

    if result['page_number'] < result['total_pages']:
        _fetch_order(
            shop_id=shop_id,
            page=page+1,
            page_size=page_size
        )
