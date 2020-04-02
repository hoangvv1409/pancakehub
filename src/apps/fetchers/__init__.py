import time
import schedule
from .fetch_shop import fetch_shop
from .fetch_order import fetch_order


def shop_hourly_fetcher():
    fetch_shop()
    schedule.every().hour.do(fetch_shop)
    while True:
        schedule.run_pending()
        time.sleep(600)


def order_15min_fetcher():
    fetch_order()
    schedule.every(15).minutes.do(fetch_order)
    while True:
        schedule.run_pending()
        time.sleep(300)
