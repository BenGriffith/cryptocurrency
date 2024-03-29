import requests
from decouple import config


class Connection:

    def __init__(self, limit: int = 5000) -> None:
        self._api_key = config("COINMARKET_API_KEY", cast=str)
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": f"{self._api_key}"
        }
        self.parameters = {
            "start": 1,
            "limit": limit,
        }

    def request(self, url: str) -> dict:
        response = requests.get(url, headers=self.headers, params=self.parameters)
        data = response.json()
        return data