import os
import time
import traceback
from src.databases.connection import db_engine, bind_session
from src.services import UpsertOrder, PancakeApi
from src.databases.repositories import (
    RawOrderRepository, ShopRepository,
    OrderRepository, ItemRepository,
)

engine = db_engine(os.getenv('DATABASE_URI'))
session = bind_session(engine)

shop_repo = ShopRepository(session)
raw_order_repo = RawOrderRepository(session)
order_repo = OrderRepository(session)
item_repo = ItemRepository(session)


upsert_order = UpsertOrder(
    raw_order_repository=raw_order_repo,
    order_repository=order_repo,
    item_repository=item_repo,
)
pancake_api = PancakeApi('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI0YWFhMTQzZS1iM2VjLTQ1YzUtOWQ2Ni01YmNlOTY2NDM1MGIiLCJpYXQiOjE1ODU2MzA4NTAsImZiX25hbWUiOiJWxakgSG_DoG5nIiwiZmJfaWQiOiIxMzY4Njg3MTk5ODY5NTMxIiwiZXhwIjoxNTkzNDA2ODUwfQ.qAPpFdfdZBOFQVqdk6lIbbfyrXVfFXXwbwzoYk4kfRo')


def fetch_order(max_page=-1):
    shops = shop_repo.find()

    for shop in shops:
        print(f'Fetch order from {shop.name}')
        _fetch_order(
            shop_id=shop.pancake_id,
            max_page=max_page,
        )


def _fetch_order(shop_id, page=1, page_size=100, max_page=-1):
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
            import pdb; pdb.set_trace()
            traceback.print_exc()

    time.sleep(2)

    if max_page > 0 and result['page_number'] == max_page:
        return

    if result['page_number'] < result['total_pages']:
        _fetch_order(
            shop_id=shop_id,
            page=page+1,
            page_size=page_size
        )
