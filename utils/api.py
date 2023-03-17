import requests

from utils.logger import create_logger


class Api:
    def __init__(self, url):
        self.base_url = url
        self.logger = create_logger(__name__)

    def get_dishes(self, year, month):
        url = f'{self.base_url}/api/hospitalDishes?year={year}&month={month}'

        payload = {}
        headers = {}

        data = []
        status_code = 0

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            status_code = response.status_code
            if response.status_code == 200:
                data = response.json()['data']['hospitalDishes']
                self.logger.info(f'[API] {url} success')
            else:
                self.logger.error(f"[API] {url} failed: {response.json()}")
        except:
            self.logger.critical(f'[API] {url} error', exc_info=True)

        return {
            'status_code': status_code,
            'data': data
        }
