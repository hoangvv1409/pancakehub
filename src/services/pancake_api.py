import requests


class PancakeApi():
    def __init__(self, access_token):
        self.base_url = 'https://pos.pages.fm/api/v1'
        self.access_token = access_token

    def list_shop(self):
        url = f'{self.base_url}/shops?access_token={self.access_token}'
        response = self._get(url)

        return response['shops'] if response else None

    def list_order(self, shop_id, page=1, page_size=30):
        url = '{}/shops/{}/orders?access_token={}'.format(
            self.base_url,
            shop_id,
            self.access_token,
        )
        url += '&page_size={}&status=-1&page={}'.format(
            page_size,
            page,
        )
        response = self._get(url)
        if not response:
            return None

        return {
            'orders': response['data'],
            'page_number': response['page_number'],
            'page_size': response['page_size'],
            'total_entries': response['total_entries'],
            'total_pages': response['total_pages'],
        }

    def _get(self, url):
        response = requests.get(url)

        if response.status_code // 100 != 2:
            raise Exception(str(response.json()))

        return response.json()
