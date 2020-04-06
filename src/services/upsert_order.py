import re


class UpsertOrder():
    def __init__(self, raw_order_repository, order_repository,
                 item_repository):
        self.raw_order_repo = raw_order_repository
        self.order_repo = order_repository
        self.item_repo = item_repository

    def execute(self, body):
        raw_order_dict = self._create_raw_order_from_pancake(body)
        order_dict = self._create_order_from_pancake(body)
        items_dict = [
            self._create_item_from_pancake(
                pancake_order_id=body['id'],
                item=item,
            )
            for item in body['items']
        ]

        raw_order = self.raw_order_repo.first(
            pancake_id=body['id']
        )

        if raw_order:
            self.raw_order_repo.update(raw_order, **raw_order_dict)
        else:
            self.raw_order_repo.create(**raw_order_dict)

        self._handle_order(order_dict)
        [self._handle_item(item_dict)
         for item_dict in items_dict]

    def _handle_order(self, order_dict):
        order = self.order_repo.first(
            pancake_id=order_dict['pancake_id']
        )

        if order:
            self.order_repo.update(order, **order_dict)
        else:
            self.order_repo.create(**order_dict)

    def _handle_item(self, item_dict):
        item = self.item_repo.first(
            pancake_id=item_dict['pancake_id']
        )

        if item:
            self.item_repo.update(item, **item_dict)
        else:
            self.item_repo.create(**item_dict)

    def _create_raw_order_from_pancake(self, body):
        return dict(
            pancake_id=body['id'],
            pancake_shop_id=body['shop_id'],
            payload=body,
            inserted_at=body['inserted_at'],
        )

    def _create_order_from_pancake(self, body):
        order_id = None
        tracking_numbers = None
        partner_id = None
        partner_str = None

        if 'partner' in body:
            partner = body['partner']
            tracking_numbers = partner.get('extend_code', None)
            partner_id = partner['partner_id']
            partner_str = self._get_partner_str(partner_id)
            order_id = self._get_order_id(partner)

        full_address = body['shipping_address']['full_address']
        # x = re.search('Thành phố *,', full_address)
        # if x:
        #     import pdb; pdb.set_trace()
        #     pass

        return dict(
            pancake_id=body['id'],
            pancake_shop_id=body['shop_id'],
            display_id=body['display_id'],
            fb_page_id=body['page_id'],
            inserted_at=body['inserted_at'],
            order_id=order_id,
            full_name=body['shipping_address']['full_name'],
            phone_number=body['shipping_address']['phone_number'],
            full_address=full_address,
            province_id=body['shipping_address']['province_id'],
            district_id=body['shipping_address']['district_id'],
            total_cod=body['cod'],
            status=body['status'],
            status_str=self._get_status_str(body['status']),
            partner_id=partner_id,
            partner_str=partner_str,
            status_updated_at=body['last_update_status_at'],
            sale=body['status_history'][0]['name'],
            tracking_numbers=tracking_numbers,
        )

    def _create_item_from_pancake(self, pancake_order_id, item):
        name = item['variation_info']['name']
        variant = item['variation_info']['detail']

        return dict(
            pancake_id=item['id'],
            pancake_order_id=pancake_order_id,
            name=item['variation_info']['name'],
            variant=variant if variant else name,
            quantity=item['quantity'],
        )

    def _get_partner_str(self, partner_id):
        return {
            0: 'SNP',
            1: 'GHTK',
            8: 'SPL',
        }.get(partner_id, None)

    def _get_status_str(self, status):
        return {
            0: 'Mới',
            1: 'Đã xác nhận',
            2: 'Đã gửi hàng',
            3: 'Đã nhận',
            4: 'Đang hoàn',
            5: 'Đã hoàn',
            6: 'Đã huỷ',
        }.get(status, None)

    def _get_order_id(self, partner):
        if 'service_partner' not in partner:
            return
        if partner['service_partner'] is None:
            return

        return partner['service_partner']['order']['id']
