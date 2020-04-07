import requests


class GHTKApi():
    def __init__(self, access_token):
        self.base_url = 'https://services.giaohangtietkiem.vn'
        self.access_token = access_token

    def get_order(self, tracking_number):
        url = '{}/services/shipment/v2/{}'.format(
            self.base_url,
            tracking_number,
        )
        response = self._get(url)

        return response['order'] if 'order' in response else None

    def _get(self, url):
        response = requests.get(url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Token': self.access_token,
        })

        if response.status_code // 100 != 2:
            raise Exception(str(response.json()))

        return response.json()
