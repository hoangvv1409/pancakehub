import click
from src.apps.fetchers import (
    order_15min_fetcher, all_order_fetcher,
    shop_hourly_fetcher
)


workers = dict(
    shop_hourly_fetcher=shop_hourly_fetcher,
    order_15min_fetcher=order_15min_fetcher,
    all_order_fetcher=all_order_fetcher,
)


@click.command()
@click.option('-w', '--worker', type=str, required=True, help='Worker name')
@click.option('-b', '--background', type=bool, default=False,
              help='Run in background', show_default=True)
def run_worker(worker, background):
    worker_runner = workers.get(worker)
    if not worker_runner:
        click.echo('Worker [{}] not found!'.format(worker))
        return None
    worker_runner()


if __name__ == '__main__':
    run_worker()
