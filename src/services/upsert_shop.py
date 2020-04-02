class UpsertShop():
    def __init__(self, shop_repository, fb_page_repository):
        self.shop_repo = shop_repository
        self.fb_page_repo = fb_page_repository

    def execute(self, body):
        shop_dict = self._create_shop_from_pancake(body)
        fb_pages_dict = self._create_fb_page_from_pancake(body)

        shop = self.shop_repo.first(
            pancake_id=shop_dict['pancake_id']
        )

        if shop:
            self.shop_repo.update(shop, **shop_dict)
        else:
            self.shop_repo.create(**shop_dict)

        [self._handle_fb_page(fb_page)
         for fb_page in fb_pages_dict]

    def _create_shop_from_pancake(self, body):
        return dict(
            pancake_id=body['id'],
            name=body['name'],
            info=body,
        )

    def _create_fb_page_from_pancake(self, body):
        fb_pages = []
        for fb_page in body['pages']:
            fb_pages.append(
                dict(
                    fb_page_id=int(fb_page['id']),
                    pancake_shop_id=fb_page['shop_id'],
                    name=fb_page['name'],
                )
            )
        return fb_pages

    def _handle_fb_page(self, fb_page_dict):
        fb_page = self.fb_page_repo.first(
            fb_page_id=fb_page_dict['fb_page_id']
        )
        if fb_page:
            self.fb_page_repo.update(fb_page, **fb_page_dict)
        else:
            self.fb_page_repo.create(**fb_page_dict)
