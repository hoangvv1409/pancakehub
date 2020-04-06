import requests


class GHTKApi():
    def __init__(self, access_token):
        self.base_url = 'https://services.giaohangtietkiem.vn'
        self.access_token = 'C424f45770F03F8D0ab87A2c1dB81c0D0505A6Ec'

    def get_order(self, tracking_number):
        url = '{}/services/shipment/v2/{}'.format(
            self.base_url,
            tracking_number,
        )
        response = self._get(url)

        return response['order'] if response else None

    def _get(self, url):
        response = requests.get(url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Token': self.access_token,
        })

        if response.status_code // 100 != 2:
            raise Exception(str(response.json()))

        return response.json()
