import requests
import utils
from utils.logger import create_logger


class Api:
    def __init__(self):
        self.base_url = utils.config.url
        self.logger = create_logger(__name__)

    def get_dishes(self, year):
        url = f'{self.base_url}/api/hospitalDishes?year={year}'

        payload = {}
        headers = {}

        data = []
        status_code = 0

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            status_code = response.status_code
            if response.status_code == 200:
                data = response.json()['data']['hospitalDishes']
                self.logger.info(f'{url} success')
            else:
                self.logger.error(f"{url} failed: {response.json()}")
        except:
            self.logger.critical(f'{url} error', exc_info=True)

        return {
            'status_code': status_code,
            'data': data
        }

    def upload_data(self, data):
        url = f'{self.base_url}/api/hospitalCollection'

        payload = data['payload']

        files = [
            ('file', ('{}.npz'.format(data['file_name']), open(data['file_path'], 'rb'), 'application/octet-stream'))
        ]

        headers = {}

        status_code = 0

        try:
            response = requests.request('POST', url, headers=headers, data=payload, files=files, timeout=30)
            status_code = response.status_code
            if response.status_code == 200:
                self.logger.info(f'{url} success')
            else:
                self.logger.error(f"{url} failed: {response.json()}")

        except:
            self.logger.error(f'{url} error', exc_info=True)

        return {
            'status_code': status_code,
        }
