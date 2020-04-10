import os
import time
import traceback
from src.databases.connection import db_engine, bind_session
from src.services import UpsertOrder, PancakeApi, GHTKApi
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
ghtk_api = GHTKApi('C424f45770F03F8D0ab87A2c1dB81c0D0505A6Ec')


def fetch_order(max_page=-1):
    shops = shop_repo.find()

    for shop in shops:
        _fetch_order(
            shop=shop,
            max_page=max_page,
        )


def _fetch_order(shop, page=1, page_size=100, max_page=-1):
    try:
        result = pancake_api.list_order(
            shop_id=shop.pancake_id,
            page=page,
            page_size=page_size,
        )
    except Exception:
        traceback.print_exc()
        return

    page_number = result["page_number"]
    total_pages = result["total_pages"]
    print(f'Fetch order from {shop.name} {page_number}/{total_pages}')
    for idx, order in enumerate(result['orders']):
        print(f'    Store order {idx+1}/ {order["id"]}')
        if 'partner' in order:
            tracking_number = order['partner'].get('extend_code', None)
            if tracking_number:
                data = ghtk_api.get_order(tracking_number)
                order['ghtk'] = data

        try:
            upsert_order.execute(order)
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()
            import pdb; pdb.set_trace()
            traceback.print_exc()

    time.sleep(2)

    if max_page > 0 and page_number >= max_page:
        return

    import pdb; pdb.set_trace()
    if page_number < total_pages:
        _fetch_order(
            shop=shop,
            page=page+1,
            page_size=page_size,
            max_page=max_page,
        )
