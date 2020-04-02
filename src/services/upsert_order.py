class UpsertOrder():
    def __init__(self, raw_order_repository):
        self.raw_order_repo = raw_order_repository

    def execute(self, body):
        order_dict = self._create_raw_order_from_pancake(body)

        order = self.raw_order_repo.first(
            pancake_id=body['id']
        )

        if order:
            self.raw_order_repo.update(order, **order_dict)
        else:
            self.raw_order_repo.create(**order_dict)

    def _create_raw_order_from_pancake(self, body):
        return dict(
            pancake_id=body['id'],
            pancake_shop_id=body['shop_id'],
            payload=body,
            inserted_at=body['inserted_at'],
        )
