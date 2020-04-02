import time
import schedule
from .fetch_shop import fetch_shop


def shop_hourly_fetcher():
    fetch_shop()
    schedule.every().hour.do(fetch_shop)
    while True:
        schedule.run_pending()
        time.sleep(300)
