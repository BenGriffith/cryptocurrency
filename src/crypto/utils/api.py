import requests
from decouple import config


class Connection:

    def __init__(self) -> None:
        self._api_key = config("COINMARKET_API_KEY", cast=str)
        self._headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": f"{self._api_key}"
        }
        self._parameters = {
            "start": "1",
            "limit": "5000",
        }

    def request(self, url: str) -> dict:
        response = requests.get(url, headers=self._headers, params=self._parameters)
        data = response.json()
        return data